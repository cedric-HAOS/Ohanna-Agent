# ADR-0017 — Architecture du Recovery Engine

## Statut

Accepté

## Date

2026-07-08

## Contexte

Les ADR précédentes ont introduit deux briques fondamentales :

* **ADR-0015** : le `HealthMonitor`, chargé d'observer l'état de santé du système ;
* **ADR-0016** : les `Heartbeat` et `Watchdog`, permettant de détecter les composants inactifs ou bloqués.

À ce stade, Shikamaru est capable de détecter une anomalie, mais aucune action corrective n'est entreprise.

Le Sprint 4 vise à rendre l'agent autonome. Pour cela, il est nécessaire d'introduire un composant spécialisé dans la prise de décision et l'exécution des actions de récupération.

## Décision

Créer un composant dédié nommé `RecoveryEngine`.

Le `RecoveryEngine` sera responsable de :

* recevoir les anomalies signalées par le `HealthMonitor` ;
* déterminer si une récupération est nécessaire ;
* sélectionner la stratégie de récupération appropriée ;
* exécuter les actions correctives ;
* suivre le résultat de chaque tentative ;
* publier les événements associés.

Le `RecoveryEngine` ne réalisera aucun diagnostic de santé.

Cette responsabilité reste exclusivement confiée au `HealthMonitor`.

## Principe d'architecture

L'architecture est volontairement découpée en deux niveaux :

```text
               HealthMonitor
                      │
         HealthResult / Events
                      │
                      ▼
             RecoveryEngine
                      │
          Recovery Strategy
                      │
                      ▼
             Recovery Actions
```

Cette séparation garantit que :

* l'observation reste indépendante de la réparation ;
* les stratégies peuvent évoluer sans modifier le Health Monitor ;
* les actions correctives restent remplaçables.

## Architecture retenue

Nouveau package :

```text
recovery/
    __init__.py
    action.py
    engine.py
    event.py
    strategy.py
```

## Responsabilités

### RecoveryEngine

Le moteur coordonne l'ensemble du processus de récupération.

Responsabilités :

* écouter les événements de santé ;
* éviter les récupérations concurrentes ;
* appliquer les stratégies ;
* enregistrer les tentatives ;
* publier les événements de récupération.

API conceptuelle :

```python
class RecoveryEngine:

    def handle(self, result: HealthResult) -> None:
        ...

    def recover(self, source: str) -> None:
        ...

    def is_recovering(self, source: str) -> bool:
        ...
```

## RecoveryStrategy

Une stratégie décrit la manière de récupérer un type de panne.

Exemple :

```python
class RecoveryStrategy(Protocol):

    def can_handle(
        self,
        result: HealthResult,
    ) -> bool:
        ...

    def execute(
        self,
        result: HealthResult,
    ) -> RecoveryResult:
        ...
```

Chaque stratégie reste indépendante.

Exemples futurs :

* PluginRecoveryStrategy
* MQTTRecoveryStrategy
* ConfigurationRecoveryStrategy

## RecoveryAction

Une action représente une opération élémentaire.

Exemples :

* redémarrer un plugin ;
* recharger une configuration ;
* reconnecter MQTT ;
* vider un cache ;
* redémarrer un service.

Une stratégie peut exécuter plusieurs actions successives.

## RecoveryResult

Chaque tentative produit un résultat structuré.

Exemple conceptuel :

```python
@dataclass(frozen=True)
class RecoveryResult:
    success: bool
    action: str
    source: str
    message: str | None = None
```

## Flux de fonctionnement

Le cycle nominal est le suivant :

```text
HealthMonitor

↓

HealthResult

↓

RecoveryEngine

↓

RecoveryStrategy

↓

RecoveryAction(s)

↓

RecoveryResult

↓

Publication d'événements
```

## Prévention des récupérations simultanées

Pour une même source, une seule récupération peut être exécutée simultanément.

Exemple :

```text
plugin.dhcp

↓

Recovery en cours

↓

Nouvelle erreur

↓

Ignorée ou mise en attente
```

Cette règle évite :

* les redémarrages multiples ;
* les effets de course ;
* les états incohérents.

## Événements produits

Le Recovery Engine pourra publier :

```text
recovery.started
recovery.completed
recovery.failed
recovery.skipped
recovery.cancelled
```

Ces événements seront utilisés par :

* MQTT ;
* les logs ;
* les métriques ;
* l'interface web.

## Principes de conception

Le Recovery Engine doit être :

* découplé du Health Monitor ;
* extensible ;
* déterministe ;
* testable ;
* indépendant des plugins ;
* indépendant de MQTT.

Toutes les dépendances concrètes seront injectées.

## Cas non couverts

Cette ADR ne définit pas :

* l'ordre des tentatives ;
* les politiques de retry ;
* le backoff exponentiel ;
* le mode dégradé ;
* les seuils de déclenchement.

Ces sujets seront définis dans les ADR suivantes.

## Conséquences positives

* Séparation claire entre détection et réparation.
* Architecture facilement extensible.
* Ajout de nouvelles stratégies sans modifier le moteur.
* Forte testabilité.
* Réduction du couplage entre les composants.
* Préparation de l'auto-réparation avancée.

## Conséquences négatives

* Introduction d'un nouveau package.
* Multiplication des objets métiers.
* Coordination supplémentaire entre les composants.
* Nécessité d'éviter les récupérations concurrentes.

## Décision finale

Ohana-Agent adopte un `RecoveryEngine` dédié.

Le `HealthMonitor` reste responsable de la détection des anomalies.

Le `RecoveryEngine` devient l'unique composant chargé d'orchestrer les opérations de récupération en s'appuyant sur des stratégies et des actions spécialisées.

Cette séparation constitue la base de l'architecture d'auto-réparation de Shikamaru.

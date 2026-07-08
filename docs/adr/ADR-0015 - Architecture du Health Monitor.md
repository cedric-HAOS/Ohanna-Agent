# ADR-0015 — Architecture du Health Monitor

## Statut

Accepté

## Date

2026-07-08

## Contexte

Ohanna-Agent dispose désormais d’un socle stable :

* cycle de vie applicatif maîtrisé ;
* configuration centralisée ;
* bus d’événements interne ;
* système de commandes ;
* runtime MQTT fonctionnel ;
* plugins intégrables ;
* 156 tests validés.

Le Sprint 4 introduit la capacité d’auto-réparation.

Avant de corriger automatiquement un problème, Shikamaru doit d’abord être capable de l’observer, le qualifier et l’exposer clairement.

Le Health Monitor devient donc le composant chargé de surveiller l’état de santé global de l’agent.

## Décision

Créer un composant dédié nommé `HealthMonitor`.

Il sera responsable de :

* centraliser les contrôles de santé ;
* exécuter les checks enregistrés ;
* agréger les résultats ;
* produire un état de santé global ;
* détecter les situations dégradées ;
* publier des événements de santé ;
* fournir une base exploitable par le futur Recovery Engine.

Le Health Monitor ne corrigera pas directement les problèmes.

Il observe, qualifie et signale.

La réparation sera déléguée au Recovery Engine introduit dans une ADR ultérieure.

## Architecture retenue

Nouveau package :

```text
health/
    __init__.py
    check.py
    monitor.py
    result.py
    status.py
```

## Concepts principaux

### HealthStatus

Représente l’état de santé d’un composant.

Valeurs prévues :

```python
class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
```

### HealthCheck

Représente un contrôle de santé unitaire.

Un check doit :

* avoir un nom stable ;
* être exécutable ;
* retourner un résultat structuré ;
* ne pas modifier l’état du système ;
* ne pas déclencher directement de réparation.

Interface conceptuelle :

```python
class HealthCheck(Protocol):
    name: str

    def run(self) -> HealthResult:
        ...
```

### HealthResult

Représente le résultat d’un contrôle.

Champs principaux :

```python
@dataclass(frozen=True)
class HealthResult:
    name: str
    status: HealthStatus
    message: str | None = None
    details: dict[str, Any] | None = None
```

### HealthMonitor

Responsabilités :

```python
class HealthMonitor:
    def register(self, check: HealthCheck) -> None:
        ...

    def unregister(self, name: str) -> None:
        ...

    def run_once(self) -> list[HealthResult]:
        ...

    def get_status(self) -> HealthStatus:
        ...
```

## Règles d’agrégation

L’état global du Health Monitor sera calculé ainsi :

| Résultats observés                          | État global |
| ------------------------------------------- | ----------- |
| Tous `HEALTHY`                              | `HEALTHY`   |
| Au moins un `DEGRADED` et aucun `UNHEALTHY` | `DEGRADED`  |
| Au moins un `UNHEALTHY`                     | `UNHEALTHY` |
| Aucun check enregistré                      | `UNKNOWN`   |

## Événements produits

Le Health Monitor pourra publier des événements internes du type :

```text
health.check.completed
health.status.changed
health.degraded
health.unhealthy
```

Ces événements seront ensuite exploitables par :

* le runtime MQTT ;
* les logs ;
* le Recovery Engine ;
* les plugins ;
* l’interface web future.

## Comportement attendu

Le Health Monitor doit être :

* déterministe ;
* testable ;
* sans dépendance forte à MQTT ;
* sans dépendance forte au Recovery Engine ;
* compatible avec l’exécution synchrone dans un premier temps ;
* extensible vers une exécution périodique ensuite.

## Limites de cette ADR

Cette ADR ne définit pas encore :

* les watchdogs ;
* les heartbeats ;
* les stratégies de réparation ;
* le backoff ;
* le mode dégradé complet ;
* la désactivation automatique de plugins.

Ces sujets seront traités dans les ADR suivantes.

## Conséquences positives

* Séparation claire entre observation et réparation.
* Architecture plus testable.
* Base solide pour l’auto-réparation.
* Possibilité d’exposer l’état de santé via MQTT.
* Préparation de l’interface web.
* Ajout progressif de checks sans modifier le noyau.

## Conséquences négatives

* Introduction d’un nouveau package.
* Nécessité de maintenir un modèle de santé cohérent.
* Risque de duplication avec certains états existants si la frontière n’est pas respectée.

## Décision finale

Ohanna-Agent adopte un `HealthMonitor` dédié.

Il sera le point central d’observation de la santé de Shikamaru.

Il ne réparera pas directement les erreurs.

Il fournira les signaux nécessaires au futur moteur d’auto-réparation.

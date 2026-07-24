# ADR-0018 — Recovery Policies

## Statut

Accepté

## Date

2026-07-08

## Contexte

L'ADR-0017 introduit le `RecoveryEngine`, chargé d'exécuter les opérations de récupération.

Cependant, un moteur de récupération ne doit jamais appliquer les mêmes actions à toutes les erreurs.

Certaines anomalies nécessitent simplement une nouvelle tentative, tandis que d'autres imposent un redémarrage, une désactivation ou le passage en mode dégradé.

Afin de conserver une architecture extensible et prévisible, les règles de récupération doivent être isolées dans un système de politiques (Recovery Policies).

## Décision

Ohana-Agent adopte un système de **Recovery Policies**.

Une Recovery Policy définit le comportement complet à appliquer lorsqu'une anomalie est détectée.

Une politique précise notamment :

* les types d'erreurs concernés ;
* les actions autorisées ;
* leur ordre d'exécution ;
* le nombre maximal de tentatives ;
* les délais entre les tentatives ;
* les critères d'abandon ;
* les conditions de succès.

Le `RecoveryEngine` exécute les politiques mais ne contient aucune règle métier spécifique.

## Architecture retenue

Nouveau module :

```text
recovery/
    policy.py
```

Architecture complète :

```text
recovery/
    __init__.py
    action.py
    engine.py
    event.py
    policy.py
    strategy.py
```

## Principe général

Le fonctionnement est le suivant :

```text
HealthMonitor

↓

HealthResult

↓

RecoveryEngine

↓

RecoveryPolicy

↓

RecoveryStrategy

↓

RecoveryAction(s)
```

Le moteur délègue entièrement les décisions à la politique sélectionnée.

## Interface conceptuelle

Une politique implémente le protocole suivant :

```python
class RecoveryPolicy(Protocol):

    def applies_to(
        self,
        result: HealthResult,
    ) -> bool:
        ...

    def next_action(
        self,
        history: RecoveryHistory,
    ) -> RecoveryAction | None:
        ...
```

La méthode `next_action()` retourne :

* la prochaine action à exécuter ;
* ou `None` lorsque la politique considère que la récupération est terminée ou impossible.

## Historique des tentatives

Chaque récupération possède un historique.

Exemple conceptuel :

```python
@dataclass
class RecoveryHistory:
    source: str
    attempts: int
    last_action: str | None
    last_result: bool | None
```

L'historique permet à la politique de prendre ses décisions sans conserver d'état interne.

## Politique déterministe

Une Recovery Policy doit toujours produire le même résultat pour un même historique.

Elle ne doit pas :

* dépendre d'un état global ;
* utiliser des valeurs aléatoires ;
* modifier directement les composants.

Elle décrit uniquement la séquence logique des actions.

## Exemple : perte de connexion MQTT

Politique :

```text
Tentative 1
↓
Reconnecter MQTT

↓

Succès ?
├── Oui → Fin
└── Non

↓

Tentative 2
↓
Reconnecter MQTT

↓

Succès ?
├── Oui → Fin
└── Non

↓

Tentative 3
↓
Reconnecter MQTT

↓

Échec

↓

Publication d'un événement
```

## Exemple : plugin bloqué

Politique :

```text
Heartbeat expiré

↓

Restart Plugin

↓

Échec ?

↓

Reload Plugin

↓

Échec ?

↓

Disable Plugin

↓

Notification
```

## Exemple : configuration invalide

Politique :

```text
Erreur configuration

↓

Rechargement

↓

Toujours invalide ?

↓

Abandon

↓

Événement critique
```

## Types de politiques

Le système doit permettre plusieurs familles de politiques.

Exemples :

* PluginRecoveryPolicy
* MQTTRecoveryPolicy
* ConfigurationRecoveryPolicy
* ServiceRecoveryPolicy
* NetworkRecoveryPolicy

Chaque politique est indépendante.

## Priorité des politiques

Une seule politique peut être appliquée à une anomalie donnée.

Si plusieurs politiques correspondent, le moteur sélectionne celle ayant la priorité la plus élevée.

Chaque politique expose donc une priorité.

Exemple conceptuel :

```python
@property
def priority(self) -> int:
    ...
```

Une valeur élevée indique une priorité plus forte.

## Arrêt d'une politique

Une politique peut se terminer lorsque :

* la récupération a réussi ;
* le nombre maximal de tentatives est atteint ;
* aucune autre action n'est disponible ;
* la situation nécessite une intervention humaine.

Dans ce dernier cas, le moteur publie un événement approprié.

## Événements produits

Le moteur pourra publier les événements suivants :

```text
recovery.policy.selected
recovery.policy.completed
recovery.policy.failed
recovery.policy.aborted
```

Ces événements seront exploités par :

* les logs ;
* MQTT ;
* l'interface web ;
* les outils de supervision.

## Principes de conception

Une Recovery Policy doit être :

* spécialisée ;
* déterministe ;
* testable ;
* indépendante du moteur ;
* indépendante des plugins ;
* indépendante de MQTT.

Les politiques ne doivent contenir que des règles métier.

## Limites de cette ADR

Cette ADR ne définit pas :

* le mode dégradé global ;
* les délais de backoff exponentiel ;
* les notifications utilisateur ;
* les actions spécifiques à chaque plugin.

Ces éléments seront définis dans les ADR et implémentations ultérieures.

## Conséquences positives

* Séparation claire entre orchestration et règles métier.
* Ajout de nouvelles politiques sans modifier le moteur.
* Forte testabilité.
* Architecture évolutive.
* Comportement prévisible et reproductible.
* Possibilité de personnaliser les stratégies par composant.

## Conséquences négatives

* Augmentation du nombre de classes.
* Gestion des priorités entre politiques.
* Nécessité de maintenir un historique des tentatives.

## Décision finale

Ohana-Agent adopte un système de **Recovery Policies**.

Les décisions de récupération ne sont pas codées dans le `RecoveryEngine`, mais déléguées à des politiques spécialisées.

Cette approche garantit une architecture modulaire, déterministe et facilement extensible, adaptée aux futurs mécanismes d'auto-réparation de Shikamaru.

# ADR-0016 — Watchdog & Heartbeat

## Statut

Accepté

## Date

2026-07-08

## Contexte

ADR-0015 a introduit le `HealthMonitor`.

Il permet d’observer l’état de santé global de Shikamaru à travers des contrôles de santé structurés.

Cependant, certains problèmes ne sont pas visibles avec un simple check ponctuel.

Exemples :

* un plugin reste chargé mais ne répond plus ;
* une boucle interne est bloquée ;
* un service ne publie plus d’activité ;
* MQTT semble connecté mais aucun message attendu ne circule ;
* un composant est vivant techniquement mais inactif fonctionnellement.

Il faut donc ajouter un mécanisme de surveillance temporelle.

Ce mécanisme repose sur deux notions :

* le **heartbeat**, qui indique qu’un composant est encore vivant ;
* le **watchdog**, qui détecte l’absence de heartbeat dans un délai défini.

## Décision

Ohanna-Agent introduit un système de `Watchdog` et de `Heartbeat`.

Chaque composant critique pourra signaler régulièrement son activité au `HealthMonitor`.

Si un composant ne signale plus d’activité dans le délai attendu, son watchdog passera en état dégradé ou unhealthy.

Le watchdog ne réparera pas lui-même le composant.

Il produira un signal exploitable par le futur Recovery Engine.

## Architecture retenue

Nouveaux fichiers dans le package `health` :

```text
health/
    heartbeat.py
    watchdog.py
```

Architecture globale :

```text
health/
    __init__.py
    check.py
    heartbeat.py
    monitor.py
    result.py
    status.py
    watchdog.py
```

## Concepts principaux

### Heartbeat

Un heartbeat est un signal léger indiquant qu’un composant est toujours actif.

Il contient au minimum :

```python
@dataclass(frozen=True)
class Heartbeat:
    source: str
    timestamp: datetime
    metadata: dict[str, Any] | None = None
```

Le champ `source` doit être stable.

Exemples :

```text
plugin.dhcp
plugin.dns
mqtt.runtime
application.main_loop
```

## Watchdog

Un watchdog surveille une source précise.

Il compare :

* le dernier heartbeat reçu ;
* le délai maximal autorisé ;
* l’heure actuelle.

Exemple conceptuel :

```python
@dataclass
class Watchdog:
    source: str
    timeout_seconds: int
    degraded_after_seconds: int | None = None
```

## États possibles

Un watchdog peut produire les états suivants :

| Situation                                             | État        |
| ----------------------------------------------------- | ----------- |
| Heartbeat reçu récemment                              | `HEALTHY`   |
| Aucun heartbeat mais délai non expiré                 | `UNKNOWN`   |
| Heartbeat trop ancien mais seuil critique non atteint | `DEGRADED`  |
| Heartbeat absent ou expiré au-delà du timeout         | `UNHEALTHY` |

## API conceptuelle

Le `HealthMonitor` sera enrichi avec les méthodes suivantes :

```python
class HealthMonitor:
    def register_watchdog(
        self,
        source: str,
        timeout_seconds: int,
        degraded_after_seconds: int | None = None,
    ) -> None:
        ...

    def heartbeat(
        self,
        source: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        ...

    def check_watchdogs(self) -> list[HealthResult]:
        ...
```

## Règles de nommage des sources

Les noms de sources doivent être :

* stables ;
* lisibles ;
* en minuscules ;
* séparés par des points ;
* alignés avec les conventions MQTT quand c’est pertinent.

Exemples valides :

```text
application.main_loop
mqtt.runtime
plugin.dns
plugin.dhcp
plugin.ntp
plugin.supervision
```

Exemples non retenus :

```text
DNSPlugin
my plugin
runtime/mqtt
watchdog-1
```

## Règles de comportement

Un heartbeat :

* ne doit pas être coûteux ;
* ne doit pas bloquer le runtime ;
* ne doit pas déclencher de réparation ;
* met uniquement à jour le dernier instant connu d’activité.

Un watchdog :

* observe une source ;
* produit un `HealthResult` ;
* ne modifie pas directement le composant surveillé ;
* ne redémarre rien ;
* ne désactive rien.

## Événements produits

Le système pourra produire les événements suivants :

```text
health.heartbeat.received
health.watchdog.healthy
health.watchdog.degraded
health.watchdog.unhealthy
health.watchdog.recovered
```

Ces événements seront utilisables par :

* les logs ;
* MQTT ;
* le futur Recovery Engine ;
* l’interface web ;
* les tests d’intégration.

## Gestion du temps

Pour garantir la testabilité, le watchdog ne doit pas dépendre directement de `datetime.now()` de manière non contrôlable.

L’implémentation devra permettre d’injecter une horloge ou une fonction `now`.

Exemple conceptuel :

```python
def __init__(self, now: Callable[[], datetime] | None = None):
    self._now = now or datetime.now
```

## Tolérance aux erreurs

Si un heartbeat est reçu pour une source non enregistrée, deux comportements sont possibles :

* ignorer le heartbeat ;
* enregistrer automatiquement la source.

La décision retenue est :

```text
Un heartbeat pour une source inconnue est ignoré.
```

Justification :

* évite les fautes de frappe silencieuses ;
* garde une topologie de surveillance explicite ;
* rend les tests plus déterministes.

## Limites de cette ADR

Cette ADR ne définit pas encore :

* les stratégies de redémarrage ;
* les politiques de retry ;
* le backoff exponentiel ;
* la désactivation automatique de plugins ;
* le mode dégradé global ;
* la publication MQTT détaillée.

Ces sujets seront traités dans les ADR suivantes.

## Conséquences positives

* Détection des composants bloqués.
* Surveillance temporelle des plugins.
* Meilleure base pour l’auto-réparation.
* Tests possibles grâce à l’injection du temps.
* Séparation propre entre observation et action.
* Préparation du Recovery Engine.

## Conséquences négatives

* Ajout d’un modèle temporel à tester.
* Nécessité de définir des timeouts cohérents.
* Risque de faux positifs si les timeouts sont trop courts.
* Nécessité de standardiser les noms de sources.

## Décision finale

Ohanna-Agent adopte un mécanisme de `Heartbeat` et de `Watchdog`.

Les composants critiques pourront signaler leur activité au `HealthMonitor`.

Le watchdog détectera les absences ou retards de heartbeat et produira des résultats de santé structurés.

Aucune réparation ne sera déclenchée directement à ce niveau.

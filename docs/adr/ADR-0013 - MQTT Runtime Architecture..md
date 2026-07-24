# ADR-0013 — MQTT Runtime Architecture

## Statut

Proposé

## Contexte

Shikamaru dispose désormais d’un noyau applicatif structuré autour de services internes, d’un dispatcher d’événements, d’un modèle de configuration, d’un système de health check et d’un cycle de vie applicatif clair.

La prochaine étape consiste à connecter Shikamaru à l’écosystème Ohana via MQTT.

MQTT doit permettre à Shikamaru de :

* publier son état ;
* publier des événements ;
* recevoir des commandes ;
* transmettre des informations de santé ;
* dialoguer avec Home Assistant, les services réseau et les futurs plugins ;
* rester découplé du broker et de la bibliothèque MQTT utilisée.

Le runtime MQTT ne doit pas devenir une dépendance directe du cœur applicatif. Il doit rester une couche d’intégration remplaçable, testable et isolée.

## Décision

Shikamaru introduira une couche dédiée appelée **MQTT Runtime**.

Cette couche sera responsable de toute la communication MQTT.

Le reste de l’application ne devra jamais manipuler directement la bibliothèque MQTT sous-jacente.

L’architecture retenue est la suivante :

```text
Application
    │
    ▼
MQTT Runtime
    │
    ├── MQTTClient
    ├── MQTTPublisher
    ├── MQTTSubscriber
    ├── MQTTReconnectPolicy
    └── MQTTHeartbeatService
```

Le runtime MQTT exposera une API interne stable autour de la classe principale `MQTTClient`.

## Structure cible

La structure proposée est :

```text
core/
    mqtt/
        __init__.py
        client.py
        publisher.py
        subscriber.py
        reconnect.py
        heartbeat.py
        messages.py
```

## API interne

Le composant principal sera `MQTTClient`.

Il exposera les opérations suivantes :

```python
class MQTTClient:
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def publish(self, topic: str, payload: object) -> None:
        ...

    async def subscribe(self, topic: str) -> None:
        ...

    async def unsubscribe(self, topic: str) -> None:
        ...
```

Cette API sera utilisée par l’application, les services internes et les futurs plugins.

## Publisher

Le `MQTTPublisher` sera responsable de :

* sérialiser les messages ;
* appliquer le format JSON ;
* ajouter les métadonnées communes ;
* respecter les paramètres de QoS ;
* gérer l’option `retain` ;
* publier les messages vers le broker.

Exemple de publication :

```python
await mqtt.publish(
    topic="ohana/agent/shikamaru/status",
    payload=status_message,
)
```

## Subscriber

Le `MQTTSubscriber` sera responsable de :

* s’abonner aux topics configurés ;
* recevoir les messages entrants ;
* les valider ;
* les transformer en événements internes ;
* les transmettre au dispatcher.

Le flux retenu est :

```text
Broker MQTT
    │
    ▼
MQTTSubscriber
    │
    ▼
Event
    │
    ▼
Dispatcher
    │
    ▼
Handlers
```

Aucun handler ne devra dépendre directement de MQTT.

## Intégration avec le Dispatcher

Les messages MQTT entrants seront convertis en événements internes.

Exemple :

```text
ohana/agent/shikamaru/command
        │
        ▼
CommandReceivedEvent
        │
        ▼
Dispatcher
```

Cela permet de conserver une architecture événementielle cohérente.

## Heartbeat

Shikamaru publiera régulièrement un heartbeat MQTT.

Topic cible :

```text
ohana/agent/shikamaru/status
```

Payload indicatif :

```json
{
  "agent": "shikamaru",
  "state": "running",
  "health": "healthy",
  "uptime": 1532,
  "version": "0.3.0",
  "timestamp": "2026-07-08T10:30:00Z"
}
```

La fréquence sera définie dans la configuration.

## Birth message et Last Will

Lors de la connexion, Shikamaru publiera un message de naissance.

Topic :

```text
ohana/agent/shikamaru/availability
```

Payload :

```json
{
  "status": "online"
}
```

En cas de déconnexion inattendue, le broker publiera automatiquement le Last Will.

Payload :

```json
{
  "status": "offline"
}
```

Cela permettra à Home Assistant et aux autres services de détecter l’indisponibilité de Shikamaru.

## Reconnexion

Le runtime MQTT devra gérer les pertes de connexion.

La stratégie retenue est un backoff progressif :

```text
1s → 2s → 4s → 8s → 16s → 30s maximum
```

Après reconnexion, Shikamaru devra :

* republier son birth message ;
* restaurer ses abonnements ;
* reprendre le heartbeat ;
* signaler l’événement au dispatcher.

## Topics MQTT

Les topics suivront la convention Ohana existante.

Racine :

```text
ohana/agent/shikamaru/
```

Topics principaux :

```text
ohana/agent/shikamaru/status
ohana/agent/shikamaru/availability
ohana/agent/shikamaru/health
ohana/agent/shikamaru/events
ohana/agent/shikamaru/command
ohana/agent/shikamaru/logs
ohana/agent/shikamaru/metrics
```

## Configuration

La configuration MQTT devra permettre de définir :

```yaml
mqtt:
  enabled: true
  host: "localhost"
  port: 1883
  username: null
  password: null
  client_id: "shikamaru"
  base_topic: "ohana/agent/shikamaru"
  qos: 1
  retain: false
  heartbeat_interval_seconds: 30
  reconnect:
    enabled: true
    initial_delay_seconds: 1
    max_delay_seconds: 30
```

## Conséquences positives

Cette décision permet de :

* découpler Shikamaru de la bibliothèque MQTT utilisée ;
* faciliter les tests unitaires ;
* isoler les détails réseau ;
* garder une architecture événementielle propre ;
* préparer l’intégration Home Assistant ;
* standardiser les messages MQTT ;
* rendre les reconnexions explicites et testables.

## Conséquences négatives

Cette décision ajoute une couche d’abstraction supplémentaire.

Elle impose aussi de maintenir plusieurs composants :

* client ;
* publisher ;
* subscriber ;
* heartbeat ;
* reconnexion ;
* messages.

Cependant, cette complexité est acceptable car MQTT devient une capacité structurante de Shikamaru.

## Alternatives considérées

### Utiliser directement la bibliothèque MQTT dans Application

Rejeté.

Cela aurait couplé le cœur applicatif à une bibliothèque externe et rendu les tests plus difficiles.

### Laisser les plugins publier eux-mêmes en MQTT

Rejeté.

Cela aurait multiplié les conventions de publication et créé des dépendances directes entre plugins et broker MQTT.

### Centraliser uniquement la publication sans gérer la réception

Rejeté.

Shikamaru doit pouvoir recevoir des commandes et les transformer en événements internes.

## Décision finale

Shikamaru adopte une architecture MQTT dédiée appelée **MQTT Runtime**.

Cette architecture repose sur :

* `MQTTClient` comme façade principale ;
* `MQTTPublisher` pour les publications ;
* `MQTTSubscriber` pour les messages entrants ;
* `MQTTReconnectPolicy` pour les pertes de connexion ;
* `MQTTHeartbeatService` pour la publication périodique de l’état ;
* une intégration stricte avec le `Dispatcher`.

Cette décision devient la base de la **Phase 3 — MQTT Runtime**.

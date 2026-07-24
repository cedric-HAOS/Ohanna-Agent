# ADR-0014 — MQTT Transport Architecture

## Statut

Proposé

## Contexte

L’ADR-0013 a défini le **MQTT Runtime** de Shikamaru.

Ce runtime fournit :

* `MQTTClient` ;
* `MQTTPublisher` ;
* `MQTTSubscriber` ;
* `MQTTReconnectPolicy` ;
* `MQTTHeartbeatService` ;
* les modèles de messages MQTT.

Cette couche est volontairement indépendante de toute bibliothèque MQTT externe.

Cependant, pour communiquer réellement avec un broker MQTT, Shikamaru doit disposer d’un composant chargé de l’accès réseau concret.

Ce composant est appelé **MQTT Transport**.

## Décision

Shikamaru introduira une couche dédiée appelée **MQTT Transport**.

Le transport sera responsable de la communication effective avec le broker MQTT.

Le reste du runtime ne devra jamais manipuler directement la bibliothèque MQTT utilisée.

L’architecture retenue devient :

```text
Application
    │
    ▼
MQTTClient
    │
    ├── MQTTPublisher
    ├── MQTTSubscriber
    └── MQTTTransport
            │
            ▼
       Bibliothèque MQTT
            │
            ▼
        Broker MQTT
```

## Responsabilités

Le transport MQTT est responsable de :

* ouvrir la connexion réseau ;
* fermer la connexion réseau ;
* publier un message sérialisé ;
* s’abonner à un topic ;
* se désabonner d’un topic ;
* configurer le Last Will ;
* exposer l’état de connexion ;
* recevoir les messages bruts du broker ;
* transmettre les messages entrants au runtime.

## Non-responsabilités

Le transport MQTT ne doit pas :

* contenir de logique métier ;
* construire les messages de heartbeat ;
* connaître les événements applicatifs ;
* décider des commandes à exécuter ;
* exposer directement la bibliothèque MQTT au reste du noyau.

## Structure cible

```text
core/
└── mqtt/
    ├── transport.py
    ├── client.py
    ├── publisher.py
    ├── subscriber.py
    ├── reconnect.py
    ├── heartbeat.py
    └── messages.py
```

## API cible

Le transport exposera une API interne simple :

```python
class MQTTTransport:
    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def publish(
        self,
        topic: str,
        payload: str,
        *,
        qos: int,
        retain: bool,
    ) -> None: ...

    async def subscribe(self, topic: str) -> None: ...

    async def unsubscribe(self, topic: str) -> None: ...
```

## Last Will

Le Last Will sera représenté par un modèle dédié.

Exemple :

```python
MQTTLastWill(
    topic="ohana/agent/shikamaru/availability",
    payload='{"status": "offline"}',
    qos=1,
    retain=True,
)
```

Ce modèle permettra au transport concret de configurer proprement le broker lors de l’ouverture de connexion.

## Implémentation concrète

Une implémentation basée sur `paho-mqtt` pourra être ajoutée ensuite.

Elle devra rester encapsulée dans le transport.

Le reste du projet ne devra pas importer directement `paho.mqtt`.

## Conséquences positives

Cette décision permet de :

* conserver le découplage du runtime MQTT ;
* isoler la dépendance à une bibliothèque externe ;
* faciliter les tests sans broker réel ;
* préparer une implémentation Paho propre ;
* rendre le Last Will explicite ;
* séparer clairement protocole, transport et logique applicative.

## Conséquences négatives

Cette décision ajoute une couche supplémentaire.

Elle impose aussi de maintenir un contrat clair entre :

* le runtime MQTT ;
* le transport MQTT ;
* la future bibliothèque MQTT.

Cette complexité est acceptable car elle protège le cœur de Shikamaru contre les détails réseau.

## Alternatives considérées

### Utiliser directement Paho dans `MQTTClient`

Rejeté.

Cela aurait couplé la façade du runtime à une bibliothèque externe.

### Utiliser Paho directement dans `Publisher` et `Subscriber`

Rejeté.

Cela aurait dupliqué la logique de connexion et rendu les tests plus difficiles.

### Reporter le transport à l’intégration Home Assistant

Rejeté.

Le transport MQTT est une brique fondamentale du runtime et doit être stabilisé avant les intégrations applicatives.

## Décision finale

Shikamaru adopte une couche **MQTT Transport** dédiée.

Cette couche sera responsable de la communication réseau concrète avec le broker MQTT.

Elle restera isolée du reste de l’application et servira de point d’entrée unique pour une future implémentation basée sur `paho-mqtt`.

Cette décision prépare la suite de la Phase MQTT sans compromettre le découplage établi par l’ADR-0013.

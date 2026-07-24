# MQTT Runtime

## Objectif

Le **MQTT Runtime** est la couche de communication de Shikamaru.

Son rôle est de connecter le noyau de l'agent au reste de l'écosystème Ohana via le protocole MQTT, tout en maintenant un découplage strict entre les composants internes et la bibliothèque MQTT utilisée.

Le runtime MQTT constitue la frontière entre le monde réseau et le cœur applicatif.

---

# Principes

Le runtime MQTT respecte les principes suivants :

* séparation des responsabilités ;
* architecture événementielle ;
* découplage du broker MQTT ;
* indépendance vis-à-vis de la bibliothèque MQTT ;
* forte testabilité ;
* reconnexion automatique ;
* tolérance aux pannes.

Le reste du projet ne communique jamais directement avec le broker.

---

# Vue d'ensemble

```text
                   Application
                        │
                        ▼
                 MQTT Runtime
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  MQTTClient      MQTTPublisher   MQTTSubscriber
        │                               │
        │                               ▼
        │                         Dispatcher
        │                               │
        ▼                               ▼
     Broker MQTT                   Event Handlers
```

---

# Architecture

Le runtime MQTT est constitué des composants suivants :

```text
core/
└── mqtt/
    ├── __init__.py
    ├── client.py
    ├── publisher.py
    ├── subscriber.py
    ├── reconnect.py
    ├── heartbeat.py
    └── messages.py
```

Chaque composant possède une responsabilité unique.

---

# MQTTClient

Le `MQTTClient` est la façade publique du runtime.

Tous les services internes utilisent uniquement cette classe.

Il est responsable de :

* créer la connexion ;
* fermer la connexion ;
* déléguer les publications ;
* déléguer les abonnements ;
* exposer une API simple au reste de l'application.

API cible :

```python
class MQTTClient:

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def publish(
        self,
        topic: str,
        payload: object,
    ) -> None:
        ...

    async def subscribe(
        self,
        topic: str,
    ) -> None:
        ...

    async def unsubscribe(
        self,
        topic: str,
    ) -> None:
        ...
```

---

# MQTTPublisher

Le publisher est responsable de toutes les publications MQTT.

Il prend en charge :

* la sérialisation JSON ;
* le QoS ;
* le flag `retain` ;
* les métadonnées communes ;
* la publication vers le broker.

Le publisher ne connaît pas la logique métier.

Il publie uniquement des objets déjà construits.

---

# MQTTSubscriber

Le subscriber écoute les topics MQTT.

À chaque message reçu :

1. validation ;
2. désérialisation ;
3. création d'un événement interne ;
4. transmission au Dispatcher.

Flux :

```text
Broker
   │
   ▼
Subscriber
   │
   ▼
Event
   │
   ▼
Dispatcher
```

Le Subscriber ne déclenche jamais directement un traitement métier.

---

# MQTTReconnectPolicy

Ce composant gère les pertes de connexion.

Stratégie retenue :

```text
1 s

↓

2 s

↓

4 s

↓

8 s

↓

16 s

↓

30 s
```

Après reconnexion :

* restauration des abonnements ;
* publication du message de disponibilité ;
* redémarrage du heartbeat ;
* émission d'un événement interne.

---

# MQTTHeartbeatService

Le heartbeat informe les autres composants que Shikamaru est toujours actif.

Publication périodique :

```text
ohana/agent/shikamaru/status
```

Exemple :

```json
{
  "agent": "shikamaru",
  "state": "running",
  "health": "healthy",
  "uptime": 3600,
  "version": "0.3.0",
  "timestamp": "2026-07-08T10:30:00Z"
}
```

La fréquence est configurable.

---

# Availability

Deux messages spéciaux sont utilisés.

## Birth Message

Publié lors de la connexion.

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

---

## Last Will

Déclaré au broker dès l'ouverture de la connexion.

En cas de perte brutale :

```json
{
  "status": "offline"
}
```

Le broker publie automatiquement ce message.

---

# Intégration avec le Dispatcher

Tous les messages entrants deviennent des événements.

Exemple :

```text
MQTT

↓

Subscriber

↓

CommandReceivedEvent

↓

Dispatcher

↓

Handler
```

Cette approche garantit que toute la logique métier reste indépendante de MQTT.

---

# Intégration avec Application

Le cycle de vie est le suivant :

```text
Application.initialize()

↓

MQTTClient.connect()

↓

Subscriber.subscribe()

↓

Heartbeat.start()

↓

Application.run()
```

À l'arrêt :

```text
Application.stop()

↓

Heartbeat.stop()

↓

MQTTClient.disconnect()
```

---

# Topics

Tous les topics sont regroupés sous une racine unique.

```text
ohana/
└── agent/
    └── shikamaru/
        ├── availability
        ├── status
        ├── health
        ├── metrics
        ├── events
        ├── command
        └── logs
```

---

# Configuration

Le runtime MQTT est piloté par la configuration.

Exemple :

```yaml
mqtt:
  enabled: true
  host: localhost
  port: 1883

  username: null
  password: null

  client_id: shikamaru

  base_topic: ohana/agent/shikamaru

  qos: 1
  retain: false

  heartbeat_interval_seconds: 30

  reconnect:
    enabled: true
    initial_delay_seconds: 1
    max_delay_seconds: 30
```

---

# Cycle de vie

```text
          CREATED
              │
              ▼
        CONNECTING
              │
              ▼
         CONNECTED
              │
              ▼
      SUBSCRIPTIONS
              │
              ▼
      HEARTBEAT START
              │
              ▼
          RUNNING
              │
     ┌────────┴────────┐
     │                 │
     ▼                 ▼
 Connection Lost     Stop
     │                 │
     ▼                 ▼
 Reconnect         Disconnect
     │                 │
     └────────┬────────┘
              ▼
           STOPPED
```

---

# Gestion des erreurs

Le runtime MQTT ne doit jamais interrompre brutalement l'application.

Les erreurs sont classées en deux catégories.

## Erreurs récupérables

Exemples :

* broker indisponible ;
* perte réseau ;
* timeout ;
* refus temporaire de connexion.

Ces erreurs déclenchent une tentative de reconnexion.

---

## Erreurs non récupérables

Exemples :

* configuration invalide ;
* paramètres incohérents ;
* erreur interne irréversible.

Ces erreurs sont remontées au Dispatcher afin que le noyau décide de l'action à entreprendre.

---

# Principes de conception

Le runtime MQTT respecte les règles suivantes :

* une seule responsabilité par composant ;
* aucune logique métier dans le runtime ;
* aucun accès direct au broker depuis les services ;
* toutes les communications passent par `MQTTClient` ;
* tous les messages entrants deviennent des événements internes ;
* toutes les publications passent par `MQTTPublisher`.

---

# Bénéfices

Cette architecture apporte :

* une communication centralisée ;
* une meilleure testabilité ;
* un faible couplage ;
* une excellente évolutivité ;
* une intégration naturelle avec le Dispatcher ;
* une compatibilité avec les futurs plugins ;
* une base solide pour l'intégration de Home Assistant et des services Ohana.

Le MQTT Runtime constitue ainsi la passerelle officielle entre Shikamaru et le reste de l'écosystème.

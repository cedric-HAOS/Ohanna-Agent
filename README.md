# README.md

# Ohanna-Agent

> **Un noyau d'automatisation événementiel, modulaire et extensible, conçu pour orchestrer des agents intelligents via MQTT.**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Licence](https://img.shields.io/badge/Licence-MIT-green)
![Tests](https://img.shields.io/badge/Tests-156-success)
![Couverture](https://img.shields.io/badge/Architecture-Clean-success)
![MQTT](https://img.shields.io/badge/MQTT-v5-orange)

---

# Vision

**Ohanna-Agent** est un moteur logiciel destiné à piloter des agents autonomes.

Il ne cherche pas à être un assistant conversationnel, mais un **runtime générique** capable de :

* recevoir des événements,
* prendre des décisions,
* exécuter des commandes,
* communiquer avec d'autres agents,
* évoluer grâce à un système de plugins.

Le projet est pensé pour fonctionner aussi bien :

* sur Raspberry Pi,
* sur mini-PC,
* sur serveur,
* dans Docker,
* ou dans le Cloud.

L'objectif est de construire un **noyau robuste**, indépendant de toute intelligence artificielle particulière.

---

# Philosophie

Ohanna-Agent repose sur quelques principes simples :

* architecture claire
* faible couplage
* forte cohésion
* composants testables
* événements avant appels directs
* aucune dépendance métier dans le noyau
* plugins isolés
* configuration simple
* extensibilité maximale

Le cœur du projet ne contient volontairement aucune logique métier.

Toutes les fonctionnalités sont apportées par des composants spécialisés.

---

# État actuel du projet

## Sprint 0 — Documentation

✔ Terminé

* Vision
* Philosophie
* Architecture
* États
* MQTT
* Conventions
* Roadmap
* ADR-0001 à ADR-0006

---

## Sprint 1 — Core Runtime

✔ Terminé

Implémentation du noyau :

* Event Bus
* Dispatcher
* Registry
* Commandes
* Configuration
* Cycle de vie
* États
* Health
* Journalisation

ADR validées :

* ADR-0007
* ADR-0008
* ADR-0009
* ADR-0010

---

## Sprint 2 — Core Services

✔ Terminé

Ajouts :

* Services internes
* Cycle de vie complet
* Health Checks
* Diagnostics
* Architecture des services
* Refactoring du runtime

ADR validées :

* ADR-0011
* ADR-0012

---

## Sprint 3 — MQTT Runtime

✔ Terminé

Le runtime dispose désormais d'une couche MQTT complète.

Fonctionnalités :

* Client MQTT
* Reconnexion automatique
* Publication
* Souscription
* Dispatch des messages
* Événements MQTT
* Découplage du cœur
* Runtime entièrement événementiel

ADR validées :

* ADR-0013
* ADR-0014

---

# Avancement

| Élément       | Statut |
| ------------- | ------ |
| Architecture  | ✅      |
| Runtime       | ✅      |
| Event Bus     | ✅      |
| Dispatcher    | ✅      |
| Registry      | ✅      |
| Lifecycle     | ✅      |
| Configuration | ✅      |
| Services      | ✅      |
| MQTT Runtime  | ✅      |
| Plugins       | 🚧     |
| Scheduler     | 🚧     |
| API REST      | 🚧     |
| IA            | ⏳      |

---

# Architecture

```
                +----------------------+
                |      Application     |
                +----------+-----------+
                           |
                           v
                 +--------------------+
                 |     Dispatcher     |
                 +---------+----------+
                           |
            +--------------+--------------+
            |                             |
            v                             v
      EventBus                      CommandBus
            |                             |
            +--------------+--------------+
                           |
                           v
                    Service Registry
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
   Lifecycle          MQTT Runtime        Plugins
        |                  |                  |
        +------------------+------------------+
                           |
                           v
                     External Systems
```

---

# Structure du dépôt

```
ohanna-agent/

├── application.py
├── configuration.py
├── dispatcher.py
├── events.py
├── event.py
├── command.py
├── lifecycle.py
├── mqtt.py
├── registry.py
├── services.py
│
├── tests/
│
├── docs/
│   ├── ADR/
│   ├── CORE.md
│   ├── ROADMAP.md
│   └── ...
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Tests

Le projet est développé selon une approche **Test First**.

Chaque composant du runtime est couvert par des tests unitaires.

État actuel :

* **156 tests**
* Tous validés
* Ruff : OK
* Pytest : OK

Exécution :

```bash
ruff check .
pytest
```

---

# Installation

## Cloner

```bash
git clone https://github.com/<utilisateur>/Ohanna-Agent.git

cd Ohanna-Agent
```

---

## Créer un environnement virtuel

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

---

## Installer

```bash
pip install -e .

pip install -r requirements.txt
```

---

# Lancer les tests

```bash
pytest
```

---

# Vérification qualité

```bash
ruff check .

ruff format .
```

---

# Documentation

La documentation est disponible dans :

```
docs/
```

Elle contient notamment :

* Vision
* Philosophie
* Architecture
* États
* MQTT
* Conventions
* ADR
* CORE
* ROADMAP

---

# Architecture documentaire

```
docs/

├── ADR/
│
├── Architecture-Logicielle.md
├── Capacites.md
├── Commandes.md
├── Configuration.md
├── CORE.md
├── Etats.md
├── MQTT.md
├── MQTT-Convention.md
├── Message-Model.md
├── Philosophie.md
├── Plugins.md
└── ROADMAP.md
```

---

# ADR

Les décisions d'architecture sont documentées dans :

```
docs/ADR/
```

Décisions validées :

* ADR-0001
* ADR-0002
* ADR-0003
* ADR-0004
* ADR-0005
* ADR-0006
* ADR-0007
* ADR-0008
* ADR-0009
* ADR-0010
* ADR-0011
* ADR-0012
* ADR-0013
* ADR-0014

Chaque ADR est immuable une fois validée.

---

# Feuille de route

## Sprint 0

Documentation

✅ terminé

---

## Sprint 1

Core Runtime

✅ terminé

---

## Sprint 2

Core Services

✅ terminé

---

## Sprint 3

MQTT Runtime

✅ terminé

---

## Sprint 4

Plugins

Prévu :

* Plugin Manager
* Chargement dynamique
* Cycle de vie des plugins
* Isolation
* Découverte automatique
* Dépendances

---

## Sprint 5

Scheduler

Prévu :

* tâches planifiées
* timers
* cron
* événements différés

---

## Sprint 6

Persistance

Prévu :

* stockage
* snapshots
* restauration

---

## Sprint 7

API

Prévu :

* REST
* WebSocket
* supervision

---

## Sprint 8

Observabilité

Prévu :

* métriques
* traces
* Prometheus
* OpenTelemetry

---

## Sprint 9

Intelligence

Prévu :

* agents IA
* outils
* mémoire
* orchestration

---

# Pourquoi "Ohanna" ?

Le nom **Ohanna** représente l'idée d'un ensemble d'agents coopérant au sein d'un même écosystème.

Chaque agent possède une responsabilité claire, communique par événements et contribue au fonctionnement global sans dépendre directement des autres.

Le noyau garantit cette coordination grâce à une architecture modulaire, résiliente et extensible.

---

# Licence

Projet distribué sous licence **MIT**.

---

# Remerciements

Ohanna-Agent est développé avec une approche orientée qualité :

* architecture pilotée par les ADR ;
* développement incrémental par sprints ;
* tests automatisés à chaque étape ;
* documentation maintenue au même niveau d'exigence que le code.

L'objectif est de construire un runtime pérenne, fiable et facilement extensible, capable de servir de fondation à une nouvelle génération d'agents intelligents.

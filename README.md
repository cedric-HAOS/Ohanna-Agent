# Ohanna-Agent

> **Shikamaru** — Un framework Python modulaire, événementiel et résilient pour les services d'infrastructure.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-204%20passed-success.svg)
![Ruff](https://img.shields.io/badge/ruff-clean-success.svg)
![Architecture](https://img.shields.io/badge/architecture-event--driven-blue.svg)
![MQTT](https://img.shields.io/badge/MQTT-native-orange.svg)
![Health](https://img.shields.io/badge/Health-Self--Healing-success.svg)

---

# Présentation

Ohanna-Agent est un framework Python permettant de développer des agents autonomes destinés à administrer des services d'infrastructure.

L'objectif du projet est de proposer un noyau logiciel robuste, modulaire et entièrement piloté par les événements.

Le noyau, baptisé **Shikamaru**, fournit toutes les briques communes :

- cycle de vie de l'application ;
- bus d'événements ;
- système de commandes ;
- client MQTT ;
- gestion des plugins ;
- supervision interne ;
- surveillance de santé ;
- moteur de récupération automatique.

Les services métier (DNS, DHCP, NTP, supervision, Home Assistant, etc.) sont développés sous forme de plugins indépendants.

---

# Philosophie

Ohanna-Agent repose sur plusieurs principes fondamentaux.

## Simplicité

Chaque composant possède une responsabilité unique.

Le code doit rester lisible, testable et facilement maintenable.

---

## Architecture événementielle

Les composants communiquent exclusivement au travers d'événements.

Aucun composant ne dépend directement d'un autre lorsqu'un échange peut être réalisé via le bus d'événements.

---

## Modularité

Toutes les fonctionnalités métier sont implémentées sous forme de plugins.

Le noyau reste indépendant des services exécutés.

---

## Résilience

L'agent surveille son propre état de santé.

En cas de problème, il tente automatiquement de récupérer le composant défaillant avant de passer en mode dégradé.

---

## Testabilité

Chaque composant doit être facilement testable.

Les dépendances sont injectées.

Le code métier reste indépendant des couches techniques.

---

# Fonctionnalités

## Noyau

- Cycle de vie complet de l'application
- Gestion centralisée de la configuration
- Bus d'événements
- Commandes internes
- Gestionnaire de plugins
- Services partagés
- Journalisation
- Ordonnanceur interne

---

## MQTT

- Client MQTT natif
- Publication d'événements
- Souscription aux commandes
- Reconnexion automatique
- Transport indépendant
- Messages typés

---

## Supervision

- Health Monitor
- Heartbeat
- Watchdog
- Agrégation de l'état de santé
- Détection des anomalies

---

## Auto-réparation

- Recovery Engine
- Recovery Strategy
- Recovery Policy
- Historique des récupérations
- Prévention des récupérations concurrentes
- Mode dégradé

---

# Architecture générale

```text
                    Plugins
                        │
                        ▼
                 Event Dispatcher
                        │
                        ▼
                  Event Bus
                        │
                        ▼
                  Application
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 Configuration       Scheduler        MQTT Client
      │                                   │
      ▼                                   ▼
 Services                        Publisher / Subscriber

                        ▼
                 Health Monitor
                        │
                Heartbeat / Watchdog
                        │
                        ▼
                Recovery Engine
                        │
                        ▼
                Recovery Policy
                        │
                        ▼
               Recovery Strategy
                        │
                        ▼
                Recovery Action
```

---

# Structure du projet

```text
ohanna-agent/

├── configuration/
├── core/
├── events/
├── health/
├── mqtt/
├── plugins/
├── recovery/
├── services/
├── tests/
├── docs/
├── config/
└── application.py
```

---

# Package Health

Le package **health** est chargé de la supervision interne.

```text
health/

heartbeat.py
monitor.py
watchdog.py
```

Responsabilités :

- surveiller les composants ;
- agréger leur état ;
- détecter les anomalies ;
- publier les informations de santé.

Le Health Monitor ne réalise aucune récupération.

---

# Package Recovery

Le package **recovery** implémente le moteur d'auto-réparation.

```text
recovery/

action.py
engine.py
policy.py
result.py
strategy.py
```

Chaque composant possède une responsabilité clairement définie.

---

# Architecture logicielle

L'architecture d'Ohanna-Agent est organisée en couches indépendantes.

```text
                    Plugins
                        │
                        ▼
                 Event Dispatcher
                        │
                        ▼
                   Event Bus
                        │
                        ▼
                  Application
                        │
    ┌───────────────┬───────────────┬───────────────┐
    ▼               ▼               ▼               ▼
Configuration     Services      MQTT Runtime     Scheduler
                                        │
                           ┌────────────┴────────────┐
                           ▼                         ▼
                     Publisher                Subscriber

                        ▼
                 Health Monitor
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      Health Checks           Watchdogs
                                      │
                                      ▼
                                 Heartbeats

                        ▼
                 Recovery Engine
                        │
                        ▼
                 Recovery Policy
                        │
                        ▼
                Recovery Strategy
                        │
                        ▼
                 Recovery Action
```

L'ensemble du framework repose sur un faible couplage entre les composants.

---

# Cycle de vie de l'application

L'application suit un cycle de vie strict.

```text
CREATED
    │
    ▼
INITIALIZING
    │
    ▼
READY
    │
    ▼
RUNNING
    │
    ▼
STOPPING
    │
    ▼
STOPPED
```

En cas d'erreur irrécupérable :

```text
RUNNING
    │
    ▼
ERROR
```

Toutes les transitions sont centralisées dans le `LifecycleManager`.

---

# Architecture événementielle

Les composants communiquent uniquement via des événements.

```text
Plugin

↓

Dispatcher

↓

Event Bus

↓

Subscribers
```

Cette approche permet :

- un faible couplage ;
- une excellente testabilité ;
- l'ajout de nouveaux plugins sans modifier le noyau.

---

# Runtime MQTT

Le runtime MQTT constitue l'interface principale entre Shikamaru et le reste du système.

```text
Commande MQTT

↓

Subscriber

↓

Dispatcher

↓

Command

↓

Services

↓

Event

↓

Publisher

↓

MQTT
```

Les échanges sont entièrement typés.

Le noyau reste indépendant de l'implémentation du broker MQTT.

---

# Gestion des plugins

Les plugins sont chargés dynamiquement.

Chaque plugin possède son propre cycle de vie.

```text
Plugin

↓

Initialize()

↓

Run()

↓

Stop()
```

Les plugins n'ont pas connaissance des autres plugins.

Ils communiquent uniquement via :

- le Dispatcher ;
- les événements ;
- les services exposés par l'application.

---

# Supervision

La supervision est assurée par le package `health`.

## Health Monitor

Le Health Monitor centralise tous les contrôles de santé.

```text
Health Check

↓

Health Monitor

↓

Health Result

↓

Health Status
```

Il calcule un état global :

- HEALTHY
- DEGRADED
- UNHEALTHY
- UNKNOWN

---

## Heartbeat

Un Heartbeat indique qu'un composant est toujours actif.

Exemples :

```text
application.main_loop

plugin.dns

plugin.dhcp

mqtt.runtime
```

Chaque heartbeat est horodaté.

---

## Watchdog

Chaque Watchdog surveille une source.

```text
Heartbeat

↓

Watchdog

↓

HealthResult
```

En cas d'absence de heartbeat :

```text
UNKNOWN

↓

DEGRADED

↓

UNHEALTHY
```

Le Watchdog ne redémarre jamais un composant.

Il ne fait que signaler son état.

---

# Auto-réparation

Le package `recovery` implémente le moteur d'auto-réparation.

Son architecture suit les ADR-0017 à ADR-0019.

```text
HealthResult

↓

Recovery Engine

↓

Recovery Policy

↓

Recovery Strategy

↓

Recovery Action

↓

Recovery Result
```

---

## Recovery Engine

Le Recovery Engine orchestre les opérations de récupération.

Il est responsable de :

- sélectionner une stratégie ;
- empêcher les récupérations concurrentes ;
- conserver l'historique ;
- exécuter les actions.

Il ne contient aucune logique métier.

---

## Recovery Policy

Une Policy décide :

- quelles actions exécuter ;
- dans quel ordre ;
- combien de tentatives effectuer ;
- quand abandonner.

Elle ne réalise aucune action.

---

## Recovery Strategy

Une Strategy associe une anomalie à une action concrète.

Exemples futurs :

- DNSRecoveryStrategy
- DHCPRecoveryStrategy
- MQTTRecoveryStrategy
- HomeAssistantRecoveryStrategy

Chaque stratégie est indépendante.

---

## Recovery Action

Une Action représente une opération élémentaire.

Exemples :

- restart
- reconnect
- reload
- disable

Les actions pourront être enrichies dans les prochains sprints.

---

# Mode dégradé

Lorsque toutes les tentatives de récupération échouent, Shikamaru peut continuer à fonctionner en mode dégradé.

```text
HEALTHY

↓

DEGRADED

↓

UNHEALTHY
```

L'objectif est de conserver le maximum de fonctionnalités disponibles.

Le retour à un état normal est automatique dès que les contrôles de santé redeviennent positifs.

---

# Installation

## Prérequis

- Python 3.13 ou supérieur
- Git
- MQTT Broker (Mosquitto recommandé)
- Ruff
- Pytest

---

## Cloner le dépôt

```bash
git clone https://github.com/<utilisateur>/Ohanna-Agent.git

cd Ohanna-Agent
```

---

## Créer un environnement virtuel

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Installer les dépendances

```bash
pip install -r requirements.txt
```

ou

```bash
pip install -e .
```

---

# Lancement

```bash
python application.py
```

Le fichier de configuration est chargé automatiquement.

---

# Configuration

Les paramètres de l'application sont regroupés dans le package :

```text
configuration/
```

Ils couvrent notamment :

- Agent
- MQTT
- Logging
- Health
- Plugins

Le chargement repose sur Pydantic afin de garantir une validation forte de la configuration.

---

# Développement

Le projet suit les recommandations modernes de Python.

## Style

- Python 3.13
- Type Hints
- Dataclasses
- Protocols
- Enum
- Ruff
- Pytest

---

## Vérification du style

```bash
ruff check .
```

---

## Lancement des tests

```bash
pytest
```

---

## Résultat actuel

```text
204 tests
204 réussis
0 échec
```

---

# Architecture des packages

```text
configuration/
```

Gestion de toute la configuration.

---

```text
core/
```

Noyau de Shikamaru.

Gestion du cycle de vie.

---

```text
events/
```

Bus d'événements.

Dispatcher.

Messages.

Commandes.

---

```text
mqtt/
```

Runtime MQTT.

Publisher.

Subscriber.

Reconnect.

Transport.

---

```text
health/
```

Supervision.

Heartbeat.

Watchdog.

Health Monitor.

---

```text
recovery/
```

Auto-réparation.

Recovery Engine.

Strategies.

Policies.

Actions.

---

```text
plugins/
```

Chargement dynamique des plugins.

---

```text
services/
```

Services internes exposés aux plugins.

---

# Tests

L'ensemble du framework est couvert par des tests unitaires.

```text
tests/

application

configuration

dispatcher

events

mqtt

plugins

health

recovery

scheduler

services

transport
```

Chaque nouvelle fonctionnalité doit être accompagnée de ses tests.

Le projet applique une politique stricte :

> Aucune nouvelle fonctionnalité sans tests.

---

# Décisions d'architecture

Toutes les décisions importantes sont documentées dans les ADR.

À ce jour :

```text
ADR-0001
Lifecycle

ADR-0002
Application

ADR-0003
Dispatcher

ADR-0004
Transitions

ADR-0005
Configuration

ADR-0006
Architecture Core

ADR-0007
...

ADR-0014
MQTT Runtime

ADR-0015
Health Monitor

ADR-0016
Heartbeat & Watchdog

ADR-0017
Recovery Engine

ADR-0018
Recovery Policies

ADR-0019
Mode dégradé
```

Chaque ADR est considérée comme contractuelle.

Le code doit rester conforme aux décisions qui y sont décrites.

---

# Documentation

Le dépôt contient une documentation complète :

```text
docs/

Architecture

ADR

Roadmap

Philosophie

Capacités

Conventions MQTT

Message Model

Configuration

Plugins
```

Chaque Sprint met à jour :

- README.md
- ROADMAP.md
- CHANGELOG.md
- CORE.md

afin que la documentation reflète toujours fidèlement l'état réel du projet.

---

# Objectifs

Les objectifs à long terme d'Ohanna-Agent sont :

- fournir un framework générique pour les services d'infrastructure ;
- garantir un fonctionnement autonome et résilient ;
- simplifier le développement de nouveaux plugins ;
- proposer une architecture moderne, testable et évolutive.

Le projet privilégie la robustesse et la maintenabilité plutôt que l'ajout rapide de fonctionnalités.

---

# État du projet

## Version actuelle

**Version : 4.0**

Statut :

> Sprint 4 terminé

Le noyau Shikamaru dispose désormais :

- d'un runtime MQTT complet ;
- d'un système de supervision interne ;
- d'un moteur d'auto-réparation ;
- d'une architecture modulaire ;
- d'une base de tests robuste.

Le projet est prêt à accueillir les premiers plugins d'infrastructure.

---

# Avancement

| Sprint | Description | État |
|----------|-------------|------|
| Sprint 0 | Architecture & Documentation | ✅ Terminé |
| Sprint 1 | Foundation | ✅ Terminé |
| Sprint 2 | Core Services | ✅ Terminé |
| Sprint 3 | Runtime MQTT | ✅ Terminé |
| Sprint 4 | Health & Recovery | ✅ Terminé |
| Sprint 5 | Plugins Infrastructure | 🚧 À venir |

---

# Roadmap

## Sprint 5

Développement des premiers plugins :

- DNS
- DHCP
- NTP
- Supervision
- Découverte réseau

---

## Sprint 6

Intégration Home Assistant

- Auto Discovery MQTT
- Entités
- Services
- Diagnostics

---

## Sprint 7

Interface Web

Objectifs :

- tableau de bord
- état des plugins
- santé du système
- historique des événements
- récupération manuelle
- visualisation des métriques

---

## Sprint 8

Supervision avancée

- métriques
- statistiques
- monitoring
- alertes
- historique
- tableaux de bord

---

## Sprint 9

Haute disponibilité

Objectifs :

- réplication
- clustering
- agents distribués
- tolérance aux pannes
- synchronisation

---

# Statistiques

À la fin du Sprint 4 :

```text
Python 3.13

204 tests unitaires

0 test en échec

Ruff
100 % conforme

Architecture
100 % événementielle

MQTT
Natif

Health Monitor
Implémenté

Heartbeat
Implémenté

Watchdog
Implémenté

Recovery Engine
Implémenté

Recovery Strategy
Implémentée

Recovery Policy
Implémentée

Mode dégradé
Implémenté
```

---

# Principes de qualité

Chaque évolution du projet respecte les règles suivantes :

- architecture guidée par les ADR ;
- couverture systématique par des tests unitaires ;
- faible couplage entre les composants ;
- séparation stricte des responsabilités ;
- injection des dépendances ;
- API stables ;
- documentation synchronisée avec le code.

---

# Contribuer

Les contributions sont les bienvenues.

Avant toute Pull Request :

1. vérifier le style :

```bash
ruff check .
```

2. lancer les tests :

```bash
pytest
```

Aucune Pull Request ne doit introduire de régression.

Les nouvelles fonctionnalités doivent être :

- documentées ;
- testées ;
- conformes aux ADR existantes.

---

# Licence

Ce projet est distribué sous licence **MIT**.

Voir le fichier `LICENSE`.

---

# Remerciements

Merci à tous ceux qui participent au développement d'Ohanna-Agent.

Le projet est construit progressivement, Sprint après Sprint, avec une attention particulière portée à :

- la qualité du code ;
- la stabilité ;
- la testabilité ;
- la documentation ;
- l'évolutivité.

---

# Pourquoi "Shikamaru" ?

Le noyau d'Ohanna-Agent porte le nom **Shikamaru** en référence au personnage du manga *Naruto*.

Shikamaru est reconnu pour :

- sa capacité d'analyse ;
- son sens de l'anticipation ;
- sa stratégie ;
- son calme face aux problèmes ;
- sa capacité à trouver la meilleure solution avec un minimum d'actions.

Ces qualités représentent parfaitement la philosophie du projet :

> **Observer. Comprendre. Décider. Agir.**

---

# Vision

À terme, Ohanna-Agent ambitionne de devenir un framework générique permettant de développer des agents d'infrastructure autonomes, capables de :

- superviser leur environnement ;
- détecter les anomalies ;
- s'auto-réparer ;
- communiquer par événements ;
- s'intégrer naturellement dans un écosystème Home Assistant ou MQTT.

Le projet privilégie une architecture durable, modulaire et maintenable plutôt qu'une accumulation rapide de fonctionnalités.

---

**Ohanna-Agent** est un projet conçu avec une conviction simple :

> *Un bon agent n'est pas seulement capable d'exécuter des tâches. Il doit aussi être capable de comprendre son état, de s'adapter aux incidents et de continuer à rendre le meilleur service possible.*

# Ohanna-Agent

> Garantir les capacités d'une infrastructure, plutôt que simplement surveiller ses équipements.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Tests](https://img.shields.io/badge/tests-706-success)
![License](https://img.shields.io/badge/license-MIT-green)

---

# Vision

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités sont garanties dans le temps.

Les machines tombent en panne.

Les logiciels évoluent.

Les configurations dérivent.

Les dépendances changent.

Pourtant, les services attendus doivent continuer à fonctionner.

Ohanna-Agent est né de cette idée.

Sa mission n'est pas de superviser des serveurs.

Sa mission est de garantir les capacités décrites par l'architecture de référence d'Ohanna-House.

---

# Philosophie

Ohanna-Agent ne surveille pas des machines.

Il surveille des **capacités**.

Par exemple :

- Résolution DNS
- Distribution DHCP
- Broker MQTT
- Home Assistant
- Sauvegardes
- Synchronisation NTP
- Accès Internet
- API REST
- Stockage

Chaque capacité est calculée à partir d'observations réalisées par des plugins indépendants.

---

# Architecture

Aujourd'hui, Ohanna-Agent est organisé autour de plusieurs sous-systèmes indépendants.

```
                 Scheduler
                      │
                      ▼
       SchedulerObservationHandler
                      │
                      ▼
           ObservationManager
                      │
                      ▼
         InfrastructureRuntime
                      │
       ┌──────────────┴──────────────┐
       ▼                             ▼
 NodeRuntime                 ServiceRuntime
       │                             │
       └──────────────┬──────────────┘
                      ▼
 InfrastructureCapabilityCalculator
                      │
                      ▼
          InfrastructureCapability
```

Cette architecture sépare clairement :

- la description de l'infrastructure ;
- son état courant ;
- les observations ;
- les capacités calculées.

---

# Fonctionnalités

## Core

- Cycle de vie de l'application
- Gestion de configuration
- Journalisation
- Dispatcher de commandes
- EventBus
- Scheduler
- Gestion mémoire

## Plugins

- Architecture extensible
- Découverte automatique
- Runtime indépendant
- États des plugins
- Cycle de vie

## Infrastructure

- Modèle Infrastructure
- Node
- Service
- Endpoint
- Runtime Infrastructure
- Observations
- Capacités calculées

## Qualité

- Typage complet
- Ruff
- Pytest
- Architecture modulaire
- Forte couverture de tests

---

# Structure du projet

```
application/
capabilities/
configuration/
core/
dispatcher/
events/
health/
infrastructure/
memory/
mqtt/
plugins/
scheduler/
scripts/
tests/
```

---

# Exemple

Création d'une infrastructure :

```python
from infrastructure import (
    Infrastructure,
    Node,
    Service,
    ServiceType,
)

infra = Infrastructure(name="Ohanna")

node = Node(name="INFRA-01")

node.add_service(
    Service(
        name="DNS",
        type=ServiceType.DNS,
    )
)

infra.add_node(node)
```

Création du Runtime :

```python
runtime = InfrastructureRuntime.from_infrastructure(infra)
```

Calcul d'une capacité :

```python
calculator = InfrastructureCapabilityCalculator(runtime)

dns = calculator.calculate_dns_available()

print(dns.available)
```

---

# Démonstration

Une démonstration est disponible :

```
python -m scripts.show_infrastructure_status
```

Exemple :

```
OHANNA INFRASTRUCTURE STATUS

❔ INFRA-01

   ✅ DNS
   ❌ MQTT

⚠️ HA-01

   ❔ Home Assistant

CALCULATED CAPABILITIES

✅ dns_available
❌ mqtt_available
```

---

# Tests

```
ruff check .
pytest
```

Version actuelle :

```
706 tests
```

---

# Roadmap

## Phase 1

- ✅ Core
- ✅ Scheduler
- ✅ EventBus
- ✅ Plugins
- ✅ Runtime
- ✅ Memory

## Phase 2

- ✅ Infrastructure
- ✅ Runtime Infrastructure
- ✅ Observation Engine
- ✅ Capacités calculées

## Phase 3

- Infrastructure déclarative
- Loader YAML
- Dépendances entre services
- Calculs avancés des capacités

## Phase 4

- Tableau de bord Web

## Phase 5

- Intégration Home Assistant

---

# Documentation

La documentation complète est disponible dans :

```
docs/
```

Elle comprend notamment :

- Architecture
- ADR
- Roadmap
- Philosophie
- Capacités
- Plugins
- MQTT
- Configuration

---

# État du projet

Version actuelle :

**v0.10.0**

Sprint terminé :

**Sprint 13 — Infrastructure Runtime**

706 tests unitaires.

Architecture stable.

Prêt pour le Sprint 14.
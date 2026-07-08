# Ohanna-Agent

> Un framework Python moderne pour construire des agents autonomes, modulaires et événementiels.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/tests-422-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-v0.8.0-orange)

---

# Présentation

Ohanna-Agent est un framework Python permettant de développer des agents intelligents, extensibles et pilotés par événements.

Le projet privilégie :

- une architecture modulaire ;
- un faible couplage entre les composants ;
- une forte testabilité ;
- une documentation orientée architecture (ADR) ;
- une évolution incrémentale guidée par les tests.

Chaque fonctionnalité majeure est introduite par un sprint dédié et validée par une architecture documentée.

---

# Philosophie

Les principes fondateurs sont :

- **Simplicité**
- **Composition plutôt qu'héritage**
- **Injection de dépendances**
- **Événementiel**
- **Typage fort**
- **Testabilité**
- **Architecture évolutive**
- **Documentation avant implémentation**

---

# Fonctionnalités actuelles

## Cycle de vie

- États applicatifs
- Gestion du lifecycle
- États typés

---

## Dispatcher

- Routage des commandes
- Découplage Command / Handler
- Exécution centralisée

---

## Bus d'événements

- Publication d'événements
- Souscription
- Diffusion interne

---

## Services

- Registre de services
- Injection de dépendances
- Résolution centralisée

---

## Plugins

- Gestionnaire de plugins
- Architecture extensible
- Chargement dynamique

---

## Scheduler

- Planification de tâches
- Exécution périodique
- DispatcherTaskExecutor
- Runtime Scheduler

---

## Capacités

- Gestion des capacités
- Activation / désactivation
- Découverte des capacités

---

## Mémoire (Sprint 7)

Le framework dispose désormais d'un système mémoire complet.

### Runtime Memory

Mémoire volatile.

### Session Memory

Mémoire de session.

### Persistent Memory

Mémoire persistante.

### Memory Manager

Façade unique permettant de manipuler l'ensemble des mémoires.

### Memory Storage

Persistance JSON.

### Memory Serializer

Sérialisation indépendante du backend.

### Memory Statistics

Statistiques d'utilisation :

- hits
- misses
- sets
- deletes
- saves
- loads

---

# Architecture

```text
Application
│
├── CommandDispatcher
├── EventBus
├── ServiceRegistry
├── PluginManager
├── Scheduler
└── MemoryManager
      │
      ├── RuntimeMemory
      ├── SessionMemory
      └── PersistentMemory
              │
              ▼
        MemoryStorage
              │
              ▼
      MemorySerializer
```

---

# Structure du projet

```text
application.py

core/
    dispatcher/
    events/
    plugins/
    services/

memory/
    memory_entry.py
    memory_manager.py
    memory_scope.py
    memory_serializer.py
    memory_statistics.py
    memory_storage.py
    persistent_memory.py
    runtime_memory.py
    session_memory.py

scheduler/

tests/

docs/
    adr/
    architecture/
```

---

# Installation

```bash
git clone https://github.com/<user>/Ohanna-Agent.git

cd Ohanna-Agent

python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Installation :

```bash
pip install -e .
```

---

# Tests

L'ensemble du projet est validé par une suite de tests automatisés.

```bash
pytest
```

État actuel :

- **422 tests**
- **100 % des tests validés**

---

# Documentation

La documentation est organisée autour de plusieurs documents :

- README.md
- ROADMAP.md
- CHANGELOG.md
- docs/Architecture/CORE.md
- docs/adr/

Les décisions d'architecture sont documentées sous forme d'ADR.

---

# Roadmap

Les prochaines évolutions concernent notamment :

- Workflows
- Pipelines
- SDK Plugins
- Moteur de raisonnement
- Observabilité
- Monitoring
- IA

Voir :

```
ROADMAP.md
```

---

# Qualité

Le projet suit une démarche de développement incrémentale :

- Architecture avant implémentation
- ADR systématiques
- Tests avant validation
- Revue de sprint
- Refactoring continu

---

# Version actuelle

**v0.8.0**

- Sprint 0 : Architecture
- Sprint 1 : Lifecycle
- Sprint 2 : Core Services
- Sprint 3 : MQTT Runtime
- Sprint 4 : Auto-réparation
- Sprint 5 : Capacités
- Sprint 6 : Scheduler
- Sprint 7 : Memory

---

# Licence

MIT License.
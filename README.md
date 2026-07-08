# Shikamaru

**Shikamaru** est le noyau logiciel d'**Ohanna-Agent**.

Son objectif est de fournir une plateforme légère, modulaire et orientée événements permettant de développer des agents autonomes dédiés à l'administration et à la supervision d'infrastructures.

Le projet privilégie une architecture simple, fortement testée et indépendante de tout framework externe.

---

# Objectifs

Shikamaru fournit les services fondamentaux nécessaires à tous les agents :

* gestion du cycle de vie de l'application ;
* gestion centralisée de la configuration ;
* registre des services ;
* communication par événements ;
* traitement des commandes ;
* planification des tâches ;
* gestion des plugins ;
* supervision interne ;
* intégration MQTT ;
* extensibilité par composants.

---

# Philosophie

Le noyau repose sur plusieurs principes :

* une responsabilité unique par composant ;
* un faible couplage entre les modules ;
* une architecture orientée événements ;
* des dépendances explicites ;
* des composants facilement testables ;
* aucune dépendance inutile envers des frameworks externes.

---

# Architecture

```text
                           Application
                                 │
               ┌─────────────────┴─────────────────┐
               │                                   │
        Service Registry                   Core Runtime
               │                                   │
               ├───────────────┬───────────────────┤
               │               │                   │
           EventBus       Scheduler       CommandDispatcher
               │               │                   │
               └───────────────┼───────────────────┘
                               │
                        PluginManager
                               │
                            Plugins
```

---

# Composants du noyau

## Application

Point d'entrée du noyau.

Responsable de :

* l'initialisation ;
* la création des services ;
* l'enregistrement des composants ;
* le démarrage ;
* l'arrêt propre.

---

## Lifecycle

Gestion du cycle de vie de l'application.

États :

* CREATED
* INITIALIZING
* READY
* RUNNING
* STOPPING
* STOPPED
* ERROR

---

## Configuration

Chargement de la configuration YAML.

Basée sur Pydantic.

---

## Service Registry

Point d'accès unique aux services internes.

Responsable de :

* l'enregistrement ;
* la recherche ;
* l'injection de dépendances.

---

## Event

Classe de base de tous les événements.

Chaque événement possède :

* un identifiant unique ;
* un horodatage UTC.

---

## Event Bus

Mécanisme de communication interne.

Les composants publient des événements sans connaître leurs destinataires.

---

## Command

Classe de base de toutes les commandes.

Chaque commande possède :

* un identifiant unique ;
* un horodatage UTC.

---

## Command Dispatcher

Point d'entrée unique pour toutes les commandes.

Responsable du routage des commandes vers leurs gestionnaires.

---

## Scheduler

Planifie les tâches périodiques du noyau.

Publie des événements lors de l'exécution des tâches.

---

## Plugin Manager

Gestion du cycle de vie des plugins.

États :

* REGISTERED
* INITIALIZED
* RUNNING
* STOPPED

---

## Health

Responsable de la supervision interne.

---

## MQTT

Interface de communication avec les systèmes externes.

L'implémentation complète sera réalisée lors d'une phase ultérieure.

---

# Organisation du projet

```text
src/
│
├── application.py
│
├── configuration/
│
├── core/
│   ├── command.py
│   ├── dispatcher.py
│   ├── event.py
│   ├── events.py
│   ├── lifecycle.py
│   ├── plugins.py
│   ├── scheduler.py
│   └── services.py
│
├── health/
│
├── logger/
│
└── mqtt/
```

---

# Tests

Le projet est développé selon une approche **Test First**.

Chaque composant possède ses propres tests unitaires.

À la fin de la Phase 2 :

* **76 tests unitaires**
* **100 % des tests réussis**
* **Ruff validé**

---

# Documentation

Le projet est documenté au travers :

* des ADR (Architecture Decision Records) ;
* de la documentation d'architecture ;
* de la roadmap ;
* des guides de développement.

---

# Roadmap

Le développement est organisé en plusieurs phases :

* Phase 0 — Fondation
* Phase 1 — Core Framework
* Phase 2 — Core Services
* Phase 3 — MQTT Runtime
* Phase 4 — DNS
* Phase 5 — DHCP
* Phase 6 — NTP
* Phase 7 — Supervision
* Phase 8 — Home Assistant
* Phase 9 — Interface Web

---

# État du projet

**Version :** Sprint 2

## Fondation

* ✅ Terminée

## Core Framework

* ✅ Terminé

## Core Services

* ✅ Terminé

## MQTT Runtime

* 🚧 À venir

---

# Licence

Ce projet est distribué sous licence MIT.

# Ohanna-Agent

> **Modular • Autonomous • Event-Driven • MQTT Native**

Ohanna-Agent est un framework Python open source destiné à la création d'agents autonomes, modulaires et pilotés par événements.

Conçu autour d'une architecture fortement découplée, il permet de construire des applications capables de recevoir, planifier, orchestrer et exécuter des actions tout en restant simples à tester, à maintenir et à faire évoluer.

Contrairement à un simple moteur MQTT ou à un système d'automatisation classique, Ohanna-Agent fournit un véritable noyau applicatif extensible, reposant sur des composants indépendants et des abstractions communes.

---

# Philosophie

Ohanna-Agent repose sur quelques principes fondamentaux qui guident l'ensemble de son architecture.

## Modularité

Chaque composant possède une responsabilité unique.

Les services du noyau peuvent évoluer indépendamment sans impacter les autres composants.

## Découplage

Les communications entre les différentes couches utilisent exclusivement des contrats clairement définis.

Aucun composant métier ne dépend directement d'une implémentation particulière.

## Testabilité

L'ensemble du framework est conçu pour être facilement testable.

Les abstractions (`Clock`, `Executor`, `Registry`, `Runtime`, etc.) permettent de produire des tests unitaires rapides, déterministes et indépendants du système d'exploitation.

## Évolutivité

Chaque nouveau service peut s'appuyer sur les abstractions du noyau sans modifier les composants existants.

Cette approche facilite l'ajout de nouvelles fonctionnalités tout en préservant la stabilité de l'architecture.

---

# Fonctionnalités

À la version **0.4.0**, Ohanna-Agent fournit notamment :

- Architecture orientée événements
- Dispatcher de commandes
- Gestionnaire de capacités (Capabilities)
- Runtime MQTT natif
- Bus d'événements
- Surveillance et auto-réparation
- Scheduler intégré
- Déclencheurs (Triggers)
- Planification de tâches
- Exécuteurs de tâches
- Runtime et statistiques des services
- Architecture orientée SOLID
- Plus de **315 tests unitaires**

---

# Architecture générale

Le noyau du framework est organisé autour de plusieurs services indépendants.

```text
Application
│
├── Configuration
├── Dispatcher
├── Scheduler
├── Capability Manager
├── MQTT Runtime
└── Event Bus
```

Chaque service possède sa propre responsabilité et communique avec les autres uniquement via des interfaces clairement définies.

Cette organisation permet d'ajouter de nouvelles fonctionnalités sans modifier les composants existants.

---

# Le Scheduler (v0.4.0)

La version **0.4.0** introduit le Scheduler, première brique permettant à Ohanna-Agent d'exécuter des actions de manière autonome.

Son architecture est volontairement découplée.

```text
                 Clock
                   │
                   ▼
             BaseTrigger
          ┌────────┼─────────┐
          ▼        ▼         ▼
     Interval   Cron    OneShot
          │
          ▼
        Task
          │
          ▼
    TaskRegistry
          │
          ▼
      Scheduler
          │
          ▼
     TaskExecutor
          │
          ▼
DispatcherTaskExecutor
          │
          ▼
      Dispatcher
          │
          ▼
        Command
          │
          ▼
         Action
```

Chaque composant possède une responsabilité unique.

Le Scheduler ne connaît jamais directement les Actions ou les Capacités.

Il orchestre simplement l'exécution de tâches planifiées.

---

# Le noyau

Le cœur d'Ohanna-Agent est construit autour d'abstractions communes.

```text
core/
│
├── Runtime
├── Statistics
├── Registry
└── Executor
```

Ces abstractions sont réutilisées par les différents services du framework afin d'assurer une architecture homogène et facilement extensible.

---

# Pourquoi Ohanna-Agent ?

Le projet poursuit plusieurs objectifs :

- fournir un noyau léger et modulaire ;
- favoriser le découplage entre les composants ;
- simplifier les tests unitaires ;
- permettre la planification de traitements autonomes ;
- faciliter le développement de nouveaux services ;
- proposer une architecture durable et maintenable.

Ohanna-Agent n'est pas uniquement un moteur MQTT.

C'est un framework destiné à construire des agents autonomes capables de recevoir des événements, de planifier leurs propres actions et d'orchestrer des traitements complexes tout en conservant une architecture claire et évolutive.

---

# Installation

## Prérequis

- Python **3.13** ou supérieur
- Git
- pip

Le projet est développé et testé principalement sous Python **3.13**, mais reste compatible avec les futures versions supportées.

---

## Cloner le dépôt

```bash
git clone https://github.com/<utilisateur>/Ohanna-Agent.git
cd Ohanna-Agent
```

---

## Installation

Installation en mode développement :

```bash
pip install -e .
```

Installation des dépendances de développement :

```bash
pip install -r requirements-dev.txt
```

---

## Vérification du code

Le projet utilise **Ruff** pour l'analyse statique.

```bash
ruff check .
```

---

## Exécution des tests

L'ensemble de la suite de tests peut être lancé avec :

```bash
pytest
```

État actuel :

- ✅ Plus de **315 tests unitaires**
- ✅ Exécution en moins d'une seconde
- ✅ Architecture entièrement testée

---

# Structure du projet

Le dépôt est organisé en plusieurs modules indépendants.

```text
Ohanna-Agent/

├── application.py
├── configuration.py
├── dispatcher.py
├── engine.py
│
├── core/
│
├── scheduler/
│
├── mqtt/
│
├── capabilities/
│
├── plugins/
│
├── docs/
│
├── tests/
│
└── pyproject.toml
```

---

## Le package Core

Le package **core** contient les abstractions communes utilisées par l'ensemble du framework.

```text
core/

Runtime

Statistics

Registry

Executor
```

Ces composants servent de fondation à tous les services du noyau.

---

## Le package Scheduler

Introduit avec la version **0.4.0**, le Scheduler permet à Ohanna-Agent d'exécuter automatiquement des traitements planifiés.

```text
scheduler/

Clock

Triggers

Task

TaskRegistry

TaskExecutor

DispatcherTaskExecutor

SchedulerRuntime

SchedulerStatistics

SchedulerState

Scheduler
```

L'ensemble est entièrement découplé du Dispatcher et facilement testable.

---

## Le Dispatcher

Le Dispatcher constitue le point central d'exécution des commandes.

Il reçoit les commandes provenant :

- du Runtime MQTT ;
- du Scheduler ;
- des Capacités ;
- des Plugins ;
- des futurs Workflows.

Toutes les commandes transitent par le Dispatcher avant d'être exécutées.

---

## Les Capacités

Les Capacités représentent les fonctionnalités métier du framework.

Chaque capacité est totalement indépendante des autres.

Exemples :

- Health
- Monitor
- Heartbeat
- Auto-Recovery
- Watchdog

De nouvelles capacités peuvent être ajoutées sans modifier le noyau.

---

## Les Plugins

Le système de plugins permet d'étendre Ohanna-Agent sans modifier le code principal.

Chaque plugin est chargé dynamiquement et respecte les contrats définis par le noyau.

---

# Qualité logicielle

La qualité du code constitue l'un des objectifs principaux du projet.

Le développement suit plusieurs principes :

- Architecture SOLID
- Séparation stricte des responsabilités
- Inversion des dépendances
- Composition plutôt qu'héritage
- Couplage faible
- Forte couverture de tests
- Documentation systématique

Chaque nouveau composant est accompagné de tests unitaires avant son intégration.

---

# Performances

L'ensemble du framework est conçu pour rester léger.

Au moment de la version **0.4.0** :

- plus de **315 tests**
- exécution complète en environ **0,4 seconde**
- aucune dépendance lourde
- architecture orientée composants

Ces performances permettent un développement rapide et un retour immédiat lors des phases de test.

---

# Exemple d'utilisation

Le Scheduler peut être utilisé pour planifier une tâche périodique.

```python
from datetime import timedelta

from scheduler import (
    IntervalTrigger,
    Scheduler,
    Task,
)

scheduler = Scheduler()

scheduler.add_task(
    Task(
        command="health.check",
        trigger=IntervalTrigger(timedelta(minutes=5)),
    )
)

scheduler.start()
scheduler.tick()
```

Le Scheduler détermine automatiquement les tâches arrivées à échéance puis les transmet au Dispatcher via un `TaskExecutor`.

---

# Compatibilité

Le projet est actuellement développé avec :

- Python 3.13
- Pytest
- Ruff

Le framework est conçu pour rester compatible avec les prochaines versions stables de Python.

---

# Objectifs de qualité

Chaque Sprint respecte plusieurs exigences :

- aucune régression
- tous les tests passent
- Ruff sans erreur
- architecture revue
- documentation mise à jour
- audit avant chaque release

Cette discipline permet de conserver une base de code stable tout au long du développement.

---

# Documentation

La documentation est organisée selon plusieurs niveaux afin de faciliter la découverte et la compréhension du framework.

| Document | Description |
|-----------|-------------|
| **README.md** | Présentation générale du projet |
| **docs/Architecture/CORE.md** | Architecture complète du noyau |
| **ROADMAP.md** | Vision du projet et évolutions prévues |
| **CHANGELOG.md** | Historique des versions |
| **docs/Architecture/ADR/** | Décisions d'architecture (Architecture Decision Records) |

Le README présente le projet.

Le document **CORE.md** constitue la référence technique principale.

Les ADR expliquent les choix architecturaux réalisés au cours du développement.

---

# Feuille de route

Les six premiers sprints ont permis de construire le noyau du framework.

## Version actuelle

✔ Architecture modulaire

✔ Dispatcher

✔ Runtime MQTT

✔ Event Bus

✔ Gestionnaire de Capacités

✔ Auto-réparation

✔ Scheduler

✔ Runtime unifié

✔ Registry

✔ Executor

✔ Plus de **315 tests unitaires**

---

## Prochaines versions

### v0.5

- Workflow Engine
- Dépendances entre tâches
- Conditions d'exécution
- Gestion des délais (Timeout)

### v0.6

- Rule Engine
- Moteur de décisions
- Conditions avancées
- Expressions

### v0.7

- Pipeline Engine
- Traitements séquentiels
- Traitements parallèles
- Reprise automatique

### v0.8

- Persistance
- Sauvegarde des tâches
- Historique
- Stockage SQLite

### v0.9

- API REST
- Supervision distante
- Administration
- Interface Web

### v1.0

Première version stable.

---

# Contribuer

Les contributions sont les bienvenues.

Avant toute Pull Request :

1. Vérifier que tous les tests passent.

```bash
pytest
```

2. Vérifier la qualité du code.

```bash
ruff check .
```

3. Respecter les conventions de codage du projet.

4. Ajouter les tests associés à toute nouvelle fonctionnalité.

5. Mettre à jour la documentation si nécessaire.

Chaque évolution importante fait également l'objet d'un ADR afin de conserver l'historique des décisions d'architecture.

---

# Philosophie du projet

Ohanna-Agent poursuit un objectif simple :

Construire un framework d'agents autonomes, modulaire, fortement découplé et simple à faire évoluer.

Le projet privilégie :

- la simplicité ;
- la lisibilité ;
- la testabilité ;
- la stabilité ;
- la maintenabilité.

Chaque nouveau composant est conçu pour remplir une responsabilité unique et s'intégrer naturellement dans l'architecture existante.

Cette philosophie guide l'ensemble des choix techniques du projet.

---

# État du projet

Version actuelle :

**v0.4.0 – Autonomous Core**

Le noyau est désormais considéré comme stable.

Les principaux services du framework sont en place :

- Dispatcher
- Scheduler
- MQTT Runtime
- Capability Manager
- Event Bus

Les prochains développements porteront principalement sur les moteurs intelligents construits au-dessus du noyau.

---

# Licence

Ce projet est distribué sous licence MIT.

Voir le fichier `LICENSE` pour plus d'informations.

---

# Remerciements

Ohanna-Agent est développé avec une attention particulière portée à l'architecture logicielle, à la qualité du code et à la maintenabilité.

Le projet s'inspire des meilleures pratiques de l'écosystème Python, de l'architecture orientée événements et des principes SOLID afin de proposer un framework moderne, robuste et durable.

---

# Conclusion

La version **0.4.0 – Autonomous Core** marque une étape importante dans l'évolution d'Ohanna-Agent.

Après six sprints de développement, le projet dispose désormais d'un noyau modulaire composé d'un Dispatcher, d'un Scheduler, d'un Runtime MQTT, d'un gestionnaire de capacités et d'un ensemble d'abstractions communes (`Runtime`, `Registry`, `Executor`, `Statistics`).

Cette architecture constitue une base solide pour les prochaines évolutions du framework, notamment les moteurs de workflows, de règles et de pipelines.

L'objectif reste inchangé :

> Construire un framework d'agents autonomes, modulaire, testable et durable.
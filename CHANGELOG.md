# Changelog

Toutes les évolutions notables du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le format suit les recommandations de **Keep a Changelog** et respecte autant que possible les principes du **Versioning Sémantique (SemVer)**.

---

# [0.4.0] - 2026-07-08

## Autonomous Core

Cette version marque une étape majeure dans l'évolution d'Ohanna-Agent.

Le projet passe d'un moteur orienté événements à un framework capable de planifier et d'orchestrer ses propres traitements.

Le noyau introduit une architecture complète de planification reposant sur un Scheduler modulaire et un ensemble de nouvelles abstractions communes.

---

## Added

### Scheduler

* Ajout du Scheduler.
* Gestion des tâches planifiées.
* Gestion du cycle de vie du Scheduler.
* Intégration du Scheduler Runtime.
* Intégration des statistiques du Scheduler.

### Triggers

Ajout des déclencheurs :

* BaseTrigger
* IntervalTrigger
* OneShotTrigger
* CronTrigger

### Task Model

Ajout de :

* Task
* TaskState
* Priorités
* Observabilité
* Statistiques d'exécution

### Task Registry

Ajout du :

* TaskRegistry

Le Scheduler ne manipule plus directement les collections de tâches.

### Task Executors

Ajout de :

* TaskExecutor
* DryRunTaskExecutor
* DispatcherTaskExecutor
* FailingTaskExecutor

L'exécution des tâches est désormais complètement découplée du Scheduler.

### Runtime Model

Ajout de :

* SchedulerRuntime
* SchedulerState
* SchedulerStatistics

Le Runtime devient responsable de l'état d'exécution du Scheduler.

### Core abstractions

Création du package :

```text
core/
```

Ajout des abstractions :

* Runtime
* Statistics
* Registry
* Executor

Ces composants constituent désormais le socle architectural du framework.

### Tests

Ajout de nombreux tests couvrant :

* Scheduler
* Triggers
* Task
* Runtime
* Registry
* Executor

Le projet atteint désormais plus de **315 tests unitaires**.

---

## Changed

### Architecture

Refactorisation importante du noyau.

Le Scheduler est désormais construit autour des composants suivants :

```text
Scheduler
│
├── Runtime
├── Registry
├── Executor
├── Clock
└── Task
```

### Responsabilités

Séparation stricte entre :

* planification ;
* stockage ;
* exécution ;
* état d'exécution.

### Runtime

Le Runtime devient un concept commun du framework.

Les nouveaux services sont encouragés à utiliser cette architecture.

### Documentation

Refonte complète de la documentation :

* README
* CORE
* ROADMAP
* ADR

---

## Fixed

* Diverses améliorations de cohérence interne.
* Harmonisation des responsabilités.
* Nettoyage de plusieurs dépendances internes.
* Amélioration de la lisibilité du Scheduler.
* Uniformisation des conventions d'architecture.

---

## Performance

* Plus de **315 tests unitaires**.
* Exécution complète de la suite de tests en environ **0,4 seconde**.
* Maintien d'une architecture légère et fortement découplée.

---

# [0.3.0] - 2026-07-08

## MQTT Runtime

### Added

* Runtime MQTT complet.
* Heartbeat.
* Monitor.
* Reconnexion automatique.
* Publisher.
* Subscriber.
* Watchdog.
* Auto-réparation.

### Changed

* Refonte de l'architecture MQTT.
* Stabilisation du Runtime.

---

# [0.2.0] - 2026-07-08

## Core Services

### Added

* Dispatcher.
* Dependency Graph.
* Configuration.
* Services principaux.
* Plugins.
* Gestionnaire de capacités.

---

# [0.1.0] - 2026-07-07

## Foundation

### Added

* Initialisation du projet.
* Architecture du Kernel.
* Dispatcher.
* MQTT.
* Documentation.
* ADR.
* Suite de tests initiale.

---

# Versions futures

Les évolutions prévues sont décrites dans le fichier **ROADMAP.md**.

---

# Références

* Semantic Versioning : https://semver.org/
* Keep a Changelog : https://keepachangelog.com/

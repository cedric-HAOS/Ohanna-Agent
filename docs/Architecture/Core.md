# Architecture du Kernel — Ohanna-Agent

## Version

**v0.9.0**

---

# Objectif

Le Kernel constitue le cœur d'Ohanna-Agent.

Il fournit une architecture modulaire permettant de construire des agents intelligents robustes, extensibles et fortement découplés.

Le Kernel ne contient aucune logique métier. Il fournit uniquement les mécanismes nécessaires à l'orchestration des composants.

---

# Principes d'architecture

Le Kernel repose sur plusieurs principes fondamentaux :

* responsabilité unique ;
* faible couplage ;
* forte cohésion ;
* injection de dépendances ;
* architecture événementielle ;
* composants facilement testables ;
* interfaces minimales.

Chaque composant possède une responsabilité clairement définie et peut évoluer indépendamment des autres.

---

# Architecture générale

```text
                           Application
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
   Dispatcher               CapabilityManager          Services
        │
        ▼
   Scheduler
        │
        ├──────────────► TaskRegistry
        │
        ├──────────────► TaskExecutor
        │
        ├──────────────► Runtime
        │
        └──────────────► EventBus
                                │
                                ▼
                        Event Subscribers

        ▼
      Memory
```

L'Application agit comme **composition root** : elle instancie les composants du Kernel et injecte leurs dépendances.

---

# Application

L'Application est responsable de :

* créer les composants principaux ;
* injecter les dépendances ;
* initialiser le Runtime ;
* coordonner le cycle de vie global.

Elle ne contient aucune logique métier.

---

# Dispatcher

Le Dispatcher exécute les commandes enregistrées.

Responsabilités :

* résolution des commandes ;
* exécution ;
* propagation des résultats.

Le Dispatcher reste indépendant des autres composants.

---

# Capability Manager

Le gestionnaire de capacités permet d'enregistrer dynamiquement les fonctionnalités disponibles.

Chaque capacité est :

* indépendante ;
* déclarative ;
* validée avant utilisation.

---

# Services

Les services représentent les composants techniques du Runtime.

Ils disposent :

* d'un cycle de vie ;
* d'une stratégie d'initialisation ;
* d'une supervision.

---

# Memory

Le système mémoire est composé de plusieurs niveaux :

* mémoire persistante ;
* mémoire de session ;
* mémoire d'exécution.

Il fournit également :

* sérialisation ;
* statistiques ;
* scopes mémoire ;
* gestion centralisée.

---

# Scheduler

Le Scheduler orchestre l'exécution des tâches planifiées.

Il est composé de plusieurs éléments :

* Task
* Trigger
* OneShotTrigger
* IntervalTrigger
* CronTrigger
* TaskRegistry
* TaskExecutor
* SchedulerRuntime
* SchedulerStatistics

Le Scheduler reste indépendant de toute logique métier.

---

# Scheduler événementiel

Depuis le Sprint 9, le Scheduler est entièrement intégré à l'architecture événementielle.

Il publie automatiquement les événements suivants :

* SchedulerStarted
* SchedulerStopped
* SchedulerTicked
* ScheduledTaskTriggered
* ScheduledTaskExecuted
* ScheduledTaskFailed

Les consommateurs d'événements peuvent ainsi observer l'activité du Scheduler sans dépendre de son implémentation.

Cette approche améliore :

* le découplage ;
* l'observabilité ;
* l'extensibilité ;
* la testabilité.

---

# EventBus

L'EventBus constitue le mécanisme de communication entre composants.

Les producteurs publient des événements.

Les consommateurs s'y abonnent.

Aucun composant ne dépend directement des autres.

Cette architecture permet d'ajouter de nouveaux comportements sans modifier les producteurs d'événements.

---

# Runtime

Chaque composant dispose d'un Runtime léger permettant de suivre son état.

Le Runtime fournit notamment :

* état courant ;
* démarrage ;
* arrêt ;
* statistiques ;
* supervision.

---

# Monitoring

Le Monitoring permet de superviser l'état général du système.

Il s'appuie sur les événements produits par les différents composants.

Les futures évolutions pourront inclure :

* métriques ;
* tableaux de bord ;
* alertes ;
* supervision distribuée.

---

# Injection de dépendances

Toutes les dépendances sont injectées depuis l'Application.

Le Kernel privilégie les abstractions plutôt que les implémentations concrètes.

Cette approche facilite :

* les tests unitaires ;
* le remplacement des composants ;
* les évolutions futures.

---

# Cycle de vie

```text
Application
      │
      ▼
Initialisation
      │
      ▼
Création des composants
      │
      ▼
Injection des dépendances
      │
      ▼
Démarrage des services
      │
      ▼
Démarrage du Scheduler
      │
      ▼
Publication des événements
      │
      ▼
Exécution des tâches
      │
      ▼
Arrêt propre
```

---

# Qualité logicielle

Le projet applique une démarche de développement orientée qualité :

* Test Driven Development (TDD) ;
* typage Python moderne ;
* dataclasses ;
* injection de dépendances ;
* architecture événementielle ;
* composants faiblement couplés.

Chaque Sprint est validé uniquement lorsque :

* tous les tests passent ;
* aucune régression n'est détectée ;
* la qualité du code est conforme.

---

# État actuel du Kernel

| Composant              | État |
| ---------------------- | :--: |
| Application            |   ✅  |
| Dispatcher             |   ✅  |
| Capabilities           |   ✅  |
| Services               |   ✅  |
| Memory                 |   ✅  |
| Runtime                |   ✅  |
| Scheduler              |   ✅  |
| Scheduler événementiel |   ✅  |
| EventBus               |   ✅  |
| Monitoring             |   ✅  |

---

# Statistiques

État du projet après le Sprint 9 :

* **453 tests automatisés**
* **0 avertissement**
* **Ruff conforme**
* **Architecture événementielle complète**
* **Aucune régression détectée**

Le Kernel est désormais suffisamment mature pour accueillir les prochains développements, notamment l'observabilité avancée, les workflows, le SDK de plugins et les futures capacités d'intelligence artificielle.

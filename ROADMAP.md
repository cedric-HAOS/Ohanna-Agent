# ROADMAP

# Ohanna-Agent

## Vision du projet

Ohanna-Agent est un framework open source destiné à la création d'agents logiciels autonomes, modulaires et pilotés par événements.

L'objectif du projet est de fournir un noyau robuste, extensible et durable sur lequel pourront être construits différents moteurs d'orchestration, de décision et d'automatisation.

La feuille de route présentée ci-dessous décrit les grandes étapes de cette évolution.

---

# État actuel

## Version en développement

**v0.4.0 – Autonomous Core**

### Réalisé

* Architecture modulaire
* Dispatcher
* Runtime MQTT
* Event Bus
* Gestionnaire de capacités
* Auto-réparation
* Scheduler
* Runtime unifié
* Registry
* Executor
* Plus de **315 tests unitaires**
* Documentation d'architecture complète
* ADR
* Audits d'architecture

Le noyau du framework est désormais considéré comme fonctionnel et stable.

Les prochaines versions porteront principalement sur les services construits au-dessus du Kernel.

---

# Vision

L'évolution d'Ohanna-Agent est organisée autour de deux grandes phases.

## Phase 1 — Construction du Kernel

Objectif :

Construire une architecture robuste, modulaire et fortement découplée.

Statut :

**Terminée avec la version v0.4.0.**

Cette phase comprend :

* Dispatcher
* MQTT Runtime
* Scheduler
* Capability Manager
* Event Bus
* Contrats `core`
* Runtime
* Registry
* Executor
* Statistics
* State

---

## Phase 2 — Construction des Services intelligents

Objectif :

Développer les moteurs qui utiliseront le Kernel pour construire des comportements autonomes.

Cette phase débute avec la version **0.5.0**.

---

# Feuille de route

## v0.5.0 — Workflow Engine

Objectif :

Introduire un moteur de workflows permettant d'orchestrer plusieurs tâches.

### Prévu

* Workflow
* WorkflowRuntime
* WorkflowExecutor
* Dépendances entre tâches
* Conditions d'exécution
* Gestion des délais
* Reprise automatique
* Annulation d'un workflow

---

## v0.6.0 — Rule Engine

Objectif :

Permettre aux agents de prendre des décisions à partir de règles déclaratives.

### Prévu

* Rule Engine
* Évaluation de conditions
* Priorités
* Expressions
* Variables
* Contexte d'exécution
* Décisions automatiques

---

## v0.7.0 — Pipeline Engine

Objectif :

Orchestrer des traitements séquentiels ou parallèles.

### Prévu

* Pipeline
* Étapes
* Exécution parallèle
* Gestion des erreurs
* Reprise
* Rollback
* Timeout

---

## v0.8.0 — Persistence

Objectif :

Ajouter une couche de persistance indépendante du Kernel.

### Prévu

* SQLite
* Persistance des tâches
* Persistance des workflows
* Historique
* Sauvegarde automatique
* Chargement au démarrage

---

## v0.9.0 — Administration

Objectif :

Faciliter l'exploitation et la supervision du framework.

### Prévu

* API REST
* Supervision
* Interface Web
* Gestion des tâches
* Visualisation des workflows
* Statistiques avancées
* Tableau de bord

---

## v1.0.0 — Stable

Première version stable du framework.

### Objectifs

* Architecture stabilisée
* API publique documentée
* Documentation complète
* Compatibilité garantie
* Couverture de tests élevée
* Performances validées
* Première version de production

---

# Principes d'évolution

Chaque nouvelle fonctionnalité suit le même processus :

1. Analyse du besoin.
2. Conception de l'architecture.
3. Rédaction ou mise à jour d'un ADR si nécessaire.
4. Implémentation.
5. Tests unitaires.
6. Audit d'architecture.
7. Mise à jour de la documentation.
8. Publication d'une nouvelle version.

Cette discipline garantit une évolution progressive et maîtrisée du framework.

---

# Objectifs de qualité

Chaque release doit respecter les critères suivants :

* Tous les tests passent.
* Ruff ne remonte aucune erreur.
* La documentation est à jour.
* Les responsabilités restent clairement séparées.
* Les nouvelles fonctionnalités sont accompagnées de tests.
* Les décisions importantes sont documentées.

---

# Au-delà de la version 1.0

Après la stabilisation du Kernel et des principaux moteurs, plusieurs axes d'évolution sont envisagés :

* Exécution distribuée
* Multi-agents
* Clustering
* Haute disponibilité
* Persistance distribuée
* Exécution distante
* Observabilité avancée
* Intégration avec d'autres transports (HTTP, AMQP, Kafka, etc.)
* SDK pour le développement de capacités et de plugins

Ces évolutions resteront guidées par les principes fondateurs du projet :

* modularité ;
* découplage ;
* testabilité ;
* simplicité ;
* maintenabilité.

---

# Conclusion

La version **0.4.0 – Autonomous Core** marque la fin de la construction du Kernel d'Ohanna-Agent.

Les prochaines versions ne viseront plus à renforcer les fondations, mais à développer des services intelligents capables d'exploiter pleinement cette architecture.

L'objectif reste inchangé :

**Construire un framework d'agents autonomes, modulaire, robuste et durable, capable d'évoluer sans remettre en cause son noyau.**

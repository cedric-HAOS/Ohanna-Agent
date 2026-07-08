# Changelog

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le format s'inspire de **Keep a Changelog** et respecte le **Versioning Sémantique**.

---

# [0.8.0] - 2026-07-08

## Sprint 7 — Memory

### Ajouté

#### Memory

- Ajout du package `memory`
- Introduction du `MemoryManager`
- Ajout de `RuntimeMemory`
- Ajout de `SessionMemory`
- Ajout de `PersistentMemory`
- Ajout des `MemoryScope`
- Ajout des `MemoryEntry`

#### Persistance

- Ajout de `MemoryStorage`
- Persistance JSON
- Chargement de la mémoire persistante
- Sauvegarde explicite
- Injection du backend de stockage

#### Sérialisation

- Ajout de `MemorySerializer`
- Découplage stockage / sérialisation
- Préparation de futurs backends (SQLite, Redis…)

#### Statistiques

- Ajout de `MemoryStatistics`
- Comptage des :
  - hits
  - misses
  - sets
  - deletes
  - clears
  - saves
  - loads

#### Application

- Intégration du `MemoryManager`
- Injection de dépendances
- Enregistrement dans le `ServiceRegistry`

#### Architecture

- ADR-0025 — Gestion de la mémoire
- ADR-0026 — Politique de persistance

### Refactoring

- Remplacement du routage conditionnel par une table de routage (`MemoryScope` → implémentation mémoire)
- Amélioration du découplage des composants mémoire
- Séparation des responsabilités entre gestion, stockage et sérialisation

### Tests

- Plus de **420 tests automatisés**
- Couverture des nouveaux composants mémoire
- Validation des trois scopes mémoire
- Validation de la persistance JSON
- Validation de la sérialisation
- Validation des statistiques
- Validation de l'intégration dans `Application`

---

# [0.7.0] - 2026-07-08

## Sprint 6 — Scheduler

### Ajouté

- Scheduler
- DispatcherTaskExecutor
- SchedulerState
- SchedulerStatistics
- Runtime Scheduler
- Gestion des tâches planifiées

### Architecture

- Découplage Scheduler / Dispatcher
- Introduction des statistiques Scheduler

---

# [0.6.0] - 2026-07-08

## Sprint 5 — Capacités

### Ajouté

- Capability
- CapabilityManager
- Gestion des capacités
- Activation / désactivation
- Découverte des capacités

---

# [0.5.0] - 2026-07-08

## Sprint 4 — Auto-réparation

### Ajouté

- Auto-réparation
- Gestion des erreurs
- Runtime Recovery

---

# [0.4.0] - 2026-07-08

## Sprint 3 — MQTT Runtime

### Ajouté

- Runtime MQTT
- Gestion des événements MQTT
- Dispatcher MQTT

---

# [0.3.0] - 2026-07-08

## Sprint 2 — Core Services

### Ajouté

- ServiceRegistry
- EventBus
- PluginManager
- Dispatcher

---

# [0.2.0] - 2026-07-07

## Sprint 1 — Lifecycle

### Ajouté

- États applicatifs
- Gestion du cycle de vie
- LifecycleManager

---

# [0.1.0] - 2026-07-07

## Sprint 0 — Architecture

### Ajouté

- Architecture initiale
- ADR fondateurs
- Documentation
- Structure du projet
- Philosophie
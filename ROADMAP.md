# Roadmap

Cette feuille de route présente les évolutions prévues d'Ohanna-Agent.

Les fonctionnalités sont organisées par sprints afin de conserver une évolution incrémentale, fortement testée et guidée par l'architecture.

---

# Vision

L'objectif d'Ohanna-Agent est de devenir un framework Python moderne permettant de construire des agents autonomes, modulaires et événementiels.

Le projet repose sur plusieurs principes :

- Architecture modulaire
- Faible couplage
- Forte cohésion
- Injection de dépendances
- Communication par événements
- Testabilité
- Documentation par ADR
- Évolution incrémentale

---

# État actuel

## Sprint 0 — Architecture

✅ Terminé

- Architecture initiale
- Documentation
- ADR fondateurs

---

## Sprint 1 — Lifecycle

✅ Terminé

- États applicatifs
- Gestion du cycle de vie

---

## Sprint 2 — Core Services

✅ Terminé

- ServiceRegistry
- EventBus
- PluginManager
- Dispatcher

---

## Sprint 3 — MQTT Runtime

✅ Terminé

- Runtime MQTT
- Dispatcher MQTT
- Gestion des événements

---

## Sprint 4 — Auto-réparation

✅ Terminé

- Runtime Recovery
- Gestion des erreurs
- Auto-réparation

---

## Sprint 5 — Capacités

✅ Terminé

- CapabilityManager
- Activation
- Découverte
- Gestion des capacités

---

## Sprint 6 — Scheduler

✅ Terminé

- Scheduler
- DispatcherTaskExecutor
- Runtime Scheduler
- Statistiques Scheduler

---

## Sprint 7 — Memory

✅ Terminé

- RuntimeMemory
- SessionMemory
- PersistentMemory
- MemoryManager
- MemoryStorage
- MemorySerializer
- MemoryStatistics
- Intégration dans Application

---

# Sprint 8 — Workflows

## Objectif

Permettre l'enchaînement de plusieurs actions sous forme de workflows.

### Prévu

- Workflow
- WorkflowStep
- WorkflowContext
- WorkflowRunner
- Conditions
- Variables
- Branchements
- Gestion des erreurs
- Reprise d'exécution

---

# Sprint 9 — Plugin SDK

## Objectif

Stabiliser le développement de plugins.

### Prévu

- Plugin SDK
- API publique
- Cycle de vie des plugins
- Dépendances
- Découverte automatique
- Validation
- Packaging

---

# Sprint 10 — Observabilité

## Objectif

Fournir une vision complète de l'état interne du framework.

### Prévu

- Health Manager
- Diagnostics
- Metrics
- Monitoring
- Logging avancé
- Export Prometheus
- Dashboard

---

# Sprint 11 — Raisonnement

## Objectif

Ajouter un moteur de décision.

### Prévu

- Context Engine
- Rule Engine
- Goal Manager
- Decision Engine
- Planification
- Priorités

---

# Sprint 12 — Intelligence

## Objectif

Préparer l'intégration de modèles d'IA.

### Prévu

- LLM Provider
- Prompt Manager
- Conversation Context
- Long-Term Memory
- Tool Calling
- Agent Reasoning

---

# Sprint 13 — Distribution

## Objectif

Permettre plusieurs agents coopératifs.

### Prévu

- Agent Discovery
- Remote Commands
- Shared Events
- Distributed Scheduler
- Shared Memory
- Cluster Runtime

---

# Évolutions techniques

## Mémoire

Prévu :

- TTL
- Expiration
- Cache
- SQLite
- Redis
- Chiffrement
- Compression
- Transactions

---

## Scheduler

Prévu :

- Cron
- Priorités
- Réessais
- Délais
- Backoff exponentiel
- Files d'attente

---

## Dispatcher

Prévu :

- Middlewares
- Pipeline
- Validation
- Autorisation
- Traces

---

## MQTT

Prévu :

- QoS avancé
- Sessions persistantes
- Découverte automatique
- Rétention
- Reconnexion intelligente

---

## Plugins

Prévu :

- Marketplace
- Signature
- Isolation
- Sandbox
- Hot Reload

---

# Documentation

Chaque sprint comprend :

- ADR
- README
- ROADMAP
- CHANGELOG
- CORE
- Tests
- Audit d'architecture

---

# Objectif v1.0.0

La version 1.0.0 sera atteinte lorsque le framework proposera :

- Architecture stable
- API publique stabilisée
- SDK Plugins
- Mémoire complète
- Scheduler avancé
- Observabilité
- Workflows
- Raisonnement
- Documentation complète
- Plus de 1 000 tests automatisés

---

# État actuel

Version :

**v0.8.0**

Tests :

**422**

Architecture :

Stable

Documentation :

À jour

Sprint actuel :

✅ Sprint 7 terminé

Prochaine étape :

➡️ Sprint 8 — Workflows
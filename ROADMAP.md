# Roadmap

## Objectif

La roadmap décrit les grandes étapes de développement de **Shikamaru**, le premier agent du projet **Ohanna-Agent**.

Chaque sprint poursuit un objectif clair et se termine par :

- une revue d'architecture ;
- un audit logiciel ;
- une batterie de tests automatisés ;
- un commit Git.

---

# Sprint 0 — Vision & Architecture

**Statut :** ✅ Terminé

## Objectif

Définir les fondations du projet avant le développement.

## Réalisations

- [x] Vision
- [x] Philosophie
- [x] Capacités
- [x] Architecture logicielle
- [x] Cycle de vie
- [x] États
- [x] MQTT
- [x] Message Model
- [x] Configuration
- [x] Documentation
- [x] Roadmap

## Résultat

Le projet est entièrement conçu avant l'écriture du premier composant.

---

# Sprint 1 — Core Framework

**Statut :** 🚧 En cours

## Objectif

Construire le noyau technique de Shikamaru.

---

## Phase 1 — Foundations

**Statut :** ✅ Terminée

### Architecture

- [x] ADR-0001 — Lifecycle
- [x] ADR-0002 — Application
- [x] ADR-0003 — Composition
- [x] ADR-0004 — State Transitions
- [x] ADR-0005 — Configuration Model
- [x] ADR-0006 — Logging Strategy

### Développement

- [x] Lifecycle
- [x] Configuration
- [x] ConfigurationLoader
- [x] YAML
- [x] Tests
- [x] Documentation
- [x] README

### Qualité

- [x] Ruff
- [x] Pytest
- [x] Pydantic
- [x] Audit d'architecture

---

## Phase 2 — Core Services

**Statut :** 🚧 À démarrer

### Logging

- [ ] LoggingConfigurator

### Health

- [ ] HealthMonitor

### MQTT

- [ ] MQTTClient

### Plugins

- [ ] PluginManager

---

## Phase 3 — Application

**Statut :** ⏳ À venir

### Application

- [ ] initialize()
- [ ] run()
- [ ] stop()

### Intégration

- [ ] Tests d'intégration
- [ ] Validation finale
- [ ] Audit logiciel
- [ ] Sprint Review

---

# Sprint 2 — Home Assistant

**Statut :** ⏳ Prévu

## Objectif

Intégrer Shikamaru dans Home Assistant.

### Fonctionnalités

- [ ] MQTT Discovery
- [ ] Device Information
- [ ] Entités
- [ ] Services
- [ ] Diagnostics

---

# Sprint 3 — Interface Web

**Statut :** ⏳ Prévu

## Objectif

Créer une interface d'administration.

### Fonctionnalités

- [ ] Dashboard
- [ ] Monitoring
- [ ] Logs
- [ ] Plugins
- [ ] Configuration

---

# Sprint 4 — Auto-réparation

**Statut :** ⏳ Prévu

## Objectif

Permettre à Shikamaru de surveiller et réparer automatiquement certains dysfonctionnements.

### Fonctionnalités

- [ ] Auto-diagnostic
- [ ] Auto-réparation
- [ ] Watchdog
- [ ] Recovery
- [ ] Notifications

---

# Vision

À l'issue de la roadmap, Shikamaru sera un agent capable de :

- gérer son propre cycle de vie ;
- charger une configuration validée ;
- publier son état de santé ;
- communiquer via MQTT ;
- charger dynamiquement des plugins ;
- s'intégrer à Home Assistant ;
- être administré via une interface Web ;
- détecter et corriger certaines anomalies automatiquement.

---

# Méthodologie

Chaque évolution du projet suit le cycle suivant :

1. Discussion
2. ADR
3. Implémentation
4. Tests
5. Audit
6. Commit Git

Cette approche garantit une architecture cohérente, documentée et durable.

---

# État du projet

| Sprint | Statut |
|---------|--------|
| Sprint 0 | ✅ Terminé |
| Sprint 1 | 🚧 En cours |
| Sprint 2 | ⏳ Prévu |
| Sprint 3 | ⏳ Prévu |
| Sprint 4 | ⏳ Prévu |
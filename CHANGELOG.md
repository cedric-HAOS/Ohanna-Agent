# Changelog

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le format suit les recommandations de **Keep a Changelog** et respecte le versioning **Semantic Versioning (SemVer)**.

---

# [3.0.0] - 2026-07-08

## 🎉 Version majeure

Cette version marque la fin des fondations du noyau d'Ohanna-Agent.

Le projet dispose désormais :

- d'une architecture hexagonale complète ;
- d'un runtime MQTT opérationnel ;
- d'un système d'événements robuste ;
- d'un moteur de commandes ;
- d'un cycle de vie complet ;
- d'une architecture validée par ADR ;
- d'une couverture de tests complète.

Le projet est désormais prêt à accueillir les premiers plugins métiers.

---

# ✨ Ajouts

## Architecture

Ajout de l'architecture hexagonale complète.

Mise en place des couches :

- Domain
- Application
- Infrastructure
- Runtime

---

## Cycle de vie

Ajout du cycle de vie complet :

- CREATED
- INITIALIZING
- STARTING
- RUNNING
- STOPPING
- STOPPED
- ERROR

---

## Bus d'événements

Création du moteur d'événements.

Ajout :

- Event Dispatcher
- Event Handler
- Event Publisher
- Event Subscription
- propagation synchrone
- propagation typée

---

## Commandes

Ajout du système de commandes.

Fonctionnalités :

- Command
- Handler
- Validation
- Dispatcher
- typage

---

## Configuration

Ajout du système de configuration.

Fonctionnalités :

- chargement YAML
- valeurs par défaut
- validation
- injection de configuration

---

## Runtime MQTT

Implémentation complète du runtime MQTT.

Ajouts :

- connexion automatique

- reconnexion automatique

- publication

- abonnement

- routage des messages

- sérialisation

- désérialisation

- QoS configurable

- gestion des erreurs réseau

- découplage Infrastructure / Domaine

---

## Messages

Ajout :

- MessageEnvelope

- EventMessage

- CommandMessage

- MessageSerializer

- MessageDeserializer

---

## Application

Création de la façade principale :

Application

Responsabilités :

- démarrage

- arrêt

- initialisation

- gestion des services

- orchestration

---

## Services

Ajout des services principaux :

- ConfigurationService

- EventDispatcher

- MQTT Runtime

- Command Dispatcher

---

## Documentation

Création de la documentation complète :

README

ROADMAP

CORE

ADR

Architecture

Philosophie

Plugins

MQTT

Message Model

Configuration

Capacités

États

Conventions MQTT

---

# 🏗 Architecture

Architecture entièrement documentée.

Validation de :

- découplage métier
- inversion des dépendances
- ports/adapters
- injection des dépendances
- responsabilité unique

---

# 📑 ADR

Validation des ADR :

- ADR-0001
- ADR-0002
- ADR-0003
- ADR-0004
- ADR-0005
- ADR-0006
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0010
- ADR-0011
- ADR-0012
- ADR-0013
- ADR-0014

---

# 🧪 Tests

Couverture complète des composants.

156 tests unitaires.

Tests :

- Application

- Dispatcher

- Events

- Commands

- Lifecycle

- MQTT

- Configuration

- Runtime

- Serialization

- Infrastructure

Tous les tests sont validés.

---

# 🔧 Qualité

Validation complète :

- Ruff

- Pytest

- Typage

- Architecture

- ADR

- Documentation

---

# 🚀 Performances

Optimisations :

- réduction des dépendances

- initialisation plus rapide

- réduction des allocations

- simplification du dispatcher

- amélioration du routage MQTT

---

# 📚 Documentation

Nouvelle documentation V3.

Ajout :

README

ROADMAP

CORE

CHANGELOG

Architecture

ADR

Documentation développeur

Conventions MQTT

Guide d'extension

---

# 🔒 Fiabilité

Amélioration :

- gestion des erreurs

- isolation des composants

- robustesse MQTT

- validation des messages

- arrêt propre

- démarrage sécurisé

---

# 🎯 Objectif atteint

Le cœur d'Ohanna-Agent est désormais considéré comme stable.

Le projet est prêt pour :

- les plugins métiers

- Home Assistant

- ESPHome

- Zigbee2MQTT

- Node-RED

- MQTT distribué

- scénarios domotiques complexes

---

# [2.0.0] - 2026-07-08

## Ajouts

### Phase 2 — Core Services

Création :

- Application
- Dispatcher
- Services
- Configuration
- Tests unitaires

76 tests validés.

---

# [1.0.0] - 2026-07-07

## Première version publique

Création des fondations du projet.

Ajouts :

- architecture hexagonale
- événements
- commandes
- lifecycle
- conventions MQTT
- philosophie
- documentation initiale

---

# Versions futures

Les prochaines versions introduiront :

## Version 3.1

- Plugin Manager
- découverte automatique des plugins
- chargement dynamique
- dépendances entre plugins

---

## Version 3.2

- Scheduler
- tâches planifiées
- timers
- cron

---

## Version 3.3

- supervision
- métriques
- Health API
- monitoring

---

## Version 3.4

- Web API
- REST
- WebSocket

---

## Version 4.0

Première version LTS d'Ohanna-Agent.

Objectifs :

- stabilité long terme
- API figée
- compatibilité des plugins
- documentation utilisateur
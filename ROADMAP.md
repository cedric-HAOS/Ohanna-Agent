# ROADMAP.md

# Roadmap d'Ohanna-Agent

> **Version : 3.0**
>
> État du projet : **Phase 3 terminée**
>
> Architecture stabilisée – Noyau Shikamaru opérationnel

---

# Vision

Ohanna-Agent a pour objectif de devenir un agent autonome, modulaire et distribué, capable de fonctionner durablement sur des infrastructures domestiques ou professionnelles.

Le développement suit plusieurs principes fondamentaux :

* simplicité du noyau ;
* architecture orientée événements ;
* communication exclusivement par MQTT ;
* extensibilité par plugins ;
* forte testabilité ;
* documentation pilotée par les ADR.

Chaque phase produit un logiciel entièrement fonctionnel avant de passer à la suivante.

---

# État actuel

## Architecture

Le noyau **Shikamaru** est désormais entièrement opérationnel.

Les composants principaux sont implémentés :

* cycle de vie de l'application ;
* EventBus ;
* Dispatcher ;
* système de commandes ;
* configuration ;
* journalisation ;
* Runtime MQTT ;
* intégration complète MQTT ↔ EventBus.

L'architecture est maintenant suffisamment stable pour accueillir les futurs plugins.

---

## Documentation

La documentation d'architecture est maintenue parallèlement au code.

Les ADR validés documentent les décisions majeures.

Le projet possède désormais :

* README
* ROADMAP
* CORE
* CHANGELOG
* documentation d'architecture
* ADR

---

## Qualité

À ce jour :

* **156 tests automatisés**
* couverture des composants critiques
* Ruff
* Pytest
* architecture validée
* documentation synchronisée

Le projet privilégie la qualité du code avant l'ajout de nouvelles fonctionnalités.

---

# Historique des phases

## Sprint 0 — Fondation

### Objectifs

Créer les fondations du projet.

### Réalisations

* philosophie
* architecture logicielle
* modèle événementiel
* conventions MQTT
* documentation
* premières ADR

**Statut : Terminé**

---

## Sprint 1 — Noyau

### Objectifs

Créer le noyau Shikamaru.

### Réalisations

* Event
* EventBus
* Dispatcher
* Commands
* Lifecycle
* Configuration
* Logger

**Statut : Terminé**

---

## Sprint 2 — Services Core

### Objectifs

Construire les services principaux.

### Réalisations

* Application
* Bootstrap
* Services Core
* amélioration des tests
* stabilisation de l'architecture

**Statut : Terminé**

---

## Sprint 3 — Runtime MQTT

### Objectifs

Permettre au noyau de communiquer avec le reste du système.

### Réalisations

* Runtime MQTT
* connexion Broker
* publication
* souscription
* intégration EventBus
* architecture événementielle distribuée

ADR-0014 valide définitivement cette architecture.

**Statut : Terminé**

---

# Prochaines phases

Le noyau étant désormais stable, les développements se concentrent sur les capacités de l'agent.

---

# Sprint 4 — Système de Plugins

## Objectif

Permettre à Ohanna-Agent d'être extensible sans modifier le noyau.

### Fonctionnalités prévues

* PluginManager
* découverte automatique
* chargement dynamique
* activation
* désactivation
* isolation
* dépendances
* métadonnées des plugins
* API publique du noyau

### Livrables

* premier plugin officiel
* documentation développeur
* nouvelles ADR

---

# Sprint 5 — Scheduler

## Objectif

Permettre l'exécution différée de commandes.

### Fonctionnalités

* tâches planifiées
* timers
* cron
* événements périodiques
* reprise après redémarrage

---

# Sprint 6 — Persistence

## Objectif

Ajouter une mémoire persistante.

### Fonctionnalités

* stockage des états
* historique
* snapshots
* restauration
* sérialisation

---

# Sprint 7 — Observabilité

## Objectif

Rendre le système observable.

### Fonctionnalités

* métriques
* Health Check avancé
* Prometheus
* traces
* statistiques
* supervision

---

# Sprint 8 — Sécurité

## Objectif

Renforcer la sécurité.

### Fonctionnalités

* authentification MQTT
* ACL
* signature des messages
* validation
* contrôle des permissions

---

# Sprint 9 — Plugins Officiels

Développement des premiers plugins :

* MQTT Discovery
* Home Assistant
* ESPHome
* Shell
* HTTP
* Webhook
* Scheduler
* Notifications

---

# Sprint 10 — Distribution

## Objectif

Faciliter le déploiement.

### Livrables

* Docker
* Docker Compose
* installation Linux
* installation Windows
* installation Raspberry Pi

---

# Sprint 11 — API

Création d'une API officielle.

### Fonctionnalités

* REST
* WebSocket
* authentification
* documentation OpenAPI

---

# Sprint 12 — Interface Web

Développement d'une interface d'administration.

### Fonctionnalités

* tableau de bord
* état des plugins
* événements
* métriques
* configuration
* journaux

---

# Sprint 13 — Intelligence

Développement des premières capacités d'automatisation.

### Fonctionnalités

* règles
* workflows
* scénarios
* conditions
* actions

---

# Sprint 14 — Version 1.0

Objectif :

publier une première version stable.

Elle comprendra :

* noyau stable
* API stable
* plugins officiels
* documentation complète
* installation simplifiée
* couverture de tests élevée

---

# Priorités

Les priorités du projet sont toujours les suivantes :

1. stabilité du noyau ;
2. qualité du code ;
3. documentation ;
4. tests ;
5. extensibilité ;
6. nouvelles fonctionnalités.

Une fonctionnalité n'est ajoutée que si elle respecte ces principes.

---

# Critères de validation d'une phase

Chaque sprint est considéré comme terminé lorsque :

* les fonctionnalités sont implémentées ;
* les tests sont écrits ;
* tous les tests passent avec succès ;
* Ruff ne détecte aucune anomalie ;
* la documentation est mise à jour ;
* les ADR nécessaires sont validés.

---

# État du projet

| Élément           | Statut         |
| ----------------- | -------------- |
| Sprint 0          | ✅ Terminé      |
| Sprint 1          | ✅ Terminé      |
| Sprint 2          | ✅ Terminé      |
| Sprint 3          | ✅ Terminé      |
| Tests automatisés | ✅ 156          |
| Architecture      | ✅ Stabilisée   |
| MQTT Runtime      | ✅ Opérationnel |
| ADR-0014          | ✅ Validé       |
| Documentation     | ✅ Synchronisée |

---

# Vision à long terme

À terme, Ohanna-Agent doit devenir une plateforme générique d'agents autonomes capable de :

* communiquer via MQTT ;
* être entièrement piloté par événements ;
* exécuter dynamiquement des plugins ;
* superviser des équipements ;
* interagir avec Home Assistant, ESPHome et d'autres systèmes ;
* rester léger, robuste et facilement déployable sur Raspberry Pi, mini-PC ou serveurs Linux.

Le noyau **Shikamaru** constitue désormais une base solide sur laquelle pourront être construites toutes les futures capacités du projet.

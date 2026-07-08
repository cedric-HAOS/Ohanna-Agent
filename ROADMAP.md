# ROADMAP

Ce document décrit les grandes étapes de développement de **Shikamaru**, le noyau d'**Ohanna-Agent**.

La roadmap est organisée par phases fonctionnelles. Chaque phase construit progressivement les capacités du noyau tout en conservant une architecture simple, modulaire et fortement testée.

---

# Phase 0 — Fondation

## Objectif

Définir la vision du projet et les principes d'architecture.

## Réalisations

* Vision
* Philosophie
* Capacités
* Architecture logicielle
* États
* Plugins
* MQTT
* Configuration
* Documentation
* Roadmap
* ADR initiales

## Statut

**Terminée**

---

# Phase 1 — Core Framework

## Objectif

Construire les fondations techniques du noyau.

## Réalisations

* Lifecycle
* Configuration
* Logger
* Health
* Interfaces MQTT
* Initialisation de l'application
* Tests unitaires

## Statut

**Terminée**

---

# Phase 2 — Core Services

## Objectif

Mettre en place les services internes du noyau.

## Réalisations

### Service Registry

* Enregistrement des services
* Recherche des services
* Injection de dépendances

### Event Model

* Classe `Event`
* Horodatage UTC
* Identifiant unique

### Event Bus

* Publication d'événements
* Abonnement
* Désabonnement

### Command Model

* Classe `Command`
* Horodatage UTC
* Identifiant unique

### Command Dispatcher

* Enregistrement des commandes
* Routage
* Gestion des erreurs
* Publication d'événements

### Scheduler

* Planification des tâches
* Publication des événements d'exécution

### Plugin Manager

* Gestion du cycle de vie
* États des plugins
* Validation des transitions

### Runtime

* Création automatique des services
* Enregistrement dans le Service Registry
* Initialisation du noyau

### Qualité

* 76 tests unitaires
* Ruff validé

## ADR

* ADR-0007 — Service Registry
* ADR-0008 — Event Bus
* ADR-0009 — Scheduler
* ADR-0010 — Plugin Lifecycle
* ADR-0011 — Command Dispatcher
* ADR-0012 — Dependency Injection

## Statut

**Terminée**

---

# Phase 3 — MQTT Runtime

## Objectif

Construire le moteur de communication MQTT.

## Prévisions

* Client MQTT
* Reconnexion automatique
* Publications
* Souscriptions
* Gestion des commandes
* Gestion des événements
* Heartbeat
* Découverte automatique
* Tests unitaires

## Statut

**À réaliser**

---

# Phase 4 — DNS

## Objectif

Développer le plugin DNS.

## Prévisions

* Résolution DNS
* Cache
* Reload dynamique
* Statistiques
* Supervision

## Statut

**À réaliser**

---

# Phase 5 — DHCP

## Objectif

Développer le plugin DHCP.

## Prévisions

* Attribution des baux
* Réservations
* Supervision
* Publication MQTT

## Statut

**À réaliser**

---

# Phase 6 — NTP

## Objectif

Développer le plugin NTP.

## Prévisions

* Synchronisation
* Publication de l'état
* Surveillance de la dérive

## Statut

**À réaliser**

---

# Phase 7 — Supervision

## Objectif

Centraliser les métriques du noyau.

## Prévisions

* CPU
* Mémoire
* Disque
* Réseau
* Santé des plugins
* Temps de fonctionnement
* Métriques internes

## Statut

**À réaliser**

---

# Phase 8 — Home Assistant

## Objectif

Intégrer Shikamaru à Home Assistant.

## Prévisions

* Découverte MQTT
* Entités
* Diagnostics
* Contrôle des plugins
* Configuration

## Statut

**À réaliser**

---

# Phase 9 — Interface Web

## Objectif

Créer une interface d'administration.

## Prévisions

* Tableau de bord
* Santé du système
* Journaux
* Plugins
* Commandes
* Configuration
* Diagnostics

## Statut

**À réaliser**

---

# Vision long terme

À terme, Shikamaru doit devenir un noyau générique permettant de développer des agents spécialisés tout en partageant une infrastructure commune.

Les futurs agents (DNS, DHCP, NTP, supervision, Home Assistant, etc.) utiliseront tous les mêmes services du noyau :

* Lifecycle
* Service Registry
* Event Bus
* Command Dispatcher
* Scheduler
* Plugin Manager

Cette architecture garantit un faible couplage, une excellente testabilité et une grande évolutivité.

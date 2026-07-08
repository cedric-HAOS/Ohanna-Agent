# CHANGELOG

Toutes les évolutions importantes du projet **Shikamaru** sont documentées dans ce fichier.

Le projet suit une approche de développement incrémentale basée sur des phases fonctionnelles.

---

# Version 0.2.0 — Core Services

**Date :** 08/07/2026

## Ajouts

### Modèle d'événements

* Ajout de la classe `Event`.
* Génération automatique d'un identifiant unique.
* Horodatage UTC automatique.

### Event Bus

* Publication d'événements.
* Gestion des abonnements.
* Gestion des désabonnements.
* Événements typés.

### Modèle de commandes

* Ajout de la classe `Command`.
* Génération automatique d'un identifiant unique.
* Horodatage UTC automatique.

### Command Dispatcher

* Enregistrement des commandes.
* Routage des commandes.
* Gestion des erreurs.
* Publication des événements d'exécution.

### Service Registry

* Enregistrement des services.
* Recherche des services.
* Vérification de leur présence.
* Suppression des services.

### Scheduler

* Planification des tâches.
* Exécution synchrone.
* Publication d'événements après exécution.

### Plugin Manager

* Gestion centralisée des plugins.
* Cycle de vie des plugins.
* Validation des transitions d'état.
* États :

  * REGISTERED
  * INITIALIZED
  * RUNNING
  * STOPPED

### Runtime

* Création automatique des services du noyau.
* Enregistrement automatique dans le Service Registry.
* Initialisation du runtime via `Application`.

### Documentation

* ADR-0007 à ADR-0012.
* Mise à jour du README.
* Mise à jour de la Roadmap.
* Mise à jour de l'architecture du noyau.

### Tests

* Ajout de tests unitaires pour :

  * Event
  * EventBus
  * Command
  * CommandDispatcher
  * ServiceRegistry
  * Scheduler
  * PluginManager
  * Application

* **76 tests unitaires**

* **100 % des tests réussis**

* **Ruff validé**

---

# Version 0.1.0 — Core Framework

**Date :** 07/07/2026

## Ajouts

### Fondation du noyau

* Lifecycle
* Configuration
* Logger
* Health
* Interfaces MQTT

### Documentation

* Vision
* Philosophie
* Capacités
* Architecture logicielle
* États
* Plugins
* MQTT
* Configuration
* Roadmap

### Architecture

* ADR-0001 à ADR-0006

### Qualité

* Mise en place des tests unitaires.
* Intégration de Ruff.
* Premiers composants du noyau.

---

# Version 0.0.1 — Fondation

**Date :** 07/07/2026

## Création du projet

* Initialisation du dépôt Git.
* Mise en place de l'environnement Python.
* Configuration de Ruff.
* Configuration de Pytest.
* Première structure du projet.
* Première documentation d'architecture.

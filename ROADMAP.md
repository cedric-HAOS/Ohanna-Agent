# ROADMAP

## Vision

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités sont garanties dans le temps.

Ohanna-Agent ne supervise pas des équipements.

Il supervise les **capacités** attendues de l'infrastructure.

Chaque évolution du projet poursuit un objectif unique :

> Transformer des observations techniques en une vision fiable de l'état réel de la maison.

---

# État actuel

**Version : v0.10.0**

* ✔ 706 tests unitaires
* ✔ Architecture modulaire
* ✔ Runtime Infrastructure
* ✔ Moteur d'observations
* ✔ Capacités calculées

Le noyau est désormais suffisamment stable pour accueillir des fonctionnalités de plus haut niveau.

---

# Phase 1 — Fondations

**Statut : Terminée**

Objectif :

Construire un noyau robuste, testable et modulaire.

Réalisé :

* ✔ Lifecycle
* ✔ Configuration
* ✔ Logging
* ✔ Dispatcher
* ✔ EventBus
* ✔ Scheduler
* ✔ Memory
* ✔ Plugin SDK
* ✔ Plugin Runtime
* ✔ Capability Engine
* ✔ Health Runtime

---

# Phase 2 — Modèle d'infrastructure

**Statut : Terminée**

Objectif :

Permettre à l'agent de représenter l'infrastructure et son état d'exécution.

Réalisé :

* ✔ Infrastructure
* ✔ Node
* ✔ Service
* ✔ Endpoint
* ✔ Infrastructure Runtime
* ✔ Observation
* ✔ ObservationManager
* ✔ SchedulerObservationHandler
* ✔ InfrastructureCapabilityCalculator

Résultat :

Le projet est désormais capable de représenter une infrastructure, de recevoir des observations et de calculer les premières capacités.

---

# Phase 3 — Infrastructure déclarative

**Statut : En préparation**

Objectif :

Décrire entièrement une infrastructure sans écrire une seule ligne de Python.

Travaux prévus :

* Infrastructure YAML
* InfrastructureLoader
* Validation de configuration
* Création automatique des objets Infrastructure
* Génération automatique du Runtime
* Gestion des identifiants uniques
* Support de plusieurs environnements

À l'issue de cette phase, une infrastructure complète pourra être définie dans un simple fichier de configuration.

---

# Phase 4 — Moteur de supervision

**Statut : À venir**

Objectif :

Transformer Ohanna-Agent en véritable moteur de supervision.

Travaux prévus :

* Dépendances entre services
* Graphe de dépendances
* Calculs avancés des capacités
* Agrégation d'observations
* Historique
* Scores de santé
* Corrélation des événements
* Détection des dégradations
* Détection des pannes en cascade

À l'issue de cette phase, les capacités ne seront plus évaluées individuellement mais à partir de l'ensemble de l'infrastructure.

---

# Phase 5 — Tableau de bord Web

**Statut : À venir**

Objectif :

Fournir une interface indépendante de Home Assistant.

Travaux prévus :

* Interface Web
* Vue Infrastructure
* Vue Capacités
* Vue Observations
* Historique
* Alertes
* Timeline
* API REST
* API WebSocket

Cette interface devra rester disponible même si Home Assistant est indisponible.

---

# Phase 6 — Intégration Home Assistant

**Statut : À venir**

Objectif :

Publier les capacités calculées dans Home Assistant.

Travaux prévus :

* Entités Home Assistant
* États des capacités
* Diagnostics
* Capteurs
* Alertes
* Device Registry
* Area Registry
* Découverte automatique

Home Assistant deviendra un consommateur des capacités calculées par Ohanna-Agent.

---

# Objectif à long terme

À terme, Ohanna-Agent devra être capable de répondre automatiquement à des questions telles que :

* Le DNS est-il réellement disponible ?
* Puis-je encore résoudre les noms locaux ?
* La maison peut-elle envoyer des notifications ?
* Les sauvegardes sont-elles garanties ?
* Home Assistant est-il opérationnel ?
* Le réseau est-il encore fonctionnel malgré une panne ?

L'objectif est de raisonner sur les **capacités réelles** de l'infrastructure, plutôt que sur l'état isolé de ses composants.

---

# Qualité

Le projet conserve les objectifs suivants :

* Architecture modulaire
* Couplage faible
* Typage complet
* Documentation systématique
* Forte couverture de tests
* Revue d'architecture à chaque sprint
* Aucune régression fonctionnelle

Chaque sprint est validé par :

* Ruff
* Pytest
* Audit d'architecture
* Mise à jour de la documentation

---

# Prochaine étape

## Sprint 14 — Infrastructure déclarative

Objectifs :

* Décrire l'infrastructure en YAML
* Charger automatiquement les nœuds, services et endpoints
* Construire automatiquement le Runtime
* Préparer les futures dépendances entre services

Ce sprint marquera la transition entre une infrastructure codée en Python et une infrastructure entièrement déclarative.

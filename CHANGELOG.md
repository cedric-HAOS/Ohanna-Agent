# Changelog

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le projet suit les principes du **Semantic Versioning**.

---

# v0.9.0 — Sprint 9 : Scheduler événementiel

## Ajouté

### Scheduler événementiel

* Création d'un modèle d'événements dédié au Scheduler.
* Ajout des événements :

  * `SchedulerStarted`
  * `SchedulerStopped`
  * `SchedulerTicked`
  * `ScheduledTaskTriggered`
  * `ScheduledTaskExecuted`
  * `ScheduledTaskFailed`

### Publication d'événements

Le Scheduler publie désormais automatiquement ses événements de cycle de vie :

* démarrage ;
* arrêt ;
* tick.

Les événements liés à l'exécution des tâches sont également publiés :

* déclenchement d'une tâche ;
* exécution réussie ;
* échec d'exécution.

### Intégration avec l'Application

* Injection automatique de l'EventBus dans le Scheduler.
* Le Scheduler devient un producteur d'événements à part entière.

### Architecture

* Renforcement du découplage entre le Scheduler et les autres composants.
* Utilisation d'un contrat minimal pour la publication des événements.
* Amélioration de l'observabilité globale du Runtime.

### Tests

Ajout de nouveaux tests couvrant notamment :

* les événements du Scheduler ;
* la publication des événements de cycle de vie ;
* la publication des événements d'exécution ;
* l'intégration avec l'Application.

---

## Amélioré

* Architecture événementielle plus cohérente.
* Meilleure extensibilité du Scheduler.
* Meilleure testabilité.
* Réduction du couplage entre composants.
* Amélioration de la qualité du code.

---

## Corrigé

* Suppression des avertissements liés à l'utilisation de `datetime.utcnow()`.
* Harmonisation des exports du package `scheduler`.
* Stabilisation de l'intégration entre le Scheduler et l'Application.

---

## Statistiques

* **453 tests automatisés**
* **0 avertissement**
* **Ruff : conforme**
* **Aucune régression détectée**

---

# v0.8.0 — Sprint 8 : EventBus

## Ajouté

* Intégration complète de l'EventBus.
* Publication et abonnement aux événements.
* Architecture orientée événements.
* Nouveaux tests de validation.

---

# v0.7.0 — Sprint 7 : Context & Memory

## Ajouté

* Gestionnaire de mémoire.
* Mémoire persistante.
* Mémoire de session.
* Mémoire d'exécution.
* Sérialisation.
* Statistiques mémoire.

---

# v0.6.0 — Sprint 6 : Scheduler

## Ajouté

* Scheduler.
* Runtime du Scheduler.
* Triggers OneShot.
* Triggers Interval.
* Triggers Cron.
* Registre de tâches.
* Exécuteur de tâches.
* Statistiques du Scheduler.

---

# v0.5.0 — Sprint 5 : Capacités

## Ajouté

* Gestionnaire de capacités.
* Capacités dynamiques.
* Dépendances entre capacités.
* Validation des capacités.

---

# v0.4.0 — Sprint 4 : Auto-réparation

## Ajouté

* Runtime supervisé.
* Watchdog.
* Heartbeat.
* Monitoring.
* Stratégies de récupération.

---

# v0.3.0 — Sprint 3 : Runtime MQTT

## Ajouté

* Runtime MQTT.
* Publication.
* Souscription.
* Reconnexion automatique.
* Supervision MQTT.

---

# v0.2.0 — Sprint 2 : Services

## Ajouté

* Gestionnaire de services.
* Injection des dépendances.
* Runtime des services.

---

# v0.1.0 — Sprint 1 : Kernel

## Ajouté

* Noyau de l'application.
* Dispatcher.
* Commandes.
* Cycle de vie.
* Architecture modulaire.

---

# v0.0.0 — Sprint 0 : Fondation

## Ajouté

* Initialisation du projet.
* Architecture de référence.
* ADR.
* Documentation initiale.
* Configuration du dépôt Git.

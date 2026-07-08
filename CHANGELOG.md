# Changelog

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le projet suit les principes du **Semantic Versioning**.

---

# [0.8.0] - Sprint 8 - Architecture événementielle

## Ajout

### EventBus

* Introduction d'un **EventBus** interne.
* Publication synchrone des événements.
* Abonnement par type d'événement.
* Désabonnement des abonnés.
* Architecture prête pour les futurs transports distribués.

### EventSubscription

* Nouvelle classe `EventSubscription`.
* Encapsulation des abonnements.
* Utilisation de `dataclass(frozen=True, slots=True)`.

### Application

* Injection du `EventBus`.
* Enregistrement automatique du `EventBus` dans le `ServiceRegistry`.
* Publication des événements :

  * `ApplicationStarted`
  * `ApplicationStopped`
  * `ApplicationTicked`

### Dispatcher

Le `CommandDispatcher` devient totalement événementiel.

Publication automatique des événements :

* `CommandDispatched`
* `CommandSucceeded`
* `CommandFailed`

Aucun changement de comportement métier.

### Tests

Ajout des tests couvrant :

* EventBus
* EventSubscription
* Injection du EventBus
* Publication des événements Application
* Publication des événements Dispatcher

---

## Amélioration

### Architecture

Le projet évolue progressivement vers une architecture orientée événements.

Les composants communiquent désormais via un bus d'événements plutôt que par dépendances directes.

Cette évolution réduit fortement le couplage entre :

* Application
* Dispatcher
* Plugins
* Mémoire
* Services

### Injection de dépendances

Uniformisation de l'injection :

* MemoryManager
* EventBus

Préparation des prochaines injections de services.

### Qualité

Maintien d'une couverture de tests complète.

Aucune régression fonctionnelle observée.

---

## Documentation

Mise à jour de :

* README
* CHANGELOG
* ROADMAP
* Documentation d'architecture

---

# [0.7.0] - Sprint 7 - Mémoire

## Ajout

* Intégration complète du `MemoryManager`.
* Injection dans `Application`.
* Services mémoire.
* Tests d'injection.
* Documentation.

---

# [0.6.0] - Sprint 6 - Scheduler

## Ajout

* Scheduler.
* Runtime du Scheduler.
* États.
* Statistiques.
* Exécuteur de tâches.
* Déclencheurs.
* Couverture complète de tests.

---

# [0.5.0] - Sprint 5 - Capacités

## Ajout

* Gestionnaire de capacités.
* Dépendances.
* Activation.
* Désactivation.
* Priorités.
* Tests.

---

# [0.4.0] - Sprint 4 - Auto-réparation

## Ajout

* Runtime enrichi.
* Surveillance.
* Heartbeat.
* Monitoring.
* Reconnexion.
* Politiques.
* Tests.

---

# [0.3.0] - Sprint 3 - MQTT

## Ajout

* Client MQTT.
* Publisher.
* Subscriber.
* Messages.
* Transport.
* Reconnexion.
* Tests.

---

# [0.2.0] - Sprint 2 - Core Services

## Ajout

* ServiceRegistry.
* PluginManager.
* Runtime.
* Dispatcher.
* Exécuteur.
* Tests.

---

# [0.1.0] - Sprint 1 - Fondations

## Ajout

* Structure initiale du projet.
* Commandes.
* Événements.
* Runtime minimal.
* Documentation initiale.
* Infrastructure de tests.

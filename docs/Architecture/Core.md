# Architecture du cœur (Core)

## Objectif

Le **Core** constitue le noyau d'Ohanna-Agent.

Il fournit les services fondamentaux nécessaires au fonctionnement de l'agent, indépendamment :

* des modèles d'intelligence artificielle ;
* des protocoles réseau ;
* des interfaces utilisateur ;
* des transports de communication.

Le Core est conçu pour rester **simple, modulaire, testable et extensible**.

---

# Principes d'architecture

Le noyau repose sur plusieurs principes fondamentaux.

## Faible couplage

Chaque composant dépend du minimum possible des autres composants.

La communication entre services s'effectue principalement via le **EventBus**, limitant les dépendances directes.

---

## Forte cohésion

Chaque classe possède une responsabilité unique.

Exemples :

* `CommandDispatcher` : distribution des commandes.
* `EventBus` : diffusion des événements.
* `MemoryManager` : gestion de la mémoire.
* `ServiceRegistry` : localisation des services.
* `PluginManager` : gestion du cycle de vie des plugins.

---

## Injection de dépendances

Les dépendances sont injectées autant que possible.

Exemple :

* `MemoryManager`
* `EventBus`

Cette approche facilite :

* les tests unitaires ;
* le remplacement des composants ;
* les futures extensions.

---

## Architecture événementielle

Depuis le Sprint 8, le noyau adopte une communication orientée événements.

Les composants publient des événements plutôt que d'appeler directement les autres composants.

Cela réduit fortement le couplage interne.

---

# Vue d'ensemble

```text
                         Application
                               │
      ┌────────────────────────┼────────────────────────┐
      │                        │                        │
      ▼                        ▼                        ▼
CommandDispatcher         Scheduler              PluginManager
      │                                              │
      └──────────────────────┬───────────────────────┘
                             ▼
                         EventBus
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
    MemoryManager      ServiceRegistry    Plugins
```

---

# Application

L'`Application` constitue le point d'entrée du noyau.

Elle est responsable de :

* l'initialisation des composants ;
* l'injection des dépendances ;
* l'enregistrement des services ;
* le démarrage et l'arrêt du système.

Elle orchestre le fonctionnement général sans contenir de logique métier.

---

# EventBus

Le **EventBus** est désormais le mécanisme central de communication interne.

Il permet :

* l'abonnement à un type d'événement ;
* le désabonnement ;
* la publication synchrone d'événements.

Le fonctionnement est volontairement simple afin de garantir :

* de bonnes performances ;
* une compréhension immédiate ;
* une excellente testabilité.

---

# EventSubscription

Chaque abonnement est représenté par une instance de `EventSubscription`.

Une souscription associe :

* un type d'événement ;
* un gestionnaire (handler).

Cette abstraction permettra d'ajouter ultérieurement des fonctionnalités comme :

* priorités ;
* abonnements temporaires ;
* activation/désactivation ;
* filtrage.

---

# CommandDispatcher

Le `CommandDispatcher` reçoit les commandes et les transmet au gestionnaire approprié.

Il publie automatiquement plusieurs événements :

* `CommandDispatched`
* `CommandSucceeded`
* `CommandFailed`

Cette publication est totalement transparente pour les gestionnaires de commandes.

---

# ServiceRegistry

Le `ServiceRegistry` permet aux composants de retrouver les services partagés.

Les principaux services enregistrés sont :

* EventBus
* Scheduler
* MemoryManager
* PluginManager
* CommandDispatcher

Cette approche évite les dépendances circulaires.

---

# PluginManager

Le `PluginManager` assure le cycle de vie des plugins.

Il est responsable de :

* leur chargement ;
* leur enregistrement ;
* leur arrêt ;
* leur accès aux services du noyau.

Grâce au `EventBus`, les plugins peuvent réagir aux événements internes sans modifier le cœur du système.

---

# MemoryManager

Le `MemoryManager` centralise toutes les formes de mémoire utilisées par l'agent.

Il prend en charge :

* la mémoire de session ;
* la mémoire persistante ;
* la mémoire d'exécution ;
* les statistiques.

Son injection dans l'`Application` facilite les tests et les évolutions futures.

---

# Scheduler

Le Scheduler reste indépendant du reste du noyau.

À ce stade, il assure :

* la planification des tâches ;
* la gestion des déclencheurs ;
* les priorités ;
* les statistiques ;
* les états d'exécution.

Son intégration complète dans l'architecture événementielle est prévue lors d'un sprint ultérieur.

---

# Qualité

Le Core est développé avec plusieurs objectifs permanents :

* couverture de tests élevée ;
* absence de régressions ;
* conformité Ruff ;
* simplicité du code ;
* documentation systématique.

État actuel :

* **438 tests automatisés**
* **0 erreur Ruff**
* **Architecture événementielle opérationnelle**

---

# Évolutions prévues

Les prochaines évolutions du Core concernent principalement :

* intégration événementielle complète du Scheduler ;
* monitoring ;
* observabilité ;
* métriques internes ;
* auto-réparation ;
* diagnostics.

Toutes ces fonctionnalités exploiteront le `EventBus` afin de conserver un faible couplage entre les composants.

---

# Conclusion

Le Sprint 8 marque une évolution importante de l'architecture d'Ohanna-Agent.

Le noyau n'est plus seulement modulaire : il devient **événementiel**.

Cette évolution prépare les prochaines fonctionnalités (Scheduler, Monitoring, MQTT distribué, plugins avancés) tout en conservant les principes fondateurs du projet :

* simplicité ;
* modularité ;
* testabilité ;
* extensibilité ;
* stabilité.

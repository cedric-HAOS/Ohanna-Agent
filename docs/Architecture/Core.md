# Architecture du noyau Shikamaru

## Objectif

Le noyau **Shikamaru** fournit l'ensemble des services fondamentaux utilisés par les agents Ohanna.

Il est conçu autour d'une architecture modulaire, orientée événements et faiblement couplée.

Chaque composant possède une responsabilité clairement définie et communique avec les autres exclusivement au travers des services du noyau.

---

# Vue d'ensemble

```text
                           Application
                                 │
               ┌─────────────────┴─────────────────┐
               │                                   │
        Service Registry                   Core Runtime
               │                                   │
               ├───────────────┬───────────────────┤
               │               │                   │
           EventBus       Scheduler       CommandDispatcher
               │               │                   │
               └───────────────┼───────────────────┘
                               │
                        PluginManager
                               │
                            Plugins
```

---

# Principes d'architecture

Le noyau repose sur plusieurs principes fondamentaux.

## Responsabilité unique

Chaque composant possède une seule responsabilité.

Par exemple :

* EventBus transporte les événements.
* Scheduler planifie les tâches.
* PluginManager gère les plugins.

---

## Faible couplage

Les composants ne communiquent jamais directement entre eux.

Toutes les interactions passent par :

* le Service Registry ;
* l'Event Bus ;
* le Command Dispatcher.

---

## Injection de dépendances

Les composants ne créent jamais eux-mêmes leurs dépendances.

L'Application construit les services puis les enregistre dans le Service Registry.

---

## Architecture orientée événements

Les composants publient des événements sans connaître leurs consommateurs.

Cette approche facilite :

* l'extension du système ;
* les tests ;
* l'ajout de nouveaux plugins.

---

# Les composants

## Application

Point d'entrée du noyau.

Responsabilités :

* créer les services ;
* enregistrer les services ;
* démarrer le runtime ;
* arrêter proprement l'application.

---

## Service Registry

Point d'accès unique aux services du noyau.

Fonctions :

* enregistrer un service ;
* récupérer un service ;
* vérifier la présence d'un service ;
* supprimer un service.

---

## Event

Classe de base de tous les événements.

Chaque événement possède automatiquement :

* un identifiant unique ;
* un horodatage UTC.

Les événements sont immuables une fois publiés.

---

## Event Bus

Assure la communication interne.

Fonctions :

* abonnement ;
* désabonnement ;
* publication.

Le bus ne contient aucune logique métier.

---

## Command

Classe de base de toutes les commandes.

Chaque commande possède automatiquement :

* un identifiant unique ;
* un horodatage UTC.

Les commandes représentent des demandes d'action adressées au noyau ou à ses plugins.

---

## Command Dispatcher

Point d'entrée unique des commandes.

Responsabilités :

* enregistrer les gestionnaires ;
* router les commandes ;
* publier les événements d'exécution.

Le Dispatcher ne contient aucune logique métier.

---

## Scheduler

Planifie les tâches périodiques.

Responsabilités :

* enregistrer les tâches ;
* déclencher leur exécution ;
* publier un événement après chaque exécution.

---

## Plugin

Les plugins implémentent les fonctionnalités métier.

Ils utilisent exclusivement les services fournis par le noyau.

---

## Plugin Manager

Responsable du cycle de vie des plugins.

États :

* REGISTERED
* INITIALIZED
* RUNNING
* STOPPED

Le Plugin Manager garantit la validité des transitions entre ces états.

---

# Communication interne

Deux mécanismes complémentaires sont utilisés.

## Les événements

Les événements permettent de diffuser une information.

Exemples :

* MQTT connecté ;
* tâche exécutée ;
* plugin démarré ;
* changement d'état.

Les événements transitent par l'Event Bus.

---

## Les commandes

Les commandes représentent une demande d'action.

Exemples :

* démarrer un plugin ;
* arrêter un plugin ;
* publier un message ;
* recharger une configuration.

Les commandes transitent par le Command Dispatcher.

---

# Cycle de vie du noyau

```text
Application
      │
      ▼
Création des services
      │
      ▼
Enregistrement dans le Service Registry
      │
      ▼
Initialisation des plugins
      │
      ▼
Démarrage du Scheduler
      │
      ▼
Exécution du noyau
      │
      ▼
Arrêt des plugins
      │
      ▼
Arrêt du Scheduler
      │
      ▼
Fin de l'application
```

---

# Organisation du code

```text
src/
│
├── application.py
│
├── configuration/
│
├── core/
│   ├── command.py
│   ├── dispatcher.py
│   ├── event.py
│   ├── events.py
│   ├── lifecycle.py
│   ├── plugins.py
│   ├── scheduler.py
│   └── services.py
│
├── health/
│
├── logger/
│
└── mqtt/
```

---

# Principes de développement

Tout nouveau composant doit respecter les règles suivantes :

* responsabilité unique ;
* dépendances explicites ;
* communication par événements ou commandes ;
* intégration via le Service Registry ;
* couverture complète par des tests unitaires.

---

# État actuel

Le noyau Shikamaru dispose désormais de tous les services fondamentaux nécessaires au développement des futurs agents.

Les prochaines phases du projet pourront se concentrer sur les fonctionnalités métier (MQTT, DNS, DHCP, NTP, supervision et intégration Home Assistant) sans remettre en cause l'architecture du noyau.

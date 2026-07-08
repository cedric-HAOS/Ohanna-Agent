# Changelog

Toutes les évolutions importantes d'Ohanna-Agent sont documentées dans ce fichier.

Le projet suit les principes du **Semantic Versioning** tant que cela reste compatible avec son stade de développement.

---

# v0.10.0 — Sprint 13 : Infrastructure Runtime

*Date : Juillet 2026*

Cette version marque une évolution majeure de l'architecture.

Ohanna-Agent ne se contente plus d'exécuter des plugins et de planifier des tâches : il dispose désormais d'un véritable modèle d'infrastructure, d'un état d'exécution (Runtime), d'un moteur d'observations et des premières capacités calculées.

---

## Ajouté

### Modèle d'infrastructure

Introduction du modèle métier décrivant l'infrastructure supervisée.

Nouveaux objets :

* Infrastructure
* Node
* Service
* Endpoint

Fonctionnalités :

* navigation dans l'infrastructure ;
* recherche de services ;
* recherche de nœuds ;
* recherche d'endpoints ;
* API métier simplifiée.

---

### Runtime Infrastructure

Création d'un Runtime entièrement séparé du modèle métier.

Nouveaux composants :

* InfrastructureRuntime
* NodeRuntime
* ServiceRuntime
* EndpointRuntime

Le Runtime représente désormais l'état vivant de l'infrastructure sans modifier les objets métier.

---

### Moteur d'observations

Introduction d'un système d'observations indépendant.

Nouveaux composants :

* Observation
* ObservationManager

Les observations sont maintenant centralisées avant d'être appliquées au Runtime.

---

### Intégration Scheduler

Ajout du composant :

* SchedulerObservationHandler

Le Scheduler peut désormais convertir le résultat d'une vérification en observation standardisée.

Cette couche prépare l'intégration complète des plugins de supervision.

---

### Capacités calculées

Ajout des premières capacités calculées à partir du Runtime.

Nouveaux composants :

* InfrastructureCapability
* InfrastructureCapabilityCalculator

Premières capacités disponibles :

* dns_available
* mqtt_available

Les capacités sont désormais dérivées de l'état réel de l'infrastructure plutôt que directement des résultats des plugins.

---

### Démonstration

Ajout du script :

```
scripts/show_infrastructure_status.py
```

Ce script permet de visualiser :

* l'état des nœuds ;
* l'état des services ;
* les observations enregistrées ;
* les capacités calculées.

---

## Amélioré

* meilleure séparation entre modèle métier et état d'exécution ;
* architecture plus modulaire ;
* API de navigation enrichie ;
* meilleure extensibilité pour les futurs calculateurs de capacités ;
* préparation de l'infrastructure déclarative.

---

## Tests

Nouveaux tests couvrant :

* modèle Infrastructure ;
* Runtime ;
* Observation ;
* ObservationManager ;
* SchedulerObservationHandler ;
* InfrastructureCapabilityCalculator.

Résultat :

```
706 tests unitaires validés
```

Aucune régression détectée.

---

# v0.9.0

## Ajouté

* Architecture de plugins
* Capability Engine
* Runtime des plugins
* DNS Observer
* EventBus
* Scheduler
* Memory Manager

---

# v0.8.0

## Ajouté

* Plugin SDK
* Runtime des plugins
* États des plugins

---

# v0.7.0

## Ajouté

* Context & Memory
* Gestionnaire mémoire
* Injection des dépendances

---

# v0.6.0

## Ajouté

* Scheduler
* Runtime Scheduler
* Statistiques
* États du Scheduler

---

# v0.5.0

## Ajouté

* Capability Engine
* Gestion des capacités

---

# v0.4.0

## Ajouté

* Auto-réparation
* Health Runtime

---

# v0.3.0

## Ajouté

* Dispatcher
* Commandes
* Exécution des actions

---

# v0.2.0

## Ajouté

* Services principaux
* Configuration
* Journalisation

---

# v0.1.0

Première fondation du projet.

## Ajouté

* Cycle de vie de l'application
* Architecture du noyau
* Configuration initiale
* Premiers tests unitaires

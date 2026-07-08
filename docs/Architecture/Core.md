# Architecture du noyau (CORE)

## Version

**v0.10.0**

---

# Objectif

Le noyau d'Ohanna-Agent fournit les fondations nécessaires à la supervision d'une infrastructure.

Il ne supervise pas directement des équipements.

Il orchestre des composants spécialisés qui observent l'infrastructure, calculent son état et garantissent les capacités attendues.

Le noyau est conçu pour être :

* modulaire ;
* découplé ;
* testable ;
* extensible.

---

# Vision

L'infrastructure est décrite par les services qu'elle rend.

Les plugins réalisent des observations.

Le Runtime représente l'état courant.

Les capacités sont calculées à partir de cet état.

Le noyau coordonne l'ensemble.

---

# Architecture générale

```text
                          Application
                               │
                               ▼
                        Lifecycle Manager
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
 Configuration            EventBus              Dispatcher
        │                      │                      │
        └──────────────┬───────┴──────────────┬───────┘
                       ▼                      ▼
                  Scheduler             Plugin Runtime
                       │                      │
                       └──────────────┬───────┘
                                      ▼
                       SchedulerObservationHandler
                                      │
                                      ▼
                             ObservationManager
                                      │
                                      ▼
                          InfrastructureRuntime
                                      │
             ┌────────────────────────┴────────────────────────┐
             ▼                                                 ▼
        NodeRuntime                                     ServiceRuntime
             │                                                 │
             └────────────────────────┬────────────────────────┘
                                      ▼
                  InfrastructureCapabilityCalculator
                                      │
                                      ▼
                        InfrastructureCapability
```

---

# Les couches

## 1. Application

Point d'entrée du système.

Responsabilités :

* initialisation ;
* chargement de la configuration ;
* création des composants ;
* démarrage ;
* arrêt.

---

## 2. Configuration

Décrit le fonctionnement de l'agent.

Contient notamment :

* paramètres généraux ;
* MQTT ;
* plugins ;
* journalisation ;
* santé ;
* infrastructure (future évolution).

---

## 3. EventBus

Assure la communication entre composants.

Les composants ne se connaissent pas directement.

Ils échangent des événements.

---

## 4. Dispatcher

Exécute les commandes.

Il constitue le point central d'exécution des actions internes.

---

## 5. Scheduler

Planifie les vérifications.

Il décide uniquement :

* quand exécuter ;
* quelle vérification lancer.

Il ne stocke aucun état métier.

---

## 6. Plugins

Les plugins réalisent les observations.

Chaque plugin est autonome.

Exemples :

* DNS ;
* MQTT ;
* HTTP ;
* Home Assistant ;
* sauvegardes.

Le Runtime des plugins est indépendant du Runtime de l'infrastructure.

---

# Infrastructure

Le modèle Infrastructure décrit la maison telle qu'elle devrait être.

Il est statique.

Il ne contient aucun état d'exécution.

Les objets principaux sont :

* Infrastructure
* Node
* Service
* Endpoint

Ils peuvent être construits en mémoire ou, à terme, chargés depuis une description déclarative.

---

# Runtime

Le Runtime représente l'état vivant de l'infrastructure.

Il est indépendant du modèle.

Composants :

* InfrastructureRuntime
* NodeRuntime
* ServiceRuntime
* EndpointRuntime

Le Runtime évolue en permanence sans modifier le modèle métier.

---

# Observations

Les plugins produisent des observations.

Une observation représente un fait observé.

Exemples :

* résolution DNS réussie ;
* broker MQTT indisponible ;
* Home Assistant dégradé.

Toutes les observations sont centralisées par l'ObservationManager.

---

# ObservationManager

L'ObservationManager constitue le point d'entrée unique des observations.

Responsabilités :

* enregistrer les observations ;
* mettre à jour le Runtime ;
* maintenir un état cohérent de l'infrastructure.

Les plugins ne modifient jamais directement le Runtime.

---

# SchedulerObservationHandler

Le SchedulerObservationHandler fait le lien entre le Scheduler et l'ObservationManager.

Son rôle est de convertir le résultat d'une exécution planifiée en observation standardisée.

Cette séparation évite de coupler le Scheduler à la représentation interne de l'infrastructure.

---

# Capacités calculées

Les capacités ne sont pas observées directement.

Elles sont calculées.

Le calculateur actuel est :

* InfrastructureCapabilityCalculator

Premières capacités disponibles :

* dns_available
* mqtt_available

À terme, des capacités plus complexes seront calculées à partir de plusieurs observations, de dépendances et de règles métier.

---

# Principe fondamental

Le flux d'information suit toujours la même direction :

```text
Plugin
   │
   ▼
Observation
   │
   ▼
ObservationManager
   │
   ▼
InfrastructureRuntime
   │
   ▼
Capability Calculator
   │
   ▼
Capabilities
```

Aucun composant ne remonte dans la chaîne.

Cette architecture garantit un faible couplage et facilite les évolutions.

---

# Principes d'architecture

Le noyau respecte les principes suivants :

* responsabilité unique ;
* séparation entre modèle et état d'exécution ;
* communication par événements lorsque cela est pertinent ;
* dépendances orientées dans un seul sens ;
* composants indépendants ;
* testabilité maximale.

---

# État actuel

Le noyau comprend désormais :

* cycle de vie de l'application ;
* configuration ;
* EventBus ;
* Dispatcher ;
* Scheduler ;
* Runtime des plugins ;
* modèle d'infrastructure ;
* Runtime de l'infrastructure ;
* moteur d'observations ;
* calcul des capacités.

Le projet compte actuellement **706 tests unitaires**, tous validés.

---

# Évolutions prévues

Les prochaines évolutions du noyau sont :

* infrastructure déclarative (YAML) ;
* chargement automatique de l'infrastructure ;
* dépendances entre services ;
* calculs avancés des capacités ;
* historique des observations ;
* tableau de bord Web ;
* intégration native avec Home Assistant.

Le noyau est désormais suffisamment stable pour accueillir ces fonctionnalités sans remise en cause de son architecture.

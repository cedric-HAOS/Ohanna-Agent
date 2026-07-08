# ADR-0027 — Architecture du Plugin SDK

**Statut :** Acceptée

**Date :** 08/07/2026

## Contexte

L'objectif d'Ohanna-Agent est de garantir les capacités d'une infrastructure plutôt que de superviser des équipements.

Afin de permettre l'ajout de nouvelles capacités sans modifier le noyau, le projet introduit un SDK de plugins.

Cette architecture doit répondre à plusieurs contraintes :

* garantir la stabilité du noyau (*Shikamaru*) ;
* permettre le développement de plugins indépendants ;
* respecter les principes SOLID ;
* préparer les futures phases du projet (Dashboard Web, intégration Home Assistant, Marketplace).

Le SDK constitue donc une API publique stable entre le noyau et les extensions.

---

# Décision

Le système de plugins est organisé autour de composants spécialisés, chacun ayant une responsabilité unique.

## Plugin

Le `Plugin` représente le contrat minimal qu'un plugin doit implémenter.

Il expose :

* son manifeste (`PluginManifest`) ;
* sa méthode d'enregistrement (`register()`).

Un plugin ne dépend jamais directement de la classe `Application`.

---

## PluginContext

Les plugins reçoivent un `PluginContext`.

Ce contexte représente l'unique point d'entrée vers les services publics du noyau.

Il expose uniquement les interfaces autorisées :

* EventBus
* Scheduler
* Dispatcher
* Memory
* CapabilityManager
* Configuration
* Runtime

Le contexte est immuable.

Les plugins ne peuvent ni modifier sa structure, ni accéder directement aux composants internes de l'application.

---

## Protocoles publics

Le SDK expose uniquement des protocoles (`Protocol`).

Les plugins compilent contre ces interfaces et non contre les implémentations du noyau.

Cette approche permet :

* de préserver l'inversion des dépendances ;
* de garantir la stabilité de l'API publique ;
* de faire évoluer les implémentations internes sans impacter les plugins.

---

## PluginDiscovery

`PluginDiscovery` est responsable de la découverte des plugins disponibles.

Il parcourt les emplacements configurés et retourne une collection de `PluginDescriptor`.

Il ne réalise aucun chargement Python.

Il n'instancie aucun plugin.

---

## PluginDescriptor

Le `PluginDescriptor` décrit un plugin découvert.

Il contient notamment :

* son module ;
* son emplacement sur le disque ;
* son manifeste (lorsqu'il est disponible).

Il représente l'origine du plugin.

---

## PluginLoader

Le `PluginLoader` est responsable du chargement d'un plugin.

À partir d'un `PluginDescriptor`, il :

* importe le module ;
* appelle la fonction `create_plugin()` ;
* retourne une instance de `Plugin`.

Il ne gère ni l'enregistrement, ni les événements, ni le stockage.

---

## PluginRegistry

Le `PluginRegistry` constitue la source de vérité des plugins chargés.

Il assure uniquement le stockage des plugins.

Il fournit notamment :

* ajout ;
* suppression ;
* recherche ;
* énumération ;
* comptage.

Il ne contient aucune logique métier.

---

## PluginRuntime

Le `PluginRuntime` conserve l'état courant de chaque plugin.

Les états sont représentés par `PluginState`.

États initiaux :

* DISCOVERED
* LOADED
* REGISTERED
* FAILED
* UNLOADED

Le Runtime constitue la source officielle de l'état des plugins.

---

## PluginManager

Le `PluginManager` orchestre les différents composants.

Il coordonne :

* la découverte ;
* le chargement ;
* le registre ;
* le Runtime ;
* la publication des événements.

Il ne réalise aucun stockage interne.

---

# Architecture

```text
Application
      │
      ▼
PluginManager
      │
      ├───────────────┐
      │               │
      ▼               ▼
PluginRegistry   PluginRuntime
      ▲
      │
PluginLoader
      ▲
      │
PluginDiscovery
      ▲
      │
PluginDescriptor
```

Les plugins utilisent exclusivement le `PluginContext`.

Le noyau reste totalement indépendant des implémentations des plugins.

---

# Conséquences

## Avantages

* Découplage complet entre le noyau et les plugins.
* API publique stable.
* Architecture conforme aux principes SOLID.
* Tests unitaires simplifiés.
* Préparation naturelle du Dashboard Web.
* Préparation du Marketplace.
* Possibilité future de rechargement dynamique des plugins.
* Possibilité d'ajouter de nouveaux mécanismes de découverte sans modifier le Loader.

## Inconvénients

* Nombre de composants plus important.
* Architecture plus riche qu'un système de plugins minimaliste.
* Courbe d'apprentissage légèrement supérieure pour les développeurs de plugins.

Ces inconvénients sont jugés acceptables au regard des bénéfices apportés en matière de maintenabilité et d'évolutivité.

---

# Décisions associées

Cette ADR complète les décisions d'architecture précédentes concernant :

* le découplage du noyau ;
* l'EventBus ;
* le Scheduler ;
* le Runtime ;
* le système de capacités.

Elle constitue la référence officielle pour toute évolution future du SDK de plugins.

Aucun plugin ne devra accéder directement à la classe `Application`.

Toute nouvelle fonctionnalité du SDK devra respecter les responsabilités définies dans cette ADR.

# Changelog

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le projet suit les principes de **Keep a Changelog** et du **Semantic Versioning**.

---

# [v0.9.0] - 2026-07-08

## Sprint 10 — Public Plugin SDK

Cette version marque une évolution majeure de l'architecture d'Ohanna-Agent.

Le noyau (*Shikamaru*) devient une véritable plateforme extensible grâce à l'introduction d'un SDK public de plugins entièrement découplé du Core.

---

## Ajouté

### SDK public de plugins

Création du contrat de base des plugins :

* `Plugin`
* `PluginManifest`
* `PluginContext`

Les plugins ne dépendent plus directement de l'objet `Application`.

Ils utilisent désormais exclusivement le `PluginContext`, qui expose uniquement les services publics du noyau.

---

### Protocoles publics

Introduction des protocoles publics du SDK afin de découpler complètement les plugins des implémentations internes.

Les plugins compilent désormais contre des interfaces stables.

---

### Gestion des plugins

Création des nouveaux composants :

* `PluginRegistry`
* `PluginRuntime`
* `PluginDescriptor`
* `PluginDiscovery`
* `PluginLoader`
* `PluginFactory`

Chaque composant possède une responsabilité unique conformément aux principes SOLID.

---

### Découverte des plugins

Introduction d'une architecture extensible de découverte :

* `DiscoveryProvider`
* `LocalDirectoryProvider`

Cette architecture prépare l'ajout futur de nouvelles sources de plugins :

* Git
* ZIP
* HTTP
* Marketplace
* NAS

---

### Chargement des plugins

Le chargement des plugins est désormais entièrement découplé de leur découverte.

Le `PluginLoader` délègue l'instanciation à un `PluginFactory`, préparant ainsi l'arrivée de nouveaux mécanismes de chargement.

---

### Cycle de vie des plugins

Ajout du cycle de vie officiel :

* `DISCOVERED`
* `LOADED`
* `REGISTERED`
* `FAILED`
* `UNLOADED`

Le `PluginRuntime` devient la source de vérité concernant l'état d'exécution des plugins.

---

### Nouveau PluginManager

Refonte complète du `PluginManager`.

Il devient un orchestrateur chargé de coordonner :

* la découverte ;
* le chargement ;
* l'enregistrement ;
* le Runtime ;
* la publication des événements.

Toute logique de stockage est désormais externalisée.

---

### Tests

Ajout d'une couverture complète du SDK :

* Plugin
* PluginContext
* PluginManifest
* PluginDescriptor
* PluginRegistry
* PluginRuntime
* PluginDiscovery
* DiscoveryProvider
* LocalDirectoryProvider
* PluginLoader
* PluginFactory
* PluginManager

Ajout d'un test d'intégration validant la chaîne complète :

Filesystem → Discovery → Loader → Factory → Plugin → Registry → Runtime → Manager.

Le projet atteint désormais **502 tests unitaires**, tous validés.

---

### Documentation

Nouvelle ADR :

* ADR-0027 — Architecture du Plugin SDK

Mise à jour de :

* README
* Architecture du Core
* Roadmap

---

## Modifié

Refactorisation complète de l'architecture du système de plugins.

Les responsabilités sont désormais clairement séparées entre :

* découverte ;
* chargement ;
* stockage ;
* état d'exécution ;
* orchestration.

Le SDK constitue désormais l'API publique officielle d'Ohanna-Agent.

---

## Qualité

* Architecture entièrement découplée.
* Respect des principes SOLID.
* Injection de dépendances généralisée.
* API publique stable.
* Aucune dette technique majeure identifiée lors de l'audit du Sprint 10.

---

# [v0.8.0] - 2026-07-08

## Sprint 9 — EventBus & Architecture

* Finalisation de l'EventBus.
* Refonte des événements du Scheduler.
* Introduction des événements de mémoire.
* Amélioration de l'injection de dépendances.
* Renforcement de l'architecture hexagonale.
* Audit complet de l'architecture.
* Documentation mise à jour.

---

# [v0.7.0] - 2026-07-08

## Sprint 8 — Scheduler

* Finalisation du Scheduler.
* Introduction du `SchedulerRuntime`.
* Introduction du `SchedulerStatistics`.
* Nouveaux événements du Scheduler.
* Refactorisation du moteur d'exécution.

---

# [v0.6.0] - 2026-07-08

## Sprint 7 — Memory

* Introduction du `MemoryManager`.
* Ajout du stockage mémoire.
* Injection de dépendances complète.
* Nouveaux tests.

---

# [v0.5.0] - 2026-07-08

## Sprint 6 — Capability Engine

* Finalisation du moteur de capacités.
* Gestion des dépendances.
* États des capacités.
* Diagnostics.

---

# [v0.4.0] - 2026-07-08

## Sprint 5 — Auto-réparation

* Mise en place du moteur d'actions.
* Introduction des commandes.
* Stratégies de réparation.

---

# [v0.3.0] - 2026-07-08

## Sprint 4 — Runtime

* Création du Runtime.
* Introduction du Dispatcher.
* Refonte du cycle de vie.

---

# [v0.2.0] - 2026-07-07

## Sprint 2 & 3

* MQTT Runtime.
* Configuration.
* EventBus initial.
* Architecture documentaire.
* ADR.

---

# [v0.1.0] - 2026-07-07

## Sprint 0 & 1

Première version publique du projet.

Création du noyau Shikamaru.

Architecture logicielle.

Documentation initiale.

Premiers tests unitaires.

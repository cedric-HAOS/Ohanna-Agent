# ROADMAP

> Construire une plateforme capable de garantir durablement les capacités d'une infrastructure.

---

# Vision

Le développement d'Ohanna-Agent est organisé en grandes phases.

Chaque phase construit un niveau d'abstraction supplémentaire.

```
Core
    ↓
SDK
    ↓
Plugins
    ↓
Dashboard
    ↓
Home Assistant
    ↓
Marketplace
```

Le noyau (*Shikamaru*) évolue lentement.

Les fonctionnalités évoluent principalement sous forme de plugins.

---

# Phase 1 — Noyau Shikamaru

## Objectif

Construire un noyau stable, découplé et entièrement testable.

## État

**Terminée**

---

### Sprint 0

Architecture initiale

* Philosophie
* Architecture logicielle
* ADR
* Documentation
* Premiers tests

**Statut :** ✅ Terminé

---

### Sprint 1

Core

* Application
* Configuration
* Lifecycle
* Injection de dépendances

**Statut :** ✅ Terminé

---

### Sprint 2

Services fondamentaux

* EventBus
* Dispatcher
* Runtime
* Événements

**Statut :** ✅ Terminé

---

### Sprint 3

MQTT Runtime

* Publication
* Modèle de messages
* Architecture MQTT

**Statut :** ✅ Terminé

---

### Sprint 4

Auto-réparation

* Commandes
* Actions
* Moteur d'exécution

**Statut :** ✅ Terminé

---

### Sprint 5

Capability Engine

* Capacités
* Dépendances
* États
* Diagnostics

**Statut :** ✅ Terminé

---

### Sprint 6

Scheduler

* Scheduler
* Runtime
* Statistiques
* Événements

**Statut :** ✅ Terminé

---

### Sprint 7

Memory

* MemoryManager
* Injection de dépendances
* Persistance

**Statut :** ✅ Terminé

---

### Sprint 8

Architecture événementielle

* EventBus avancé
* Nouveaux événements
* Découplage

**Statut :** ✅ Terminé

---

### Sprint 9

Stabilisation du Core

* Audit
* Documentation
* Refactorisation
* Nettoyage

**Statut :** ✅ Terminé

---

### Sprint 10

Public Plugin SDK

* Plugin SDK
* PluginContext
* Protocoles publics
* PluginDiscovery
* DiscoveryProvider
* PluginDescriptor
* PluginLoader
* PluginFactory
* PluginRegistry
* PluginRuntime
* PluginManager
* ADR-0027

**Statut :** ✅ Terminé

---

# Phase 2 — Plugins métier

## Objectif

Développer les premières capacités réelles d'Ohanna-Agent.

Chaque capacité devient un plugin indépendant.

---

### Sprint 11

Plugin DNS

* Vérification DNS
* Résolution
* Temps de réponse
* Diagnostics

**Statut :** ⏳ Prévu

---

### Sprint 12

Plugin DHCP

* Vérification DHCP
* Attribution d'adresses
* Diagnostics

**Statut :** ⏳ Prévu

---

### Sprint 13

Plugin MQTT

* Broker
* Publication
* Souscription
* Boucle de validation

**Statut :** ⏳ Prévu

---

### Sprint 14

Plugin Docker

* Conteneurs
* Santé
* Redémarrage
* Diagnostics

**Statut :** ⏳ Prévu

---

### Sprint 15

Plugin Home Assistant

* API
* Santé
* Entités
* Services

**Statut :** ⏳ Prévu

---

### Sprint 16

Plugins réseau

* Ping
* HTTP
* HTTPS
* Reverse Proxy

**Statut :** ⏳ Prévu

---

### Sprint 17

Plugins système

* Sauvegardes
* Stockage
* Disques
* Certificats

**Statut :** ⏳ Prévu

---

# Phase 3 — Dashboard Web

## Objectif

Construire une interface Web totalement indépendante de Home Assistant.

Le Dashboard doit continuer à fonctionner même si Home Assistant est indisponible.

---

### Sprint 18

Serveur Web

* Backend HTTP
* API REST
* Authentification

---

### Sprint 19

Interface Web

* Plugins
* Capacités
* Diagnostics
* Runtime

---

### Sprint 20

Visualisation

* États
* Dépendances
* Historique
* Journal des événements

---

### Sprint 21

Administration

* Configuration
* Journaux
* Exécution d'actions
* Diagnostics avancés

---

# Phase 4 — Intégration Home Assistant

## Objectif

Exposer les informations du noyau dans Home Assistant.

Home Assistant devient un consommateur des données produites par Ohanna-Agent.

---

### Sprint 22

Intégration officielle

* Entités
* Diagnostics
* Services

---

### Sprint 23

Commandes

* Réparations
* Redémarrages
* Maintenance

---

### Sprint 24

Automatisations

* Événements
* Déclencheurs
* Notifications

---

# Phase 5 — Plateforme

## Objectif

Transformer Ohanna-Agent en plateforme d'extensions.

---

### Sprint 25

Marketplace

* Installation
* Désinstallation
* Mise à jour

---

### Sprint 26

Gestion des dépendances

* Compatibilité
* Versions
* Contraintes

---

### Sprint 27

Plugins distants

* Git
* HTTP
* ZIP

---

### Sprint 28

Sécurité

* Signatures
* Vérification
* Sandbox

---

# Améliorations transverses

Ces travaux pourront être réalisés entre plusieurs sprints.

* Optimisations des performances.
* Renforcement des diagnostics.
* Amélioration de la couverture de tests.
* Refactorisations internes.
* Documentation.
* ADR supplémentaires.
* Modernisation du code Python.
* Harmonisation des patterns (Registry / Runtime / Manager / Provider).

---

# Vision finale

À terme, Ohanna-Agent devra être capable de garantir automatiquement les capacités d'une infrastructure complète.

Le noyau restera volontairement stable.

Les nouvelles fonctionnalités seront principalement développées sous forme de plugins.

Cette approche permettra de faire évoluer le projet pendant de nombreuses années sans remettre en cause son architecture fondamentale.

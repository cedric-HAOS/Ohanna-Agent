# Ohanna-Agent

> Garantir les capacités d'une infrastructure, pas seulement surveiller ses composants.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/tests-502-success.svg)
![Architecture](https://img.shields.io/badge/architecture-hexagonal-blueviolet.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

# Vision

Une infrastructure fiable n'est pas simplement une infrastructure qui fonctionne.

C'est une infrastructure capable de **garantir durablement les services qu'elle fournit**, malgré les mises à jour, les pannes matérielles ou les changements de configuration.

Ohanna-Agent ne surveille pas des logiciels.

Il garantit des **capacités**.

Par exemple :

- DNS
- DHCP
- MQTT
- Home Assistant
- Sauvegardes
- Reverse Proxy
- Docker
- VPN
- Accès Internet

Chaque capacité possède son propre cycle de vie, son état, ses dépendances et sa stratégie de réparation.

Le noyau d'Ohanna-Agent orchestre ces capacités sans connaître leur implémentation.

---

# Philosophie

Le projet repose sur cinq principes fondamentaux :

- Architecture hexagonale
- Responsabilité unique (SRP)
- Inversion des dépendances
- Événements métier
- Extensibilité par plugins

Le noyau reste volontairement minimal et stable.

Toutes les fonctionnalités sont destinées à devenir des plugins.

---

# Architecture

```
                    Application
                          │
                          ▼
                   PluginManager
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 PluginDiscovery     PluginLoader     PluginRegistry
        │                 │                 │
        ▼                 ▼                 ▼
 DiscoveryProvider   PluginFactory    PluginRuntime
```

Le SDK de plugins constitue désormais l'API publique officielle d'Ohanna-Agent.

---

# Noyau actuel

Le noyau (*Shikamaru*) fournit les services suivants :

- EventBus
- Scheduler
- Dispatcher
- Runtime
- Memory
- Configuration
- Capability Manager
- Plugin SDK

Le noyau ne contient aucune logique métier spécifique à une capacité.

---

# Plugin SDK

Chaque plugin est totalement indépendant du noyau.

Il implémente simplement :

```python
class MyPlugin(Plugin):

    @property
    def manifest(self):
        ...

    def register(self, context):
        ...
```

Le plugin reçoit un `PluginContext` qui expose uniquement les services publics du noyau.

Il n'a jamais accès directement à l'objet `Application`.

---

# Cycle de vie d'un plugin

```
DISCOVERED
      │
      ▼
LOADED
      │
      ▼
REGISTERED
      │
      ▼
UNLOADED
```

L'état d'exécution est conservé dans le `PluginRuntime`.

---

# Découverte des plugins

Le SDK sépare clairement les responsabilités.

```
Filesystem
      │
      ▼
LocalDirectoryProvider
      │
      ▼
PluginDiscovery
      │
      ▼
PluginDescriptor
```

De nouveaux fournisseurs pourront être ajoutés sans modifier le noyau :

- Git
- ZIP
- HTTP
- Marketplace
- NAS

---

# Chargement des plugins

Le chargement est lui aussi découplé.

```
PluginDescriptor
        │
        ▼
PluginLoader
        │
        ▼
PluginFactory
        │
        ▼
Plugin
```

Le Loader orchestre uniquement le chargement.

Le Factory instancie les plugins.

---

# Capacités

Les capacités représentent les services garantis par Ohanna-Agent.

Exemples :

- DNS
- DHCP
- MQTT
- Home Assistant
- Docker
- Reverse Proxy
- Sauvegardes
- VPN
- Internet

Chaque capacité possède :

- un état
- des dépendances
- des diagnostics
- des actions correctives

---

# Organisation du projet

```
application/

capability/

configuration/

dispatcher/

eventbus/

memory/

plugin/

scheduler/

runtime/

tests/

docs/
```

Chaque module suit les mêmes principes d'architecture :

- Registry
- Runtime
- Manager

---

# Documentation

Le projet est accompagné d'une documentation complète :

- Architecture
- ADR
- Roadmap
- Changelog
- Philosophie
- Capacités
- MQTT
- Plugins
- Configuration

---

# Qualité

Le projet applique systématiquement :

- Ruff
- Pytest
- Architecture orientée événements
- Injection de dépendances
- Typage Python
- Documentation des décisions (ADR)

État actuel :

- **502 tests unitaires**
- **100 % des tests validés**
- **Aucune dette technique majeure identifiée**

---

# Roadmap

## Phase 1

✔ Noyau Shikamaru

✔ EventBus

✔ Scheduler

✔ Dispatcher

✔ Runtime

✔ Memory

✔ Capability Engine

✔ Plugin SDK

---

## Phase 2

Création des premiers plugins :

- DNS
- DHCP
- MQTT
- Docker
- Home Assistant

---

## Phase 3

Dashboard Web indépendant de Home Assistant.

---

## Phase 4

Intégration native Home Assistant.

---

# Objectif

À terme, Ohanna-Agent devra être capable de garantir automatiquement l'ensemble des capacités définies par l'architecture de référence d'Ohanna-House.

Le projet doit rester :

- modulaire ;
- extensible ;
- documenté ;
- testé ;
- indépendant des technologies qu'il supervise.

---

# État du projet

**Sprint 10 terminé**

- ✅ SDK public de plugins
- ✅ Architecture entièrement découplée
- ✅ 502 tests validés
- ✅ Architecture prête à accueillir les premiers plugins métier
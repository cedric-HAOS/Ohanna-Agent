# Ohanna-Agent

> **Un noyau d'agent intelligent, modulaire et événementiel, conçu pour être extensible, testable et indépendant des modèles d'IA.**

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/tests-438-success)
![Ruff](https://img.shields.io/badge/lint-ruff-success)
![Architecture](https://img.shields.io/badge/architecture-clean-success)
![License](https://img.shields.io/badge/license-MIT-green)

---

# Présentation

**Ohanna-Agent** est un framework Python permettant de construire des agents intelligents autonomes.

Le projet est conçu autour de plusieurs principes fondamentaux :

* Architecture modulaire
* Injection de dépendances
* Communication par événements
* Faible couplage entre les composants
* Forte couverture de tests
* Documentation d'architecture complète

Le noyau est totalement indépendant :

* des modèles d'IA
* des LLM
* des transports réseau
* des interfaces utilisateur

Il peut être utilisé aussi bien pour des assistants personnels que pour des agents industriels ou des services distribués.

---

# Philosophie

Ohanna-Agent suit plusieurs principes de conception :

* **Composition plutôt qu'héritage**
* **Injection de dépendances**
* **Architecture événementielle**
* **Faible couplage**
* **Haute testabilité**
* **Documentation avant implémentation**
* **Évolution incrémentale par sprints**

---

# Fonctionnalités actuelles

## Noyau

* Runtime
* Dispatcher de commandes
* Registre de services
* Gestionnaire de plugins
* Gestionnaire de mémoire
* Scheduler
* EventBus
* EventSubscription

---

## Mémoire

* Mémoire persistante
* Mémoire de session
* Mémoire runtime
* Sérialisation
* Statistiques
* Scopes mémoire

---

## Scheduler

* Tâches planifiées
* Déclencheurs OneShot
* Déclencheurs Interval
* Déclencheurs Cron
* Priorités
* Runtime
* Statistiques
* États

---

## Événements

Le noyau possède désormais un **EventBus** interne.

Les composants peuvent publier ou recevoir des événements sans dépendances directes.

Événements actuellement utilisés :

* ApplicationStarted
* ApplicationStopped
* ApplicationTicked
* CommandDispatched
* CommandSucceeded
* CommandFailed

Cette architecture prépare les futures intégrations :

* MQTT
* Monitoring
* WebSocket
* Interface graphique
* Plugins avancés

---

# Architecture

```text
                Application
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 CommandDispatcher  Scheduler     PluginManager
      │
      ▼
   EventBus
      │
 ┌────┼───────────────┐
 │    │               │
 ▼    ▼               ▼
Memory Plugins   Future Services
```

---

# Structure du projet

```text
application.py

core/
    dispatcher.py
    events.py
    event_subscription.py
    services.py
    plugins.py
    runtime.py

memory/

scheduler/

mqtt/

tests/

docs/
```

---

# Qualité

Le projet est développé avec une forte exigence de qualité.

## Vérifications automatiques

```bash
ruff check .
pytest
```

État actuel :

* **438 tests**
* **0 erreur Ruff**
* **100 % des tests réussis**

---

# Documentation

Le projet est accompagné d'une documentation complète.

* README
* CHANGELOG
* ROADMAP
* Documentation d'architecture
* ADR (Architecture Decision Records)

---

# Roadmap

Les prochaines évolutions prévues comprennent notamment :

* Événements avancés du Scheduler
* Monitoring
* Auto-réparation
* Capacités (Capabilities)
* MQTT avancé
* Plugins dynamiques
* Observabilité
* Métriques
* API HTTP
* Interface Web

---

# Installation

```bash
git clone https://github.com/<user>/Ohanna-Agent.git

cd Ohanna-Agent

python -m venv .venv

source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -e .

pytest
```

---

# Développement

Le projet suit une évolution incrémentale.

Chaque Sprint comprend :

* conception
* implémentation
* couverture de tests
* audit
* documentation

Cette méthode garantit une architecture stable tout au long du développement.

---

# État actuel

Version du noyau :

**Sprint 8 validé**

* Architecture événementielle en place
* EventBus opérationnel
* Dispatcher événementiel
* Injection de dépendances consolidée
* Documentation synchronisée
* 438 tests verts

---

# Licence

Projet distribué sous licence **MIT**.

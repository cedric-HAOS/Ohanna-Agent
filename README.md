# Ohanna-Agent

> **Un noyau d'agent IA modulaire, événementiel et extensible, conçu pour orchestrer des capacités, des services et des automatismes de manière fiable.**

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Tests](https://img.shields.io/badge/tests-453%20passed-success)
![Ruff](https://img.shields.io/badge/lint-ruff-success)
![Architecture](https://img.shields.io/badge/architecture-event--driven-blue)
![Version](https://img.shields.io/badge/version-v0.9.0-orange)

---

# Vision

Ohanna-Agent est un **framework de développement d'agents intelligents**.

Son objectif est de fournir un **Kernel robuste** capable d'orchestrer :

* des capacités (Capabilities),
* des services,
* des commandes,
* des workflows,
* de la mémoire,
* un ordonnanceur (Scheduler),
* un bus d'événements.

Le projet privilégie une architecture **simple, fortement testée et faiblement couplée**.

---

# Philosophie

Le Kernel ne contient aucune logique métier.

Il fournit uniquement les briques nécessaires à la construction d'agents spécialisés.

Chaque composant doit être :

* indépendant ;
* testable ;
* remplaçable ;
* découplé des autres composants.

Les interactions passent principalement par des événements afin de limiter les dépendances directes.

---

# Fonctionnalités

## Kernel

* Gestion du cycle de vie de l'application
* Dispatcher de commandes
* Gestion des capacités
* Gestion des services
* Injection des dépendances
* Architecture modulaire

## Runtime

* Runtime supervisé
* Heartbeat
* Watchdog
* Monitoring
* Statistiques d'exécution

## Memory

* Mémoire persistante
* Mémoire de session
* Mémoire d'exécution
* Sérialisation
* Statistiques
* Scopes mémoire

## Scheduler

* Déclencheurs OneShot
* Déclencheurs Interval
* Déclencheurs Cron
* Registre de tâches
* Exécution de tâches
* Statistiques
* Runtime dédié
* Scheduler événementiel

## EventBus

Le Scheduler est désormais totalement intégré au bus d'événements.

Événements publiés :

* SchedulerStarted
* SchedulerStopped
* SchedulerTicked
* ScheduledTaskTriggered
* ScheduledTaskExecuted
* ScheduledTaskFailed

Cette architecture permet d'observer l'activité du Scheduler sans créer de dépendance avec son implémentation.

---

# Architecture

```
                Application
                      │
     ┌────────────────┼────────────────┐
     │                │                │
 Dispatcher       EventBus         Memory
     │                ▲
     │                │
     └──────────── Scheduler
                      │
              Task Registry
                      │
               Task Executor
                      │
                 Triggers
```

Le Scheduler publie désormais tous ses événements via l'EventBus.

Les composants consommateurs restent totalement découplés.

---

# Qualité

Le projet est développé selon une approche **Test Driven Development (TDD)**.

État actuel :

* **453 tests automatisés**
* Ruff
* Typage Python moderne
* Dataclasses
* Architecture découplée
* Injection de dépendances

Chaque Sprint est validé uniquement lorsque :

* tous les tests passent ;
* aucune régression n'est détectée ;
* la qualité de code est conforme.

---

# Arborescence

```
application.py

core/
memory/
monitoring/
mqtt/
scheduler/
services/
tests/

docs/
```

---

# Installation

```bash
git clone https://github.com/<utilisateur>/Ohanna-Agent.git

cd Ohanna-Agent

python -m venv .venv

source .venv/bin/activate
```

Windows :

```powershell
.venv\Scripts\activate
```

Installation :

```bash
pip install -r requirements.txt
```

---

# Lancer les tests

```bash
pytest
```

---

# Vérification qualité

```bash
ruff check .
```

---

# État du projet

| Élément                | Statut |
| ---------------------- | :----: |
| Kernel                 |    ✅   |
| Runtime                |    ✅   |
| Memory                 |    ✅   |
| EventBus               |    ✅   |
| Scheduler              |    ✅   |
| Scheduler événementiel |    ✅   |
| MQTT Runtime           |    ✅   |
| Monitoring             |    ✅   |
| Tests                  |  ✅ 453 |

---

# Roadmap

Les prochaines évolutions prévues concernent notamment :

* Observabilité avancée
* Supervision Runtime
* SDK de plugins
* Workflows avancés
* Capacités IA
* Intégrations Home Assistant
* Intégrations MQTT

Voir le fichier **ROADMAP.md** pour le détail.

---

# Documentation

La documentation du projet est disponible dans le dossier :

```
docs/
```

Elle comprend notamment :

* Architecture du Kernel
* ADR
* Conventions
* Roadmap
* Changelog

---

# Licence

Ce projet est distribué sous licence MIT.

---

# Auteur

Projet développé dans le cadre de **Ohanna**, une plateforme modulaire destinée à la création d'agents intelligents, autonomes et extensibles.

# ROADMAP

> Feuille de route officielle du projet **Ohanna-Agent**

---

# Vision

Ohanna-Agent a pour objectif de devenir un framework Python modulaire permettant de développer des agents d'infrastructure autonomes.

Ces agents doivent être capables de :

- administrer des services réseau ;
- communiquer par événements ;
- s'intégrer nativement à MQTT ;
- superviser leur propre état ;
- détecter les anomalies ;
- tenter leur auto-réparation ;
- fonctionner en mode dégradé lorsque cela est nécessaire.

Le projet privilégie :

- une architecture propre ;
- une forte testabilité ;
- un faible couplage ;
- une documentation exhaustive ;
- une évolution progressive par Sprint.

---

# Philosophie

Chaque Sprint doit respecter les principes suivants :

- aucune régression ;
- architecture validée par ADR avant implémentation ;
- couverture systématique par des tests unitaires ;
- documentation synchronisée avec le code ;
- faible dette technique.

Chaque Sprint se termine par :

- revue de code ;
- audit d'architecture ;
- mise à jour de la documentation ;
- publication Git.

---

# État actuel

Version :

```text
4.0
```

État :

```text
Sprint 4 terminé
```

Tests :

```text
204 tests

204 réussis

0 échec
```

Qualité :

```text
Ruff

100 % conforme
```

---

# Historique

## Sprint 0

### Objectif

Définir les fondations du projet.

### Réalisations

- Vision
- Philosophie
- Architecture
- Capacités
- MQTT
- Plugins
- Configuration
- Documentation
- ADR

### Résultat

Architecture entièrement définie.

---

## Sprint 1

### Objectif

Construire le noyau Shikamaru.

### Réalisations

- Lifecycle
- Application
- Configuration
- Services
- Logger
- Initialisation
- Tests

### Résultat

Premier noyau fonctionnel.

---

## Sprint 2

### Objectif

Mettre en place les services internes.

### Réalisations

- Dispatcher
- Events
- Messages
- Scheduler
- Services
- Plugins

### Résultat

Architecture événementielle complète.

---

## Sprint 3

### Objectif

Implémenter le runtime MQTT.

### Réalisations

- MQTT Client
- Publisher
- Subscriber
- Transport
- Reconnexion automatique
- Messages MQTT

### Résultat

Communication MQTT native entièrement opérationnelle.

---

## Sprint 4

### Objectif

Rendre Shikamaru capable de superviser son état et de préparer son auto-réparation.

### ADR

- ADR-0015
- ADR-0016
- ADR-0017
- ADR-0018
- ADR-0019

### Réalisations

Package Health :

- Health Monitor
- Heartbeat
- Watchdog

Package Recovery :

- Recovery Engine
- Recovery Strategy
- Recovery Policy
- Recovery Action
- Recovery Result

Fonctionnalités :

- surveillance des composants ;
- agrégation de l'état de santé ;
- prévention des récupérations concurrentes ;
- historique des récupérations ;
- mode dégradé.

### Résultat

Le noyau possède désormais les fondations d'un véritable agent autonome.

---

# État de l'architecture

À la fin du Sprint 4 :

```text
Application

↓

Configuration

↓

Dispatcher

↓

Events

↓

MQTT Runtime

↓

Plugins

↓

Health Monitor

↓

Heartbeat

↓

Watchdog

↓

Recovery Engine

↓

Recovery Policy

↓

Recovery Strategy

↓

Recovery Action
```

Le noyau est maintenant entièrement modulaire.

Les futurs développements concerneront principalement les plugins métier.

---

# Sprint 5 — Plugins Infrastructure

## Objectif

Le Sprint 5 marque le début du développement des premiers plugins métier.

Jusqu'à présent, Shikamaru fournit uniquement le framework.

À partir de ce Sprint, il commencera à rendre des services concrets.

---

## Objectifs principaux

Développer les premiers plugins :

- DNS
- DHCP
- NTP
- Supervision système
- Découverte réseau

Chaque plugin devra :

- utiliser le Dispatcher ;
- publier ses événements ;
- enregistrer ses Health Checks ;
- déclarer ses Watchdogs ;
- fournir une Recovery Strategy.

---

## Livrables

### Plugin DNS

Fonctionnalités envisagées :

- résolution DNS
- cache
- statistiques
- supervision
- récupération automatique

---

### Plugin DHCP

Fonctionnalités envisagées :

- gestion des baux
- réservation d'adresses
- supervision
- événements
- récupération automatique

---

### Plugin NTP

Fonctionnalités envisagées :

- synchronisation
- contrôle de dérive
- supervision
- métriques

---

### Plugin Supervision

Fonctionnalités :

- CPU
- mémoire
- disque
- température
- charge système

---

### Découverte réseau

Première version de :

- découverte automatique
- inventaire réseau
- publication MQTT

---

# Sprint 6 — Intégration Home Assistant

## Objectif

Faire d'Ohanna-Agent un composant natif de Home Assistant.

---

## Fonctionnalités

- MQTT Discovery
- Entités
- Diagnostics
- Services Home Assistant
- Device Information
- Availability

---

## Entités prévues

- État de santé
- Plugins
- CPU
- RAM
- Uptime
- Version
- Recovery
- Watchdogs

---

## Services

- Restart Plugin
- Reload Plugin
- Enable Plugin
- Disable Plugin
- Run Health Check
- Trigger Recovery

---

# Sprint 7 — Interface Web

## Objectif

Créer une interface Web légère permettant de superviser Shikamaru.

---

## Tableau de bord

Visualisation :

- état global
- plugins
- MQTT
- Health Monitor
- Watchdogs
- Recoveries

---

## Plugins

Vue détaillée :

- version
- état
- configuration
- statistiques

---

## Health

Affichage :

- Health Checks
- Heartbeats
- Watchdogs
- historique

---

## Recovery

Visualisation :

- tentatives
- historique
- actions
- stratégies

---

# Sprint 8 — Supervision avancée

## Objectif

Renforcer les capacités d'observation.

---

## Fonctionnalités

- métriques
- statistiques
- historique
- alertes
- journal des événements

---

## Métriques prévues

Application :

- uptime
- mémoire
- CPU
- threads

Plugins :

- état
- temps de réponse
- nombre d'erreurs

MQTT :

- publications
- abonnements
- reconnexions

Recovery :

- nombre de recoveries
- temps moyen
- taux de réussite

---

## Alertes

Détection :

- watchdog expiré
- plugin arrêté
- erreur critique
- mode dégradé
- récupération impossible

---

# Sprint 9 — Haute disponibilité

## Objectif

Préparer Ohanna-Agent à fonctionner dans des architectures distribuées.

Le noyau devra être capable de collaborer avec d'autres instances afin d'assurer la continuité de service.

---

## Fonctionnalités

### Agents distribués

Plusieurs instances de Shikamaru pourront coopérer.

Exemples :

- serveur principal ;
- serveur secondaire ;
- Raspberry Pi ;
- machine virtuelle.

---

### Synchronisation

Les agents devront partager :

- leur état ;
- leurs capacités ;
- leur santé ;
- leurs événements.

---

### Réplication

Les composants critiques pourront être répliqués.

Exemples :

- configuration ;
- plugins ;
- états internes.

---

### Tolérance aux pannes

En cas d'arrêt d'un agent :

- détection automatique ;
- redistribution des services ;
- maintien du fonctionnement global.

---

# Sprint 10 — Version 1.0

## Objectif

Publier la première version stable d'Ohanna-Agent.

Cette version devra être utilisable en production.

---

## Critères

Architecture :

- stable ;
- documentée ;
- testée.

Code :

- fortement typé ;
- conforme Ruff ;
- documenté.

Tests :

- couverture importante ;
- aucune régression.

Documentation :

- complète ;
- synchronisée avec le code ;
- ADR à jour.

---

# Vision à long terme

À terme, Ohanna-Agent devra être capable de piloter un ensemble de services d'infrastructure.

Exemples :

- DNS
- DHCP
- NTP
- Reverse Proxy
- VPN
- MQTT
- Monitoring
- Découverte réseau
- Sauvegardes
- Home Assistant

Chaque service restera implémenté sous forme de plugin indépendant.

---

# Dette technique

Le projet suit une politique stricte de maîtrise de la dette technique.

## Autorisée

- amélioration de l'API ;
- simplification du code ;
- optimisation des performances ;
- refactoring documenté.

---

## Refusée

- duplication de code ;
- dépendances circulaires ;
- contournement des ADR ;
- fonctionnalités non testées.

---

# Indicateurs de qualité

Chaque Sprint est évalué selon les critères suivants.

## Architecture

- séparation des responsabilités ;
- faible couplage ;
- extensibilité.

---

## Qualité

- Ruff sans erreur ;
- tests unitaires ;
- documentation.

---

## Documentation

Tous les documents doivent évoluer en même temps que le code.

Documents concernés :

- README.md
- ROADMAP.md
- CORE.md
- CHANGELOG.md

Les ADR restent la référence architecturale du projet.

---

# Vision Version 1.0

La version 1.0 devra fournir :

## Framework

- architecture modulaire ;
- système d'événements ;
- MQTT natif ;
- scheduler ;
- services partagés.

---

## Supervision

- Health Monitor ;
- Heartbeat ;
- Watchdog ;
- métriques.

---

## Résilience

- Recovery Engine ;
- Recovery Policies ;
- Recovery Strategies ;
- auto-réparation ;
- mode dégradé.

---

## Plugins

Premiers plugins officiels :

- DNS
- DHCP
- NTP
- Supervision

---

## Home Assistant

- MQTT Discovery ;
- diagnostics ;
- services ;
- entités.

---

## Qualité

Objectifs minimums :

```text
Python 3.13

Architecture documentée

ADR validées

Documentation complète

250+ tests unitaires

Ruff 100 %

Version stable

Publication GitHub Release v1.0
```

---

# Conclusion

La feuille de route d'Ohanna-Agent est volontairement progressive.

Chaque Sprint apporte une évolution fonctionnelle tout en préservant les principes fondamentaux du projet :

- architecture claire ;
- faible couplage ;
- forte testabilité ;
- documentation synchronisée ;
- qualité du code.

À l'issue du Sprint 4, Shikamaru dispose désormais des fondations d'un **framework d'agents autonomes**.

Les prochains Sprints seront principalement consacrés au développement des plugins d'infrastructure et à leur intégration dans un environnement complet, jusqu'à la publication de la version **1.0**.
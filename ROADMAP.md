# ROADMAP

## Vision

L'objectif d'**Ohanna-Agent** est de devenir un noyau d'agent intelligent, modulaire, événementiel et extensible, capable de fonctionner de manière autonome, distribuée ou intégrée à différents écosystèmes (MQTT, HTTP, Home Assistant, LLM, etc.).

Les développements sont réalisés par sprints successifs, chaque sprint devant respecter les principes suivants :

* Architecture propre (Clean Architecture)
* Faible couplage
* Forte cohésion
* Couverture de tests exhaustive
* Documentation systématiquement mise à jour
* Évolution incrémentale sans régression

---

# État actuel

## Sprint 8 — Terminé ✅

Le noyau est désormais basé sur une **architecture événementielle**.

### Réalisations

* EventBus
* EventSubscription
* Injection du EventBus dans l'Application
* Dispatcher événementiel
* Événements applicatifs
* ServiceRegistry enrichi
* 438 tests automatisés
* Ruff conforme

---

# Sprint 9 — Scheduler événementiel

Objectif :

Intégrer le Scheduler dans l'architecture événementielle existante sans modifier son fonctionnement interne.

### Prévu

* Publication des événements Scheduler
* Cycle de vie du Scheduler
* Exécution des tâches
* Événements de déclenchement
* Événements d'erreur
* Intégration complète avec l'EventBus

---

# Sprint 10 — Monitoring

Objectif :

Introduire l'observabilité du noyau.

### Prévu

* Collecte des événements système
* Métriques runtime
* Statistiques globales
* Santé des composants
* Journalisation centralisée

---

# Sprint 11 — Auto-réparation avancée

Objectif :

Permettre au noyau de réagir automatiquement aux anomalies.

### Prévu

* Détection d'erreurs
* Redémarrage automatique de composants
* Stratégies de récupération
* Surveillance permanente
* Politiques de réparation

---

# Sprint 12 — Capacités avancées

Objectif :

Faire évoluer le système de capacités.

### Prévu

* Chargement dynamique
* Dépendances complexes
* Priorités
* Conditions d'activation
* Désactivation automatique

---

# Sprint 13 — MQTT avancé

Objectif :

Faire du bus MQTT un véritable transport distribué.

### Prévu

* Synchronisation entre agents
* Découverte automatique
* Publication distribuée
* Haute disponibilité
* Résilience réseau

---

# Sprint 14 — Plugins dynamiques

Objectif :

Permettre le chargement et le déchargement de plugins à chaud.

### Prévu

* Découverte automatique
* Cycle de vie complet
* Isolation
* Gestion des dépendances
* Validation

---

# Sprint 15 — API

Objectif :

Ouvrir le noyau vers l'extérieur.

### Prévu

* API REST
* API WebSocket
* Authentification
* Documentation OpenAPI
* Gestion des erreurs

---

# Sprint 16 — Interface Web

Objectif :

Créer une interface d'administration.

### Prévu

* Tableau de bord
* Monitoring
* Gestion des plugins
* Gestion de la mémoire
* Visualisation des événements

---

# Sprint 17 — Intelligence

Objectif :

Préparer l'intégration de moteurs d'IA.

### Prévu

* Gestionnaire de modèles
* Sélection dynamique des LLM
* Historique des conversations
* Mémoire contextuelle
* Routage intelligent

---

# Sprint 18 — Distribution

Objectif :

Permettre le fonctionnement d'un réseau d'agents.

### Prévu

* Fédération d'agents
* Synchronisation
* Élection
* Répartition de charge
* Communication sécurisée

---

# Objectifs transverses

Ces objectifs sont poursuivis tout au long du développement :

## Qualité

* Ruff sans avertissement
* Couverture de tests en augmentation constante
* Régression interdite

## Documentation

Chaque sprint met systématiquement à jour :

* README
* CHANGELOG
* Documentation d'architecture
* ADR concernés

## Architecture

Maintenir :

* Faible couplage
* Injection de dépendances
* Communication par événements
* Composants indépendants
* Interfaces simples

---

# Vision à long terme

À terme, Ohanna-Agent devra constituer un **noyau universel d'agents intelligents**, capable de fonctionner :

* sur une machine unique ;
* dans un réseau local ;
* dans une architecture distribuée ;
* avec ou sans modèle d'IA ;
* avec différents transports de communication ;
* tout en conservant une architecture simple, testable et maintenable.

Chaque sprint devra renforcer cette vision sans compromettre la stabilité du noyau.

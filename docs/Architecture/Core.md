# Core

> **Le Core ne fait rien. Le Core orchestre tout.**

---

# Objectif

Le Core constitue le cœur de **Shikamaru**.

Il est responsable du cycle de vie de l'agent et de la coordination des composants principaux.

Le Core ne contient aucune logique métier.

Son rôle est exclusivement d'orchestrer le fonctionnement de l'application.

---

# Philosophie

Chaque composant possède une responsabilité unique.

Le Core ne réalise jamais directement le travail d'un composant.

Il demande simplement aux composants d'effectuer leur propre travail.

Cette séparation garantit :

- un faible couplage ;
- une architecture lisible ;
- une excellente testabilité ;
- une évolution progressive du projet.

---

# Principe fondamental

Le Core applique le principe :

> **Le Core ne fait rien. Le Core orchestre tout.**

Exemples :

✔ Le Core demande au composant MQTT de se connecter.

✔ Le Core demande au composant Plugins de charger les plugins.

✔ Le Core demande au composant Health de publier son état.

En revanche :

✘ Le Core ne publie jamais directement un message MQTT.

✘ Le Core ne lit jamais directement un fichier YAML.

✘ Le Core n'exécute jamais un plugin.

---

# Architecture

```
                    Application
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
     Config            Logger          Lifecycle
                                              │
                     ┌────────────┬────────────┴────────────┐
                     │            │                         │
                   MQTT        Plugins                  Health
```

La classe `Application` constitue le point d'entrée unique du Core.

---

# Les composants du Core

## Application

Chef d'orchestre de l'application.

Responsabilités :

- créer les composants principaux ;
- initialiser l'application ;
- lancer l'exécution ;
- arrêter proprement l'application ;
- superviser le cycle de vie.

Elle ne réalise jamais le travail spécifique des composants.

---

## Lifecycle

Responsable de l'état global de l'application.

Il expose les différents états définis dans :

- ADR-0001 — Lifecycle

Il permet à tous les composants de connaître l'état courant de Shikamaru.

---

## Config

Responsable du chargement de la configuration.

Il centralise l'accès à tous les paramètres de l'application.

Le Core ne lit jamais directement un fichier YAML.

---

## Logger

Responsable de la journalisation.

Tous les composants utilisent le même logger.

Le Core ne produit pas directement de sortie console.

---

# Cycle de vie

Le cycle de vie est entièrement défini par :

ADR-0001 — Lifecycle

Le Core applique ce cycle sans le modifier.

```
CREATED
    │
INITIALIZING
    │
READY
    │
RUNNING
    │
STOPPING
    │
STOPPED

ERROR
```

---

# Séquence d'exécution

Au démarrage :

```
Application

↓

INITIALIZING

↓

Config

↓

Logger

↓

MQTT

↓

Plugins

↓

Health

↓

READY

↓

RUNNING
```

À l'arrêt :

```
RUNNING

↓

STOPPING

↓

Plugins

↓

MQTT

↓

Logger

↓

STOPPED
```

L'ordre d'arrêt est volontairement l'inverse de l'ordre d'initialisation.

---

# Communication

Les composants ne communiquent jamais directement entre eux.

Exemple interdit :

```
MQTT
   │
   ▼
Plugin
```

Exemple autorisé :

```
Plugin

↓

Application

↓

MQTT
```

Cette règle réduit fortement le couplage entre les modules.

---

# Dépendances

Les dépendances autorisées sont :

```
Application

↓

Config

↓

Logger

↓

Lifecycle

↓

MQTT

↓

Plugins

↓

Health
```

Les dépendances circulaires sont interdites.

Un composant ne doit jamais créer un autre composant.

---

# Règles d'architecture

Le Core applique les principes suivants.

## Responsabilité unique

Chaque composant possède une responsabilité clairement définie.

---

## Orchestration

Le Core coordonne.

Les composants exécutent.

---

## Simplicité

La solution retenue doit être la plus simple répondant au besoin.

La complexité n'est introduite que lorsqu'elle résout un problème réel.

---

## Extensibilité

L'ajout d'un nouveau composant ne doit pas nécessiter de modifier les composants existants.

Seule `Application` est responsable de son intégration.

---

# Évolutions prévues

Le Core accueillera progressivement :

- Scheduler
- Memory
- AI
- MCP
- HTTP API
- CLI
- Web UI

Ces composants devront respecter les principes décrits dans ce document.

---

# Références

- ADR-0001 — Lifecycle
- ADR-0002 — Application
- ADR-0003 — Composition
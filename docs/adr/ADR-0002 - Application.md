# ADR-0002 — Application

**Statut :** Accepté
**Version :** 1.0
**Date :** 2026-07-07
**Décideurs :** Cédric Harnois, ChatGPT

---

# Objectif

Définir le rôle de la classe `Application`.

Cette classe constitue le cœur de Shikamaru.

Elle orchestre le fonctionnement de l'ensemble de l'agent sans réaliser elle-même le travail métier des différents composants.

---

# Contexte

Shikamaru est conçu comme un agent modulaire.

Au fil de son évolution, il intégrera notamment :

- MQTT
- Plugins
- Scheduler
- IA
- MCP
- Mémoire
- API HTTP
- CLI
- Web UI

Sans une architecture claire, ces composants risqueraient de devenir fortement couplés les uns aux autres.

Il est donc nécessaire de disposer d'un point central de coordination.

---

# Décision

La classe `Application` est le chef d'orchestre de Shikamaru.

Elle possède les composants principaux de l'application.

Elle contrôle leur cycle de vie.

Elle coordonne leurs interactions.

Elle ne réalise jamais directement le travail spécifique de ces composants.

---

# Responsabilités

La classe `Application` est responsable de :

- créer les composants principaux ;
- initialiser l'application ;
- lancer l'exécution ;
- arrêter proprement l'application ;
- gérer le cycle de vie global ;
- superviser l'état général de l'agent.

---

# Non-responsabilités

La classe `Application` ne doit jamais :

- publier directement sur MQTT ;
- traiter un message MQTT ;
- charger un fichier YAML ;
- exécuter un plugin ;
- effectuer des calculs métier ;
- gérer la mémoire ;
- prendre des décisions liées à l'IA.

Ces responsabilités appartiennent aux composants spécialisés.

---

# API publique

La seule interface publique de la classe est :

```python
app.initialize()

app.run()

app.stop()
```

Aucune autre méthode ne doit être utilisée par les composants externes.

---

# Architecture

```
                   Application
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    Configuration      Logger        Lifecycle
                                            │
            ┌──────────────┬───────────────┬───────────────┐
            │              │               │               │
          MQTT          Plugins         Health        Scheduler
                                                (Sprint futur)
```

Tous les composants appartiennent à `Application`.

Les composants ne se connaissent pas directement.

Toute coordination passe par `Application`.

---

# Communication

Les composants ne doivent pas communiquer directement entre eux.

Exemple :

❌

```
MQTT → Plugin
```

❌

```
Plugin → Health
```

✔

```
Plugin
    │
    ▼
Application
    │
    ▼
MQTT
```

Cette règle limite le couplage entre les modules.

---

# Cycle de vie

Le cycle de vie est défini dans :

ADR-0001 — Lifecycle

La classe `Application` est seule responsable des transitions entre les états.

---

# Extensibilité

L'ajout d'un nouveau composant ne nécessite pas de modification des composants existants.

Seule la classe `Application` est responsable de son intégration.

Exemple :

Aujourd'hui :

```
Application
    ├── MQTT
    ├── Plugins
    └── Health
```

Demain :

```
Application
    ├── MQTT
    ├── Plugins
    ├── Health
    ├── Scheduler
    ├── Memory
    ├── MCP
    └── AI
```

Les composants déjà existants restent inchangés.

---

# Conséquences

Cette architecture apporte :

- un faible couplage ;
- une forte cohérence ;
- une meilleure testabilité ;
- une maintenance facilitée ;
- une évolution progressive de Shikamaru.

---

# Alternatives étudiées

## Architecture procédurale

```
main.py

↓

Logger

↓

MQTT

↓

Plugins
```

Cette approche fonctionne pour un petit projet mais devient difficile à maintenir lorsque le nombre de composants augmente.

Elle est rejetée.

---

## Communication directe entre composants

```
MQTT
   │
   ▼
Plugins
   │
   ▼
Health
```

Cette architecture crée de nombreuses dépendances croisées.

Elle est rejetée.

---

## Chef d'orchestre (choix retenu)

```
                 Application

      ↓        ↓        ↓

   MQTT   Plugins   Health
```

Cette architecture centralise la coordination tout en conservant des composants indépendants.

Elle est retenue.

---

# Évolutions possibles

À terme, `Application` pourra devenir le point d'entrée unique pour :

- une interface Web ;
- une API REST ;
- une interface CLI ;
- un superviseur externe ;
- des tests d'intégration.

Son interface publique devra cependant rester volontairement minimale afin de préserver la simplicité de son utilisation.
# ADR-0021 — Capability Manager

- **Statut** : Accepté
- **Date** : 2026-07-08
- **Décideurs** : Équipe Ohanna-Agent
- **Version cible** : v0.4.0

---

# Contexte

L'ADR-0020 introduit la notion de **Capability** comme unité fonctionnelle principale d'Ohanna-Agent.

Le noyau ne manipule désormais plus directement les plugins, mais des capacités représentant les fonctionnalités offertes par l'agent.

Il devient donc nécessaire d'introduire un composant chargé de gérer leur cycle de vie et leur orchestration.

---

# Problème

Sans composant dédié :

- les capacités seraient gérées directement par l'Application ;
- plusieurs composants pourraient modifier leur état ;
- l'enregistrement des capacités ne serait pas centralisé ;
- la découverte des fonctionnalités deviendrait difficile ;
- les futures fonctionnalités (API REST, supervision, interface Web) devraient chacune maintenir leur propre représentation des capacités.

Cette approche augmenterait fortement le couplage.

---

# Décision

Ohanna-Agent introduit un nouveau Core Service nommé **CapabilityManager**.

Le CapabilityManager devient l'unique responsable de la gestion des Capabilities.

Toutes les interactions avec une Capability passent par ce composant.

---

# Responsabilités

Le CapabilityManager est responsable de :

- enregistrer les capacités ;
- supprimer une capacité ;
- rechercher une capacité ;
- retourner la liste des capacités ;
- démarrer une capacité ;
- arrêter une capacité ;
- redémarrer une capacité ;
- surveiller leur état ;
- exposer leur état au reste du système.

Il constitue le point d'entrée unique du noyau.

---

# Architecture

```text
                +----------------------+
                |     Application      |
                +----------+-----------+
                           |
                  CapabilityManager
                           |
        +------------------+------------------+
        |                  |                  |
      DNS               MQTT           Home Assistant
        |                  |                  |
     Plugin A          Plugin B          Plugin C
```

Le noyau ne manipule jamais directement les plugins.

---

# Principe

Le CapabilityManager connaît les Capabilities.

Les Capabilities connaissent leur implémentation.

Les plugins ne connaissent pas le reste du système.

Cette séparation réduit fortement le couplage.

---

# Interface publique

Le CapabilityManager expose une API homogène.

Exemples :

```python
register(capability)

unregister(capability_id)

get(capability_id)

list()

start(capability_id)

stop(capability_id)

restart(capability_id)

exists(capability_id)
```

Cette interface constitue l'API officielle de gestion des capacités.

---

# Enregistrement

Chaque Capability possède un identifiant unique.

Exemple :

```text
dns

mqtt

dhcp

monitoring

home_assistant
```

Toute tentative d'enregistrer deux fois le même identifiant provoque une erreur.

---

# États

Le CapabilityManager ne définit pas les états.

Il s'appuie sur ceux exposés par chaque Capability.

Il fournit simplement un accès centralisé.

---

# Recherche

Le CapabilityManager permet notamment :

- rechercher une capacité par identifiant ;
- récupérer toutes les capacités ;
- récupérer uniquement les capacités actives ;
- récupérer les capacités en erreur ;
- récupérer les capacités selon leur état de santé.

Ces opérations seront utilisées par :

- l'interface Web ;
- l'API REST ;
- la supervision ;
- l'auto-réparation.

---

# Observabilité

Toutes les informations concernant une Capability transitent par le CapabilityManager.

Il devient ainsi possible de produire facilement :

- un inventaire des capacités ;
- leur état ;
- leur santé ;
- leur version ;
- leurs dépendances.

---

# Cycle de vie

Le CapabilityManager délègue le cycle de vie à chaque Capability.

Il orchestre uniquement les appels.

Exemple :

```text
register()

↓

initialize()

↓

start()

↓

running()

↓

stop()

↓

unregister()
```

Le détail de ce cycle de vie est défini dans l'ADR-0024.

---

# Conséquences

## Avantages

- responsabilité unique ;
- découplage fort ;
- API homogène ;
- supervision simplifiée ;
- meilleure extensibilité ;
- base solide pour les futures API ;
- orchestration centralisée.

---

## Inconvénients

- ajout d'un Core Service supplémentaire ;
- légère complexité supplémentaire.

---

# Alternatives étudiées

## Gérer les capacités directement dans l'Application

Rejeté.

L'Application ne doit pas devenir un point central contenant toute la logique métier.

---

## Confier cette responsabilité au PluginManager

Rejeté.

Le PluginManager gère les implémentations techniques.

Le CapabilityManager gère les fonctionnalités offertes.

Les responsabilités sont différentes.

---

## Utiliser un registre global

Rejeté.

Une variable globale ne permet pas d'encapsuler les règles métier.

---

# Conséquences sur l'architecture

Le CapabilityManager devient un Core Service permanent.

L'architecture devient :

```text
Application
│
├── EventBus
├── Dispatcher
├── MQTT
├── HealthManager
├── PluginManager
└── CapabilityManager
        │
        ├── DNS
        ├── DHCP
        ├── MQTT
        ├── Monitoring
        └── Home Assistant
```

Toutes les interactions avec les fonctionnalités passent désormais par lui.

---

# ADR associés

- ADR-0020 — Capability Model
- ADR-0022 — Dependency Resolution
- ADR-0023 — Plugin Discovery
- ADR-0024 — Capability Lifecycle

---

# Décision finale

Le **CapabilityManager** devient le gestionnaire officiel des fonctionnalités d'Ohanna-Agent.

Il constitue le point d'entrée unique permettant au noyau de découvrir, enregistrer, rechercher et orchestrer les Capabilities.

Cette décision garantit une architecture faiblement couplée, extensible et cohérente avec les principes du noyau **Shikamaru**.
# ADR-0020 — Capability Model

- **Statut** : Accepté
- **Date** : 2026-07-08
- **Décideurs** : Équipe Ohana-Agent
- **Version cible** : v0.4.0

---

# Contexte

Depuis les premiers sprints, Ohana-Agent s'est progressivement doté des services fondamentaux nécessaires à son fonctionnement :

- Lifecycle
- Configuration
- Event Bus
- Dispatcher
- MQTT Runtime
- Plugin Manager
- Health Manager
- Auto-Réparation

Ces composants constituent le **noyau technique (Shikamaru)** de l'agent.

En revanche, le noyau ne possède pas encore de représentation explicite des fonctionnalités qu'il met à disposition.

Aujourd'hui, les plugins sont les seules unités d'extension connues du système.

Cette approche présente plusieurs limites :

- un plugin peut fournir plusieurs fonctionnalités ;
- plusieurs plugins peuvent fournir la même fonctionnalité ;
- les dépendances sont exprimées entre plugins plutôt qu'entre services réellement rendus ;
- le noyau reste indirectement couplé aux implémentations.

Pour préparer les prochaines évolutions (API REST, interface Web, supervision avancée, architecture distribuée), il est nécessaire d'introduire une abstraction représentant les fonctionnalités offertes par l'agent.

---

# Problème

Le plugin n'est pas une bonne unité fonctionnelle.

Il représente une implémentation technique.

À l'inverse, les utilisateurs et les autres composants raisonnent en termes de services :

- DNS
- DHCP
- MQTT
- Home Assistant
- Supervision
- NTP

Le noyau doit donc manipuler ces services sans connaître leur implémentation.

---

# Décision

Ohana-Agent adopte un modèle orienté **Capability**.

Une **Capability** représente une fonctionnalité métier offerte par l'agent, indépendamment de son implémentation technique.

Les plugins deviennent uniquement des fournisseurs de capacités.

Le noyau ne manipule plus directement les plugins pour fournir des fonctionnalités.

Il manipule exclusivement des capacités.

---

# Définition

Une Capability est une représentation logique d'une fonctionnalité du système.

Elle possède une identité propre, un cycle de vie, un état de santé et des métadonnées permettant son orchestration.

Une Capability n'est ni un plugin, ni un service interne du noyau.

Elle constitue une couche d'abstraction entre les deux.

---

# Architecture

```text
                 +-----------------------+
                 |      Application      |
                 +-----------+-----------+
                             |
                      Core Services
                             |
        +--------------------+--------------------+
        |                    |                    |
 PluginManager      CapabilityManager      HealthManager
        |
        |
      Plugins
        |
        +-------------------------------+
        |                               |
   Capability DNS                 Capability MQTT
        |
        |
 Implémentation réelle
```

Le noyau ne dépend jamais d'une implémentation particulière.

---

# Caractéristiques d'une Capability

Chaque Capability possède au minimum :

- un identifiant unique ;
- un nom ;
- une version ;
- une description ;
- un état d'exécution ;
- un état de santé ;
- une configuration ;
- une liste de dépendances ;
- une liste de commandes ;
- une liste d'événements.

Elle constitue l'unité fonctionnelle manipulée par le noyau.

---

# Responsabilités

Une Capability est responsable de :

- représenter une fonctionnalité métier ;
- exposer son état courant ;
- publier ses événements ;
- déclarer ses commandes ;
- déclarer ses dépendances ;
- exposer son état de santé ;
- fournir des métadonnées descriptives.

Elle n'est pas responsable :

- du chargement dynamique ;
- de la découverte des plugins ;
- de l'orchestration globale ;
- de la résolution des dépendances.

Ces responsabilités appartiennent aux services du noyau.

---

# Relations

Le modèle distingue désormais trois niveaux.

## Core Services

Les Core Services constituent l'infrastructure du noyau.

Exemples :

- Event Bus
- Dispatcher
- MQTT Runtime
- Health Manager
- Plugin Manager
- Capability Manager

Ils ne représentent pas des fonctionnalités utilisateur.

---

## Plugins

Les plugins sont des modules techniques.

Ils contiennent le code permettant d'implémenter une ou plusieurs capacités.

Ils peuvent être remplacés sans modifier le noyau.

---

## Capabilities

Les Capabilities représentent les fonctionnalités offertes.

Exemples :

- DNS
- DHCP
- MQTT
- Home Assistant
- Monitoring
- NTP

Le noyau manipule exclusivement ces objets.

---

# Principes d'architecture

Le modèle repose sur plusieurs principes fondamentaux.

## Découplage

Le noyau ne dépend jamais d'une implémentation particulière.

---

## Abstraction

Toutes les interactions fonctionnelles passent par les Capabilities.

---

## Substituabilité

Plusieurs plugins peuvent fournir la même Capability.

Le noyau n'a pas connaissance de l'implémentation utilisée.

---

## Extensibilité

Une nouvelle fonctionnalité peut être ajoutée sans modifier le noyau.

---

## Observabilité

Toutes les capacités exposent leur état et leur santé de manière uniforme.

---

## Orchestration

Les futures fonctionnalités d'orchestration seront réalisées au niveau des Capabilities et non des plugins.

---

# Exemple

Un plugin AdGuard peut fournir :

```text
Plugin AdGuard

└── Capability DNS
```

Un plugin Bind9 peut également fournir :

```text
Plugin Bind9

└── Capability DNS
```

Pour le noyau, il n'existe qu'une seule fonctionnalité :

```text
DNS
```

L'implémentation reste transparente.

---

# Conséquences

## Avantages

- séparation claire entre fonctionnalités et implémentations ;
- découplage fort du noyau ;
- architecture orientée services métier ;
- supervision homogène ;
- découverte automatique simplifiée ;
- remplacement transparent des implémentations ;
- meilleure évolutivité ;
- préparation des futures API REST ;
- préparation de l'interface Web ;
- préparation d'une architecture distribuée.

---

## Inconvénients

- ajout d'une couche d'abstraction supplémentaire ;
- architecture plus riche ;
- nécessité d'un CapabilityManager dédié.

---

# Alternatives étudiées

## Utiliser directement les plugins

Rejeté.

Les plugins représentent des implémentations techniques et non des fonctionnalités.

---

## Utiliser uniquement les services du noyau

Rejeté.

Les services internes n'ont pas vocation à représenter les capacités offertes à l'utilisateur.

---

## Utiliser les événements comme unité fonctionnelle

Rejeté.

Les événements décrivent des échanges entre composants mais ne représentent pas les fonctionnalités disponibles.

---

# Conséquences sur l'architecture

À partir de cette décision :

- toutes les fonctionnalités seront modélisées comme des Capabilities ;
- les plugins deviendront uniquement des fournisseurs de capacités ;
- le noyau pilotera exclusivement les Capabilities ;
- les dépendances seront exprimées entre Capabilities ;
- les commandes seront rattachées aux Capabilities ;
- les événements seront produits par les Capabilities ;
- la supervision sera réalisée au niveau des Capabilities.

---

# ADR associés

- ADR-0001 — Lifecycle
- ADR-0005 — Plugin Architecture
- ADR-0014 — Auto Repair
- ADR-0021 — Capability Manager
- ADR-0022 — Dependency Resolution
- ADR-0023 — Plugin Discovery
- ADR-0024 — Capability Lifecycle

---

# Décision finale

Le noyau **Shikamaru** adopte une architecture orientée **Capability**.

À partir de la version **v0.4.0**, les Capabilities deviennent l'unité fonctionnelle centrale d'Ohana-Agent.

Les plugins sont désormais considérés comme des fournisseurs de capacités, tandis que le noyau orchestre exclusivement ces dernières.

Cette décision constitue le fondement des futures évolutions de la plateforme.
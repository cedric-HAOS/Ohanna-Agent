# ADR-0022 — Dependency Resolution

- **Statut** : Accepté
- **Date** : 2026-07-08
- **Décideurs** : Équipe Ohanna-Agent
- **Version cible** : v0.4.0

---

# Contexte

L'ADR-0020 introduit les **Capabilities** comme unité fonctionnelle centrale d'Ohanna-Agent.

L'ADR-0021 introduit le **CapabilityManager**, responsable de leur enregistrement et de leur orchestration.

Les Capabilities ne sont cependant pas indépendantes les unes des autres.

Certaines nécessitent qu'une ou plusieurs autres fonctionnalités soient déjà disponibles avant de pouvoir démarrer.

Exemples :

- Home Assistant nécessite MQTT.
- La supervision peut nécessiter MQTT.
- Un service DNS peut dépendre de la connectivité réseau.
- Un plugin de sauvegarde peut dépendre du système de fichiers.

Il est donc nécessaire de définir un mécanisme permettant de résoudre automatiquement ces dépendances.

---

# Problème

Sans résolution automatique des dépendances :

- l'ordre de démarrage serait codé en dur ;
- chaque plugin devrait gérer ses propres vérifications ;
- l'ajout d'une nouvelle Capability nécessiterait de modifier le noyau ;
- l'arrêt d'une Capability pourrait interrompre d'autres fonctionnalités sans contrôle.

Cette approche limiterait fortement l'évolutivité de l'architecture.

---

# Décision

Les dépendances sont exprimées exclusivement entre **Capabilities**.

Le noyau ne manipule jamais des dépendances entre plugins.

Le **CapabilityManager** est responsable de construire le graphe des dépendances et de déterminer l'ordre d'exécution.

---

# Principe

Chaque Capability déclare explicitement les fonctionnalités dont elle dépend.

Exemple :

```text
HomeAssistant

depends_on:

- mqtt
```

ou

```text
Monitoring

depends_on:

- mqtt
- dns
```

Les dépendances sont déclaratives.

Aucune logique métier ne doit être écrite dans le noyau.

---

# Graphe de dépendances

Les dépendances forment un graphe orienté.

Exemple :

```text
        Network
           │
     ┌─────┴─────┐
     │           │
    DNS        MQTT
                 │
        ┌────────┴────────┐
        │                 │
 Monitoring      Home Assistant
```

Chaque nœud représente une Capability.

Chaque arête représente une dépendance.

---

# Ordonnancement

Le CapabilityManager réalise un tri topologique du graphe.

L'ordre obtenu est utilisé pour :

- l'initialisation ;
- le démarrage ;
- l'arrêt ;
- le redémarrage ;
- la réparation automatique.

Aucun ordre n'est codé en dur.

---

# Démarrage

Une Capability ne peut être démarrée que si toutes ses dépendances sont disponibles.

Exemple :

```text
Network

↓

MQTT

↓

Home Assistant
```

Si MQTT est indisponible :

- Home Assistant reste dans un état d'attente ;
- aucune tentative de démarrage n'est effectuée.

---

# Arrêt

L'arrêt est réalisé dans l'ordre inverse.

Exemple :

```text
Home Assistant

↓

MQTT

↓

Network
```

Cette stratégie garantit qu'aucune Capability ne perd une dépendance encore utilisée.

---

# Détection des cycles

Les dépendances circulaires sont interdites.

Exemple invalide :

```text
A

↓

B

↓

C

↓

A
```

Le CapabilityManager détecte automatiquement les cycles lors de la construction du graphe.

Le démarrage est alors refusé.

---

# Dépendances optionnelles

Une Capability peut déclarer une dépendance comme optionnelle.

Exemple :

```text
Monitoring

required:

- mqtt

optional:

- home_assistant
```

L'absence d'une dépendance optionnelle ne bloque pas le démarrage.

Elle peut simplement limiter certaines fonctionnalités.

---

# Dépendances futures

Le modèle est conçu pour permettre ultérieurement :

- des dépendances distantes ;
- des dépendances réseau ;
- des dépendances distribuées ;
- des dépendances conditionnelles.

Aucune modification du modèle ne sera nécessaire.

---

# Responsabilités

Le CapabilityManager est responsable de :

- construire le graphe ;
- détecter les cycles ;
- déterminer l'ordre d'exécution ;
- vérifier les dépendances ;
- empêcher un démarrage invalide.

Les Capabilities restent responsables de leur propre logique métier.

---

# Conséquences

## Avantages

- aucun ordre codé en dur ;
- architecture déclarative ;
- ajout de nouvelles fonctionnalités sans modifier le noyau ;
- démarrage déterministe ;
- arrêt sécurisé ;
- excellente extensibilité ;
- préparation à une architecture distribuée.

---

## Inconvénients

- nécessité de maintenir un graphe de dépendances ;
- légère augmentation de la complexité du CapabilityManager.

---

# Alternatives étudiées

## Ordre de démarrage codé en dur

Rejeté.

Cette solution rendrait le noyau difficile à maintenir.

---

## Vérification des dépendances dans chaque plugin

Rejeté.

La logique d'orchestration ne doit pas être dupliquée.

---

## Dépendances entre plugins

Rejeté.

Les plugins sont des implémentations.

Les dépendances doivent porter sur les fonctionnalités réellement offertes.

---

# Conséquences sur l'architecture

Le CapabilityManager devient responsable de l'orchestration globale.

Le noyau n'a plus besoin de connaître l'ordre de démarrage des fonctionnalités.

Toutes les nouvelles Capabilities s'intègrent automatiquement au système dès lors que leurs dépendances sont correctement déclarées.

---

# ADR associés

- ADR-0020 — Capability Model
- ADR-0021 — Capability Manager
- ADR-0023 — Plugin Discovery
- ADR-0024 — Capability Lifecycle

---

# Décision finale

Les dépendances d'Ohanna-Agent sont désormais exprimées exclusivement entre **Capabilities**.

Le **CapabilityManager** construit automatiquement le graphe de dépendances, détecte les incohérences et détermine l'ordre de démarrage, d'arrêt et de réparation des fonctionnalités.

Cette décision garantit une architecture déclarative, extensible et indépendante des implémentations techniques.
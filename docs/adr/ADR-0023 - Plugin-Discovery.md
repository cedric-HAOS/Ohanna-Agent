# ADR-0023 — Plugin Discovery

- **Statut** : Accepté
- **Date** : 2026-07-08
- **Décideurs** : Équipe Ohanna-Agent
- **Version cible** : v0.4.0

---

# Contexte

L'ADR-0020 introduit les **Capabilities** comme unité fonctionnelle centrale d'Ohanna-Agent.

L'ADR-0021 confie leur gestion au **CapabilityManager**.

L'ADR-0022 définit la résolution automatique des dépendances entre Capabilities.

Il reste cependant à définir comment les nouvelles fonctionnalités sont découvertes par le noyau.

Le système doit permettre d'ajouter de nouvelles fonctionnalités sans modifier le code du noyau.

---

# Problème

Si chaque nouvelle Capability devait être enregistrée manuellement dans l'Application :

- le noyau devrait connaître tous les plugins ;
- chaque nouveau plugin nécessiterait une modification du code central ;
- le couplage augmenterait rapidement ;
- l'architecture perdrait son extensibilité.

Cette approche est incompatible avec les objectifs d'Ohanna-Agent.

---

# Décision

Les **Plugins** deviennent les fournisseurs officiels de Capabilities.

Chaque plugin déclare explicitement les Capabilities qu'il fournit.

Le **PluginManager** est responsable de découvrir les plugins.

Le **CapabilityManager** est responsable d'enregistrer les Capabilities exposées par ces plugins.

Les deux composants collaborent sans se substituer l'un à l'autre.

---

# Architecture

```text
                +----------------------+
                |     Application      |
                +----------+-----------+
                           |
                 +---------+---------+
                 |                   |
          PluginManager     CapabilityManager
                 |                   |
          Découverte           Enregistrement
                 |                   |
              Plugin ───────────────► Capability
```

Le PluginManager ne gère jamais directement les Capabilities.

Le CapabilityManager ne découvre jamais directement les plugins.

---

# Principe

Chaque plugin expose une méthode permettant de déclarer les Capabilities qu'il fournit.

Exemple conceptuel :

```python
class DNSPlugin(Plugin):

    def capabilities(self):
        return [
            DNSCapability(),
        ]
```

ou

```python
class MonitoringPlugin(Plugin):

    def capabilities(self):
        return [
            MonitoringCapability(),
            MetricsCapability(),
        ]
```

Le nombre de Capabilities fournies par un plugin est libre.

---

# Cycle de découverte

Le démarrage suit les étapes suivantes :

```text
Chargement des plugins

↓

Découverte des Capabilities

↓

Enregistrement

↓

Résolution des dépendances

↓

Initialisation

↓

Démarrage
```

Chaque étape est clairement séparée.

---

# Séparation des responsabilités

## PluginManager

Responsable de :

- découvrir les plugins ;
- charger les modules ;
- créer les instances ;
- gérer leur cycle de vie technique.

---

## CapabilityManager

Responsable de :

- enregistrer les Capabilities ;
- vérifier leur unicité ;
- construire le registre ;
- orchestrer leur fonctionnement.

---

# Unicité

Chaque Capability possède un identifiant unique.

Exemple :

```text
dns

mqtt

dhcp

home_assistant
```

Deux plugins ne peuvent pas enregistrer simultanément une Capability portant le même identifiant.

Le CapabilityManager refuse l'enregistrement et signale une erreur.

---

# Métadonnées

Une Capability peut exposer différentes informations :

- identifiant ;
- nom ;
- version ;
- description ;
- auteur ;
- dépendances ;
- commandes ;
- événements.

Ces informations permettent au noyau d'orchestrer les fonctionnalités sans connaître leur implémentation.

---

# Découverte dynamique

Le modèle permet d'ajouter un nouveau plugin simplement en le déposant dans le répertoire des plugins.

Aucune modification du noyau n'est nécessaire.

Le PluginManager le découvre automatiquement.

Le CapabilityManager enregistre automatiquement les nouvelles Capabilities.

---

# Évolutions futures

Cette architecture permet ultérieurement :

- des plugins installables à chaud ;
- un catalogue de plugins ;
- des plugins distants ;
- un gestionnaire de versions ;
- une activation ou désactivation dynamique.

Le modèle actuel reste compatible avec ces évolutions.

---

# Conséquences

## Avantages

- découplage complet entre le noyau et les plugins ;
- ajout de nouvelles fonctionnalités sans modification du noyau ;
- architecture modulaire ;
- découverte automatique ;
- excellente extensibilité ;
- responsabilités clairement séparées.

---

## Inconvénients

- communication supplémentaire entre PluginManager et CapabilityManager ;
- validation des identifiants nécessaire lors de l'enregistrement.

---

# Alternatives étudiées

## Enregistrement manuel

Rejeté.

Chaque nouvelle fonctionnalité imposerait une modification du noyau.

---

## Découverte par réflexion globale

Rejeté.

Le noyau devrait analyser l'ensemble des modules Python, ce qui augmenterait la complexité et le temps de démarrage.

---

## PluginManager responsable des Capabilities

Rejeté.

Le PluginManager gère les implémentations techniques.

Le CapabilityManager gère les fonctionnalités.

Les deux responsabilités doivent rester indépendantes.

---

# Conséquences sur l'architecture

Le noyau ne connaît plus les plugins.

Il découvre uniquement des Capabilities.

Le PluginManager devient un fournisseur de fonctionnalités.

Le CapabilityManager devient le registre fonctionnel officiel de l'agent.

Cette séparation garantit une architecture simple, modulaire et évolutive.

---

# ADR associés

- ADR-0005 — Plugin Architecture
- ADR-0020 — Capability Model
- ADR-0021 — Capability Manager
- ADR-0022 — Dependency Resolution
- ADR-0024 — Capability Lifecycle

---

# Décision finale

Les plugins deviennent les fournisseurs officiels de **Capabilities**.

Le **PluginManager** est chargé de leur découverte et de leur chargement.

Le **CapabilityManager** est chargé de l'enregistrement et de l'orchestration des fonctionnalités exposées.

Cette architecture garantit qu'une nouvelle fonctionnalité peut être intégrée à Ohanna-Agent sans aucune modification du noyau, conformément aux principes de modularité et de découplage du projet.
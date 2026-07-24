# ADR-0000 — Vision d'Architecture

**Statut :** Accepté

**Date :** 2026-07-09

---

# Contexte

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités restent disponibles malgré les mises à jour, les pannes matérielles, les erreurs de configuration ou les défaillances d'un composant.

Dans une maison moderne, de nombreux services collaborent :

- DNS
- DHCP
- MQTT
- Home Assistant
- WireGuard
- ESPHome
- AdGuard
- Sauvegardes
- Réseau
- Internet

Le bon fonctionnement individuel de chacun de ces composants ne garantit pas que la maison continue réellement à rendre les services attendus.

La véritable question n'est donc pas :

> « Le serveur DNS fonctionne-t-il ? »

mais :

> « La maison est-elle encore capable de résoudre les noms de domaine ? »

Cette différence constitue la raison d'être d'Ohana-Agent.

---

# Décision

Ohana-Agent est un **moteur d'observation et de raisonnement sur les capacités d'une infrastructure**.

Il ne supervise pas des équipements.

Il ne supervise pas des logiciels.

Il détermine quelles **capacités** sont réellement disponibles à un instant donné.

Toutes les décisions d'architecture du projet devront respecter cette vision.

---

# Les responsabilités d'Ohana-Agent

Le moteur possède quatre responsabilités fondamentales.

## 1. Observer

Des plugins réalisent des observations sur l'infrastructure.

Les observations sont factuelles.

Exemples :

- une résolution DNS réussit ;
- un bail DHCP est obtenu ;
- une connexion MQTT est établie ;
- un tunnel WireGuard est actif.

Les plugins ne prennent aucune décision.

Ils produisent uniquement des observations.

---

## 2. Centraliser

Toutes les observations sont regroupées dans un modèle commun.

Une observation possède notamment :

- un identifiant ;
- une date ;
- un résultat ;
- une durée ;
- des métadonnées ;
- un contexte.

Cette uniformisation permet au moteur de raisonner indépendamment des protocoles observés.

---

## 3. Déduire

Le moteur analyse les observations.

Il calcule les capacités réellement disponibles.

Une capacité n'est jamais directement observée.

Elle est toujours déduite.

Par exemple, la capacité **Accès Internet** peut dépendre simultanément :

- du DNS ;
- de la passerelle ;
- du routage ;
- d'HTTPS ;
- de la connectivité IPv6.

Une seule observation ne suffit donc pas à déterminer cette capacité.

---

## 4. Publier

Une fois calculées, les capacités deviennent disponibles pour des consommateurs externes.

Ces consommateurs peuvent être :

- Home Assistant ;
- Ohana-Vision ;
- MQTT ;
- une API REST ;
- un export JSON.

Ohana-Agent reste totalement indépendant de ces consommateurs.

---

# Ce qu'Ohana-Agent n'est pas

Ohana-Agent n'est pas :

- une interface Web ;
- un tableau de bord ;
- un outil de visualisation ;
- une application Home Assistant ;
- un serveur MQTT ;
- un orchestrateur d'infrastructure ;
- un système de documentation.

Ces responsabilités appartiennent à d'autres composants de l'écosystème.

---

# Les plugins

Les plugins sont les seuls composants qui connaissent les protocoles.

Le moteur ne connaît pas :

- DNS ;
- DHCP ;
- MQTT ;
- HTTP ;
- ICMP ;
- WireGuard ;
- Home Assistant ;
- AdGuard.

Il ne connaît que des observations.

Ajouter un nouveau protocole ne nécessite donc aucune modification du moteur.

Il suffit d'ajouter un plugin produisant des observations conformes au modèle commun.

---

# Les capacités

Une capacité représente un service réellement rendu par l'infrastructure.

Elle n'est jamais directement mesurée.

Elle est calculée.

Une capacité peut dépendre :

- de plusieurs observations ;
- de plusieurs plugins ;
- de plusieurs équipements ;
- d'autres capacités.

Le moteur raisonne donc sur des relations plutôt que sur des états individuels.

---

# Les consommateurs

Ohana-Agent ne décide jamais de la manière dont ses résultats seront utilisés.

Il expose uniquement des données.

Ces données peuvent être consommées par différents systèmes.

## Ohana-Vision

Visualisation de l'état global de l'infrastructure.

## Home Assistant

Affichage des capacités dans les tableaux de bord et les automatisations.

## MQTT

Publication des capacités vers d'autres applications.

## API REST

Intégration avec des outils tiers.

Tous ces consommateurs sont optionnels.

Le moteur doit pouvoir fonctionner sans aucun d'entre eux.

---

# L'écosystème Ohana

Chaque projet possède une responsabilité unique.

```text
                +----------------------+
                |    Ohana-House      |
                | Architecture cible   |
                +----------+-----------+
                           |
            Infrastructure déclarative
                           |
                           v
                +----------------------+
                |    Ohana-Agent      |
                | Observer • Déduire   |
                | Calculer             |
                +----------+-----------+
                           |
         Capacités calculées et observations
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
+---------------+  +---------------+  +---------------+
| Ohana-Vision |  | Home Assistant|  | MQTT / REST   |
| Visualiser    |  | Consommer     |  | Intégrer      |
+---------------+  +---------------+  +---------------+
```

Les responsabilités sont clairement séparées.

### Ohana-House

Décrit l'architecture de référence.

### Ohana-Agent

Observe l'infrastructure.

Calcule les capacités.

Expose les résultats.

### Ohana-Vision

Présente les capacités à l'utilisateur.

### Les connecteurs

Permettent l'intégration avec des systèmes externes.

---

# Principes d'architecture

Toutes les évolutions d'Ohana-Agent doivent respecter les principes suivants.

## Responsabilité unique

Chaque composant possède une responsabilité clairement identifiée.

## Découplage

Le moteur ne dépend d'aucun protocole spécifique.

## Extensibilité

Les nouveaux protocoles sont ajoutés sous forme de plugins.

## Raisonnement

Les capacités sont calculées.

Elles ne sont jamais directement observées.

## Indépendance

Le moteur fonctionne indépendamment des consommateurs.

## Évolutivité

Toute nouvelle fonctionnalité doit renforcer le raisonnement sur les capacités, sans remettre en cause les principes précédents.

---

# Conséquences

Cette décision conduit à une architecture modulaire.

Le cœur du moteur reste stable tandis que les protocoles, les connecteurs et les interfaces utilisateur peuvent évoluer indépendamment.

Cette séparation permet notamment :

- l'ajout de nouveaux plugins sans modifier le moteur ;
- la création de nouvelles capacités par agrégation d'observations ;
- plusieurs interfaces clientes (Ohana-Vision, Home Assistant, API, MQTT) ;
- une évolution indépendante des différents composants de l'écosystème.

Cette ADR constitue le document fondateur du projet.

Toutes les futures décisions d'architecture devront être cohérentes avec cette vision.
# Architecture logicielle

## Introduction

Ohana-Agent est construit autour d'une séparation stricte des responsabilités.

Le logiciel ne doit jamais dépendre directement d'une technologie particulière.

Il doit manipuler des concepts stables :

* capacités ;
* observations ;
* états ;
* décisions ;
* commandes ;
* événements ;
* plugins.

L'architecture logicielle garantit que les implémentations peuvent évoluer sans remettre en cause le modèle général.

---

# Vue d'ensemble

Ohana-Agent est organisé autour de trois grands ensembles :

```text
Ohana-Agent
│
├── Shikamaru
│   Moteur de décision
│
├── Plugins
│   Fournisseurs de capacités
│
└── Interfaces
    Points d'entrée et de sortie
```

---

# Shikamaru

Shikamaru est le moteur de décision d'Ohana-Agent.

Il est responsable de :

* recevoir les observations ;
* évaluer les capacités ;
* déterminer les états ;
* prendre les décisions ;
* envoyer les commandes ;
* orchestrer les réparations ;
* publier les événements.

Shikamaru ne connaît aucune technologie externe.

Il ne connaît ni DNS, ni DHCP, ni MQTT, ni Home Assistant.

Il manipule uniquement les concepts fondamentaux du système.

---

# Plugins

Les plugins sont les fournisseurs de capacités.

Ils sont responsables de :

* observer des systèmes externes ;
* produire des observations ;
* recevoir des commandes ;
* exécuter des actions ;
* publier des événements techniques.

Un plugin ne décide jamais.

Il ne calcule pas l'état global d'une capacité.

Il ne coordonne pas d'autres plugins.

Il reste spécialiste d'une technologie ou d'un domaine.

---

# Interfaces

Les interfaces permettent à Ohana-Agent d'échanger avec l'extérieur.

Exemples :

* interface MQTT ;
* interface API ;
* interface CLI ;
* interface Web ;
* interface de configuration ;
* interface de journalisation.

Une interface ne contient pas de logique métier.

Elle expose ou transporte des informations produites par Shikamaru et les plugins.

---

# Flux principal

Le fonctionnement nominal suit le cycle suivant :

```text
Plugin
  │
  ▼
Observation
  │
  ▼
Shikamaru
  │
  ▼
Évaluation
  │
  ▼
État
  │
  ▼
Décision
  │
  ▼
Commande
  │
  ▼
Plugin
  │
  ▼
Action
  │
  ▼
Nouvelle observation
```

La réussite d'une action n'est jamais supposée.

Elle est toujours confirmée par une nouvelle observation.

---

# Séparation des responsabilités

## Shikamaru décide

Shikamaru porte la logique centrale du système.

Il décide :

* si une capacité est disponible ;
* si une capacité est dégradée ;
* si une réparation doit être tentée ;
* si une intervention humaine est nécessaire.

---

## Les plugins observent et agissent

Les plugins ne font que deux choses :

* produire des observations ;
* exécuter des commandes.

Ils ne portent aucune stratégie globale.

---

## Les interfaces exposent

Les interfaces permettent de consulter, piloter ou intégrer Ohana-Agent.

Elles ne décident pas.

Elles ne réparent pas.

Elles ne modifient pas directement l'état des capacités.

---

# État interne

L'état interne d'Ohana-Agent est construit à partir des observations.

Il ne doit jamais être déduit uniquement d'une configuration.

L'état peut concerner :

* une capacité ;
* un plugin ;
* une commande ;
* une réparation ;
* une interface ;
* l'agent lui-même.

---

# Événements

Les événements permettent de signaler les changements importants.

Exemples :

* une capacité devient disponible ;
* une capacité devient dégradée ;
* une commande est envoyée ;
* une réparation commence ;
* une réparation échoue ;
* un plugin devient indisponible.

Les événements permettent de découpler les composants.

---

# Commandes

Une commande est une demande adressée à un plugin ou à une interface.

Une commande ne garantit jamais son résultat.

Elle déclenche une action.

Le résultat est vérifié ensuite par observation.

---

# Configuration

La configuration décrit les intentions de déploiement.

Elle peut définir :

* les capacités attendues ;
* les plugins activés ;
* les seuils d'évaluation ;
* les règles de réparation ;
* les paramètres d'accès aux systèmes externes.

La configuration ne constitue jamais une preuve de fonctionnement.

---

# Journalisation

Ohana-Agent doit être observable.

Chaque décision importante doit pouvoir être expliquée.

Les journaux doivent permettre de comprendre :

* ce qui a été observé ;
* comment l'état a été évalué ;
* quelle décision a été prise ;
* quelle commande a été envoyée ;
* quel résultat a été observé ensuite.

---

# Testabilité

Chaque composant doit pouvoir être testé indépendamment.

En particulier :

* Shikamaru doit pouvoir être testé sans plugins réels ;
* un plugin doit pouvoir être testé sans infrastructure réelle ;
* les règles d'évaluation doivent pouvoir être testées avec des observations simulées ;
* les commandes doivent pouvoir être vérifiées sans action destructive.

La testabilité est une propriété fondamentale de l'architecture.

---

# Résumé

Ohana-Agent repose sur une séparation simple :

```text
Shikamaru décide.

Les plugins observent et agissent.

Les interfaces exposent.

Les capacités constituent le contrat.
```

Cette organisation permet de construire un logiciel fiable, extensible et durable.

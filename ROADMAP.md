# ROADMAP — Ohanna-Agent

## Vision

Ohanna-Agent n'est pas un superviseur d'équipements.

Il est le garant des **capacités** définies par l'architecture de référence d'Ohanna-House.

Les logiciels évoluent.

Les matériels changent.

Les services sont remplacés.

Les capacités, elles, doivent rester disponibles.

Ohanna-Agent observe, évalue et garantit ces capacités indépendamment des technologies qui les implémentent.

> **Les logiciels changent. Les capacités demeurent.**

---

# État actuel

Le noyau logiciel est désormais mature.

Il fournit :

* une architecture modulaire ;
* un Runtime supervisé ;
* un Scheduler événementiel ;
* un système mémoire ;
* un Dispatcher ;
* un EventBus ;
* une forte couverture de tests.

Cette base constitue le socle des prochaines évolutions.

---

# Phase I — Foundation ✅

## Objectif

Construire un noyau robuste, modulaire et fortement testé.

## Réalisations

* Application
* Dispatcher
* Runtime
* Services
* Memory
* Scheduler
* EventBus
* Monitoring
* MQTT Runtime
* Architecture événementielle

**État : Terminé**

---

# Phase II — Modèle de capacités

## Objectif

Faire évoluer Ohanna-Agent d'un ordonnanceur de tâches vers un garant de capacités.

Une capacité représente un service attendu par l'infrastructure.

Exemples :

* DNS
* DHCP
* MQTT
* Home Assistant
* Sauvegardes
* Téléinformation
* Accès distant
* Supervision
* Notifications

Chaque capacité possédera notamment :

* un identifiant ;
* une description ;
* un état courant ;
* un niveau de criticité ;
* une fréquence de vérification ;
* un ou plusieurs contrôles de santé.

Le Scheduler exécutera des vérifications de capacités plutôt que de simples tâches techniques.

---

# Phase III — Fournisseurs de capacités

## Objectif

Séparer les capacités de leurs implémentations techniques.

Une même capacité pourra être assurée par un ou plusieurs fournisseurs.

Exemple :

**Capacité : DNS**

Fournisseurs possibles :

* AdGuard Home
* Pi-hole
* Unbound

Le remplacement d'un logiciel ne devra jamais remettre en cause la capacité garantie.

Cette abstraction permettra :

* la redondance ;
* la haute disponibilité ;
* les migrations ;
* les évolutions de l'infrastructure.

---

# Phase IV — Tableau de bord Web

## Objectif

Créer une interface Web native permettant de superviser Ohanna-Agent sans dépendre d'un logiciel tiers.

Cette interface devra rester disponible même si Home Assistant est indisponible.

Le tableau de bord présentera notamment :

* les capacités disponibles ;
* leur état de santé ;
* leur niveau de disponibilité ;
* les fournisseurs utilisés ;
* les événements récents ;
* les tâches planifiées ;
* les alertes ;
* les statistiques d'exécution.

À terme, cette interface constituera la console d'administration d'Ohanna-Agent.

---

# Phase V — Intégration Home Assistant

## Objectif

Intégrer naturellement Ohanna-Agent dans Home Assistant.

Les capacités seront publiées sous forme d'entités Home Assistant.

Exemples :

* capteurs d'état ;
* disponibilités ;
* diagnostics ;
* alertes ;
* statistiques ;
* événements.

Home Assistant deviendra une interface de consultation et d'automatisation supplémentaire, sans être indispensable au fonctionnement d'Ohanna-Agent.

---

# Phase VI — Politiques de disponibilité

## Objectif

Définir ce que signifie une capacité "fonctionnelle".

Chaque capacité pourra disposer de politiques telles que :

* disponibilité minimale ;
* fréquence maximale des erreurs ;
* temps de réponse attendu ;
* seuils d'alerte ;
* périodes de maintenance.

Les politiques permettront d'évaluer objectivement l'état des capacités.

---

# Phase VII — Diagnostic

## Objectif

Comprendre pourquoi une capacité est dégradée.

Le moteur de diagnostic analysera :

* les événements ;
* l'historique ;
* les dépendances ;
* les fournisseurs ;
* les symptômes observés.

L'objectif est d'identifier automatiquement la cause la plus probable d'une dégradation.

---

# Phase VIII — Remédiation

## Objectif

Proposer ou exécuter des actions correctives.

Exemples :

* redémarrage d'un service ;
* bascule vers un fournisseur secondaire ;
* relance d'une tâche ;
* notification de l'administrateur ;
* exécution d'un scénario de secours.

Chaque remédiation sera traçable et vérifiable.

---

# Phase IX — Autonomie

## Objectif

Permettre à Ohanna-Agent de maintenir les capacités sans intervention humaine.

Le cycle deviendra :

Observation

↓

Diagnostic

↓

Décision

↓

Action

↓

Validation

↓

Retour à un état nominal

L'objectif est d'augmenter progressivement le niveau d'autonomie tout en conservant le contrôle de l'administrateur.

---

# Phase X — Intelligence assistée

## Objectif

Utiliser l'intelligence artificielle comme outil d'analyse et d'aide à la décision.

L'IA pourra notamment :

* expliquer les incidents ;
* corréler plusieurs événements ;
* détecter des tendances ;
* anticiper des dégradations ;
* proposer des améliorations de l'architecture ;
* assister l'administrateur dans ses décisions.

L'intelligence artificielle n'a pas vocation à remplacer le moteur de supervision.

Elle vient enrichir les capacités d'analyse d'Ohanna-Agent.

---

# Principes directeurs

Toutes les évolutions futures respecteront les principes suivants :

* priorité aux capacités plutôt qu'aux logiciels ;
* architecture modulaire ;
* faible couplage ;
* composants testables ;
* développement guidé par les tests (TDD) ;
* documentation systématiquement mise à jour ;
* compatibilité ascendante autant que possible.

---

# Vision à long terme

À terme, Ohanna-Agent devra être capable de garantir qu'une capacité définie par l'architecture de référence reste disponible, quel que soit le logiciel, le matériel ou le fournisseur utilisé pour la mettre en œuvre.

Le logiciel ne sera plus au centre de la supervision.

La capacité rendue à l'utilisateur deviendra l'unité fondamentale du système.

**Les logiciels changent. Les capacités demeurent.**

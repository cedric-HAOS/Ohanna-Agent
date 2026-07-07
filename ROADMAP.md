# Roadmap

## Introduction

Cette feuille de route décrit l'évolution prévue d'Ohanna-Agent.

Elle ne constitue pas un engagement de livraison.

Elle exprime la vision de l'évolution du logiciel, dans le respect des principes définis par son architecture.

Chaque sprint poursuit un objectif de maturité clairement identifié.

---

# Sprint 0 — Fondation

## Objectif

Définir l'architecture de référence du logiciel.

## Livrables

* Vision
* Concepts
* Philosophie
* Capacités
* Plugins
* Architecture logicielle
* États
* Commandes
* Message Model
* MQTT
* MQTT Convention
* Configuration
* Roadmap

## Résultat attendu

Une architecture stable, indépendante des technologies et prête à être implémentée.

---

# Sprint 1 — Le noyau

## Objectif

Construire Shikamaru.

## Livrables

* structure du projet ;
* moteur de décision ;
* gestion des plugins ;
* découverte automatique ;
* bus d'événements interne ;
* journalisation ;
* configuration ;
* premiers tests unitaires.

## Résultat attendu

Un moteur capable de charger des plugins, recevoir des observations et prendre des décisions.

---

# Sprint 2 — Les premières capacités

## Objectif

Garantir les capacités essentielles de l'infrastructure.

## Capacités ciblées

* résolution DNS ;
* attribution DHCP ;
* synchronisation temporelle ;
* connectivité réseau.

## Résultat attendu

Premiers plugins opérationnels.

Premières capacités garanties.

---

# Sprint 3 — Intégration domotique

## Objectif

Intégrer Ohanna-Agent à l'écosystème domotique.

## Livrables

* interface MQTT ;
* API Home Assistant ;
* publication des états ;
* réception des commandes.

## Résultat attendu

Ohanna-Agent devient observable et pilotable depuis Home Assistant.

---

# Sprint 4 — Exploitabilité

## Objectif

Améliorer l'exploitation quotidienne.

## Livrables

* interface Web ;
* tableau de bord ;
* historique des capacités ;
* indicateur Health ;
* visualisation des événements.

## Résultat attendu

Une vision claire de l'état du système.

---

# Sprint 5 — Auto-réparation

## Objectif

Permettre au système de restaurer lui-même les capacités dégradées.

## Livrables

* stratégies de réparation ;
* politiques de reprise ;
* limitation des tentatives ;
* validation automatique des réparations.

## Résultat attendu

Shikamaru devient capable de restaurer certaines capacités sans intervention humaine.

---

# Sprint 6 — Déploiement distribué

## Objectif

Étendre Ohanna-Agent à plusieurs machines.

## Livrables

* découverte des agents ;
* coopération entre instances ;
* partage des observations ;
* synchronisation des états.

## Résultat attendu

Plusieurs instances d'Ohanna-Agent collaborent pour garantir les capacités de l'infrastructure.

---

# Sprint 7 — Intelligence opérationnelle

## Objectif

Améliorer la prise de décision grâce à l'analyse de l'historique.

## Livrables

* corrélation d'événements ;
* détection d'anomalies ;
* anticipation des défaillances ;
* recommandations d'exploitation.

## Résultat attendu

Shikamaru ne réagit plus uniquement aux incidents.

Il commence à les anticiper.

---

# Sprint 8 — Écosystème

## Objectif

Faire d'Ohanna-Agent une plateforme extensible.

## Livrables

* SDK de développement de plugins ;
* documentation développeur ;
* catalogue de plugins ;
* outils de validation.

## Résultat attendu

Des plugins peuvent être développés indépendamment du noyau.

---

# Vision à long terme

À terme, Ohanna-Agent devra être capable de :

* découvrir automatiquement son environnement ;
* identifier les capacités attendues ;
* sélectionner les fournisseurs adaptés ;
* observer l'infrastructure ;
* prendre des décisions ;
* réparer les défaillances ;
* expliquer chacune de ses décisions.

L'objectif n'est pas seulement d'automatiser une infrastructure.

L'objectif est de garantir durablement les capacités qu'elle doit fournir.

---

# Principes

La feuille de route respecte les principes suivants :

* l'architecture précède l'implémentation ;
* les capacités précèdent les technologies ;
* les décisions précèdent les optimisations ;
* la simplicité reste prioritaire ;
* chaque sprint produit une base stable pour le suivant.

---

# Résumé

Ohanna-Agent évolue progressivement :

de l'architecture,

au moteur,

des capacités,

à l'autonomie.

# CORE.md — Architecture du noyau Ohanna-Agent

Version : 3
Statut : validé
Projet : Ohanna-Agent
Noyau : Shikamaru
État actuel : Phase 3 — MQTT Runtime terminée
Validation : 156 tests automatisés
ADR de référence : ADR-0014 validé

---

## 1. Rôle du noyau

Le noyau d’Ohanna-Agent, nommé **Shikamaru**, constitue le cœur d’exécution de l’agent.

Il ne représente pas une intelligence autonome complète, mais une base logicielle fiable, testable et extensible chargée de :

* représenter l’état interne de l’agent ;
* recevoir des commandes ;
* produire des événements ;
* dispatcher ces événements ;
* maintenir un cycle de vie clair ;
* exposer une interface runtime MQTT ;
* permettre l’ajout progressif de capacités sans casser l’architecture existante.

Le noyau doit rester simple, déterministe et observable.

Son objectif principal est de garantir que toute évolution future d’Ohanna-Agent repose sur une base stable.

---

## 2. Principes d’architecture

Le noyau repose sur les principes suivants :

1. **Séparation stricte des responsabilités**
   Chaque composant possède un rôle clair : état, commande, événement, dispatcher, application, runtime MQTT.

2. **Architecture pilotée par événements**
   Le cœur ne déclenche pas directement des actions complexes. Il émet des événements qui peuvent être observés, testés et routés.

3. **Cycle de vie explicite**
   Les transitions de l’agent sont représentées par des états connus et contrôlés.

4. **Commandes typées**
   Les actions reçues par l’agent sont représentées par des objets de commande structurés.

5. **Configuration centralisée**
   Le comportement du noyau dépend d’une configuration explicite, validée et testée.

6. **Runtime interchangeable**
   MQTT est actuellement le runtime principal, mais il ne doit pas polluer le cœur métier.

7. **Testabilité prioritaire**
   Toute évolution significative doit être couverte par des tests automatisés.

---

## 3. Vue d’ensemble

L’architecture actuelle peut être résumée ainsi :

```text
┌──────────────────────────┐
│        Runtime MQTT       │
│  Connexion / messages     │
│  Commandes entrantes      │
│  Événements sortants      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│       Application         │
│  Orchestration globale    │
│  Cycle de vie             │
│  Commandes                │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│       Dispatcher          │
│  Routage des événements   │
│  Observateurs             │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│         Events            │
│  Domain events            │
│  System events            │
│  MQTT events              │
└──────────────────────────┘
```

Le runtime MQTT est placé à la frontière du système.

L’application reste le point d’orchestration central.

Le dispatcher permet de découpler la production d’événements de leur consommation.

---

## 4. Composants principaux

### 4.1 Application

L’application est le composant d’orchestration du noyau.

Elle est responsable de :

* l’initialisation du noyau ;
* le démarrage de l’agent ;
* l’arrêt propre de l’agent ;
* la réception et le traitement des commandes ;
* l’émission des événements associés ;
* la gestion du cycle de vie.

L’application ne doit pas contenir de logique spécifique à MQTT.

Elle doit rester indépendante du transport.

---

### 4.2 Lifecycle

Le cycle de vie décrit les états fondamentaux de l’agent.

Il permet d’éviter les comportements implicites ou ambigus.

Les états attendus sont notamment :

* initialisé ;
* démarré ;
* arrêté ;
* en erreur si nécessaire.

Le cycle de vie permet de garantir que certaines commandes ne sont acceptées que dans des états cohérents.

Par exemple, un arrêt ne doit pas produire le même effet si l’agent n’est pas démarré.

---

### 4.3 Command

Les commandes représentent les intentions reçues par l’agent.

Elles doivent être :

* explicites ;
* typées ;
* sérialisables ;
* testables ;
* indépendantes du transport.

Une commande peut provenir de MQTT aujourd’hui, mais demain d’une CLI, d’une API HTTP ou d’un autre runtime.

Exemples de commandes :

* démarrer l’agent ;
* arrêter l’agent ;
* demander son état ;
* publier un signal de santé ;
* exécuter une action future.

Le noyau ne doit jamais dépendre directement du format brut d’un message MQTT.

Le runtime transforme les messages externes en commandes internes.

---

### 4.4 Events

Les événements décrivent ce qui s’est produit dans le système.

Ils ne sont pas des ordres, mais des faits.

Exemples :

* application démarrée ;
* application arrêtée ;
* commande reçue ;
* commande rejetée ;
* état modifié ;
* événement MQTT publié ;
* erreur détectée.

Les événements permettent :

* l’observabilité ;
* les tests ;
* le découplage ;
* la journalisation ;
* l’intégration future avec d’autres systèmes.

---

### 4.5 Dispatcher

Le dispatcher est responsable du routage des événements.

Il reçoit les événements produits par l’application ou par d’autres composants et les transmet aux handlers enregistrés.

Il permet de découpler :

* le producteur d’un événement ;
* les consommateurs de cet événement.

Le dispatcher ne doit pas connaître la logique métier des handlers.

Il applique uniquement une mécanique de diffusion contrôlée.

---

### 4.6 Configuration

La configuration définit les paramètres nécessaires à l’exécution de l’agent.

Elle peut inclure :

* l’identité de l’agent ;
* les paramètres MQTT ;
* les topics ;
* les options runtime ;
* les paramètres de logs ;
* les options de sécurité futures.

La configuration doit être validée avant utilisation.

Une configuration invalide doit provoquer une erreur explicite et testable.

---

### 4.7 MQTT Runtime

Le runtime MQTT est la couche d’intégration actuelle avec l’extérieur.

Il est responsable de :

* établir la connexion MQTT ;
* s’abonner aux topics de commande ;
* recevoir les messages entrants ;
* convertir les messages MQTT en commandes internes ;
* publier les événements sortants ;
* gérer les erreurs de transport ;
* respecter les conventions validées par ADR-0014.

Le runtime MQTT ne doit pas devenir le noyau.

Il reste une frontière technique.

Le cœur applicatif doit pouvoir exister sans MQTT.

---

## 5. Architecture événementielle

Ohanna-Agent suit une architecture orientée événements.

Une commande reçue produit généralement un ou plusieurs événements.

Exemple :

```text
Message MQTT entrant
        │
        ▼
Parsing runtime MQTT
        │
        ▼
Command interne
        │
        ▼
Application
        │
        ▼
Events
        │
        ▼
Dispatcher
        │
        ▼
Handlers / publication MQTT / logs
```

Cette approche permet de conserver une trace claire de ce qui s’est passé.

Elle facilite aussi les tests : il est possible de vérifier qu’une commande donnée produit bien les événements attendus.

---

## 6. Frontière entre cœur et runtime

La frontière entre le cœur et MQTT est essentielle.

Le cœur connaît :

* les commandes ;
* les événements ;
* l’état ;
* le dispatcher ;
* le cycle de vie.

Le cœur ne doit pas connaître :

* les détails de connexion MQTT ;
* les topics bruts ;
* les payloads réseau ;
* les bibliothèques MQTT ;
* les erreurs spécifiques au broker.

Le runtime MQTT connaît :

* le broker ;
* les topics ;
* le format réseau ;
* les conversions vers les commandes internes ;
* la publication des événements sortants.

Cette séparation protège l’architecture contre un couplage excessif.

---

## 7. ADR-0014 — Convention MQTT Runtime

ADR-0014 valide la structure actuelle du runtime MQTT.

Les décisions structurantes sont :

* MQTT est le runtime officiel de la Phase 3 ;
* les commandes MQTT doivent être converties en commandes internes ;
* les événements sortants doivent être publiés selon une convention stable ;
* le cœur applicatif ne doit pas dépendre directement du client MQTT ;
* les tests doivent couvrir le comportement attendu du runtime.

ADR-0014 marque la fin de la Phase 3 MQTT Runtime.

---

## 8. État actuel du projet

L’état actuel d’Ohanna-Agent est le suivant :

```text
Tests automatisés : 156
Phase 3 MQTT Runtime : terminée
ADR-0014 : validé
Architecture événementielle : en place
Dispatcher : opérationnel
Commandes : opérationnelles
Cycle de vie : opérationnel
Configuration : opérationnelle
Runtime MQTT : opérationnel
```

Ce niveau de validation permet de considérer le noyau comme suffisamment stable pour préparer les phases suivantes.

---

## 9. Responsabilités interdites au noyau

Le noyau ne doit pas prendre en charge directement :

* la logique métier domotique ;
* les scénarios Home Assistant ;
* la gestion directe de périphériques physiques ;
* les décisions IA complexes ;
* la persistance avancée ;
* les appels réseau non abstraits ;
* les automatisations longues ;
* la configuration de l’infrastructure domestique.

Ces responsabilités pourront être ajoutées plus tard sous forme de capacités, plugins, adapters ou services dédiés.

---

## 10. Extension future

Le noyau doit permettre l’ajout futur de :

* plugins ;
* capacités ;
* mémoire ;
* scheduler ;
* supervision ;
* règles de décision ;
* intégrations Home Assistant ;
* intégrations MQTT avancées ;
* API HTTP éventuelle ;
* CLI ;
* persistence store ;
* observabilité enrichie.

Ces évolutions ne doivent pas modifier les fondations existantes sans ADR.

Toute évolution structurante doit passer par :

1. une proposition claire ;
2. une ADR ;
3. une implémentation minimale ;
4. des tests ;
5. une mise à jour documentaire.

---

## 11. Règles de stabilité

À partir de cette version v3, les règles suivantes s’appliquent :

* toute modification du cycle de vie doit être testée ;
* toute nouvelle commande doit avoir un comportement explicite ;
* tout nouvel événement doit être documenté ;
* toute modification MQTT doit respecter ADR-0014 ou proposer une nouvelle ADR ;
* le cœur ne doit pas importer directement de dépendance runtime ;
* les tests existants doivent rester verts ;
* la documentation doit évoluer avec le code.

---

## 12. Contrats internes

Les contrats internes du noyau sont :

### Commande

Une commande représente une intention.

Elle doit pouvoir être créée indépendamment de MQTT.

### Événement

Un événement représente un fait passé.

Il doit pouvoir être dispatché, observé et testé.

### Dispatcher

Le dispatcher transmet les événements sans connaître leur logique métier.

### Application

L’application orchestre le cycle de vie et les commandes.

### Runtime

Le runtime traduit le monde extérieur vers le cœur, puis republie les événements utiles.

---

## 13. Stratégie de tests

La stratégie actuelle repose sur 156 tests automatisés.

Les tests couvrent notamment :

* l’application ;
* les commandes ;
* la configuration ;
* le dispatcher ;
* les événements ;
* le cycle de vie ;
* le runtime MQTT ;
* les comportements d’erreur ;
* les transitions principales.

La règle de base est simple :

> Une fonctionnalité non testée n’est pas considérée comme stabilisée.

Avant chaque évolution majeure, les tests doivent être exécutés avec :

```bash
ruff check .
pytest
```

L’état attendu est :

```text
All checks passed
156 passed
```

---

## 14. Positionnement de Shikamaru

Shikamaru n’est pas encore l’agent complet.

Shikamaru est le noyau rationnel d’Ohanna-Agent.

Son rôle est de préparer une base propre pour les futures couches :

* perception ;
* mémoire ;
* décision ;
* action ;
* supervision ;
* intégration maison ;
* autonomie progressive.

Le nom Shikamaru est cohérent avec cette philosophie :

* calme ;
* structuré ;
* stratégique ;
* prévisible ;
* efficace.

---

## 15. Conclusion

La version v3 du noyau Ohanna-Agent acte la stabilisation de l’architecture actuelle.

Avec 156 tests automatisés, une Phase 3 MQTT Runtime terminée et ADR-0014 validé, le projet dispose désormais d’un socle solide.

Le cœur applicatif est séparé du runtime MQTT.

Les commandes, événements, dispatcher, configuration et cycle de vie forment une base cohérente.

La suite du projet peut désormais se concentrer sur l’extension des capacités d’Ohanna-Agent sans remettre en cause le noyau.

Le noyau Shikamaru est prêt pour la suite.

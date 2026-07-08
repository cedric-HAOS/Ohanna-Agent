# CORE.md

## Architecture du noyau Shikamaru

---

# 1. Vision

## Pourquoi Ohanna-Agent existe

Les outils de supervision traditionnels répondent à une question simple :

> *« Est-ce que le service fonctionne ? »*

Ohanna-Agent répond à une question différente :

> **« La capacité que l'infrastructure est censée fournir est-elle réellement garantie ? »**

Cette différence est fondamentale.

Un serveur DNS peut être démarré mais incapable de résoudre des noms.

Un broker MQTT peut accepter des connexions tout en étant incapable de distribuer des messages.

Une sauvegarde peut s'exécuter quotidiennement tout en produisant des archives inutilisables.

Dans chacun de ces cas, le logiciel fonctionne.

La capacité, elle, est perdue.

Ohanna-Agent ne surveille donc pas des applications.

Il garantit des **capacités**.

---

## Les capacités

Une capacité représente un service rendu par l'infrastructure.

Quelques exemples :

* DNS
* DHCP
* MQTT
* Home Assistant
* Docker
* Reverse Proxy
* VPN
* Sauvegardes
* Accès Internet

Chaque capacité possède :

* un état ;
* des dépendances ;
* des diagnostics ;
* des actions correctives ;
* un cycle de vie.

Le rôle d'Ohanna-Agent est de maintenir ces capacités disponibles dans le temps.

---

## Une architecture orientée capacités

Le projet ne décrit jamais une infrastructure par la liste des logiciels installés.

Il la décrit par les services qu'elle rend.

Ainsi, plusieurs implémentations peuvent fournir une même capacité.

Par exemple, la capacité **DNS** peut être assurée par :

* AdGuard Home ;
* Pi-hole ;
* BIND ;
* Unbound ;
* tout autre serveur DNS compatible.

Le noyau ne dépend donc jamais d'une technologie particulière.

---

# 2. Principes de conception

Depuis sa création, Ohanna-Agent repose sur quelques principes architecturaux simples.

Ils guident toutes les décisions de conception.

---

## Noyau minimal

Le noyau (*Shikamaru*) doit rester volontairement réduit.

Il fournit uniquement les services communs :

* EventBus ;
* Scheduler ;
* Dispatcher ;
* Runtime ;
* Memory ;
* Configuration ;
* Capability Manager ;
* Plugin SDK.

Aucune logique métier spécifique ne doit être implémentée dans le noyau.

---

## Responsabilité unique

Chaque composant possède une responsabilité clairement définie.

Par exemple :

* `PluginDiscovery` découvre les plugins ;
* `PluginLoader` les charge ;
* `PluginRegistry` les stocke ;
* `PluginRuntime` conserve leur état ;
* `PluginManager` orchestre l'ensemble.

Cette séparation facilite la maintenance et les tests.

---

## Découplage

Les composants communiquent exclusivement par leurs contrats publics.

Le noyau ne dépend jamais d'une implémentation concrète.

Les plugins ne connaissent jamais directement la classe `Application`.

Ils utilisent uniquement un `PluginContext`.

---

## Architecture orientée événements

Les interactions importantes sont publiées sous forme d'événements.

Par exemple :

* démarrage du Scheduler ;
* enregistrement d'un plugin ;
* changement d'état d'une capacité.

Cette approche réduit fortement les dépendances entre composants.

---

## API publique stable

Le SDK constitue désormais l'API publique officielle d'Ohanna-Agent.

Les plugins compilent contre des interfaces stables (`Protocol`) plutôt que contre les implémentations internes du noyau.

Cette décision garantit la compatibilité des extensions malgré l'évolution du Core.

---

# 3. Architecture générale

L'architecture est organisée autour d'un noyau stable auquel viennent se rattacher des extensions indépendantes.

```text
                         Plugins
                             │
                             ▼
                    Plugin Manager
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Plugin Discovery     Plugin Loader      Plugin Registry
        │                    │                    │
        ▼                    ▼                    ▼
 DiscoveryProvider    Plugin Factory      Plugin Runtime
                             │
                             ▼
                        Plugin Context
                             │
                             ▼
                      Noyau Shikamaru
```

Le noyau ne connaît jamais les plugins.

Les plugins ne connaissent jamais l'architecture interne du noyau.

Le `PluginContext` constitue l'unique point de contact entre ces deux mondes.

---

## Objectifs de cette architecture

Cette organisation poursuit plusieurs objectifs :

* garantir la stabilité du noyau ;
* permettre l'ajout de nouvelles capacités sans modifier le Core ;
* simplifier les tests unitaires ;
* faciliter l'évolution de l'architecture ;
* préparer l'intégration du Dashboard Web et de Home Assistant ;
* permettre, à terme, la distribution de plugins tiers.

Le noyau devient ainsi une plateforme d'orchestration capable d'accueillir des extensions tout en conservant un cœur simple, stable et durable.

---

# 4. Le noyau Shikamaru

## Philosophie

Le noyau **Shikamaru** constitue le cœur d'Ohanna-Agent.

Il ne contient aucune logique métier liée à une technologie particulière.

Il fournit uniquement les services nécessaires à l'exécution des plugins et à l'orchestration des capacités.

Le noyau est volontairement :

* simple ;
* stable ;
* fortement découplé ;
* indépendant des implémentations.

Toutes les fonctionnalités spécifiques (DNS, MQTT, Docker, Home Assistant, etc.) sont destinées à être implémentées sous forme de plugins.

---

# Les composants du noyau

Le noyau est composé des services suivants :

```text
                    Application
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
    EventBus         Configuration      Memory
        │
        ├──────────────────────────────────────────┐
        │                                          │
        ▼                                          ▼
    Scheduler                               Dispatcher
        │                                          │
        └──────────────────────────────────────────┘
                           │
                           ▼
                  Capability Manager
                           │
                           ▼
                     Plugin Manager
```

Chaque composant possède une responsabilité clairement définie.

---

# Application

L'objet `Application` constitue le point d'entrée du programme.

Son rôle est limité à :

* créer les différents services du noyau ;
* injecter les dépendances ;
* démarrer le système ;
* arrêter proprement l'application.

Il ne contient aucune logique métier.

L'Application joue le rôle de **composition root**.

Toutes les dépendances y sont construites avant d'être injectées dans les composants concernés.

---

# EventBus

L'EventBus permet aux composants de communiquer sans dépendances directes.

Les événements représentent les changements significatifs du système.

Quelques exemples :

* démarrage du Scheduler ;
* arrêt du Scheduler ;
* enregistrement d'un plugin ;
* changement d'état d'une capacité.

L'EventBus réduit fortement le couplage entre les composants.

Il constitue la colonne vertébrale de l'architecture événementielle.

---

# Scheduler

Le Scheduler pilote les tâches planifiées.

Il ne connaît jamais leur implémentation.

Son rôle consiste uniquement à :

* planifier ;
* déclencher ;
* arrêter ;
* publier les événements associés.

Le Scheduler ne stocke aucun état métier.

Les informations d'exécution sont conservées dans le `SchedulerRuntime`.

---

# Dispatcher

Le Dispatcher exécute les commandes demandées par les différents composants.

Il constitue un point central pour l'exécution des actions.

Cette approche permet notamment :

* la journalisation ;
* la supervision ;
* les statistiques ;
* l'évolution future vers une exécution distribuée.

Le Dispatcher reste totalement indépendant des commandes qu'il exécute.

---

# Memory

Le système de mémoire fournit un stockage partagé entre les différents composants.

Il permet de conserver des informations nécessaires au fonctionnement du noyau.

La mémoire ne contient pas d'intelligence métier.

Elle constitue uniquement un service de stockage.

Son accès est centralisé par le `MemoryManager`.

---

# Runtime

Le Runtime représente l'état courant du système.

Il ne stocke jamais les objets métier.

Il conserve uniquement les informations liées à leur exécution.

Exemples :

* état d'un Scheduler ;
* état d'un Plugin ;
* état d'une capacité.

Cette séparation simplifie les diagnostics et la supervision.

---

# Capability Manager

Le `CapabilityManager` orchestre les capacités disponibles.

Il coordonne :

* leur enregistrement ;
* leurs dépendances ;
* leur cycle de vie ;
* leurs diagnostics.

Les capacités restent totalement indépendantes du noyau.

Le Capability Manager constitue le lien entre le Core et les plugins métier.

---

# Plugin Manager

Le `PluginManager` représente le point d'entrée du SDK de plugins.

Il orchestre :

* la découverte ;
* le chargement ;
* l'enregistrement ;
* la publication des événements.

Il ne réalise jamais directement :

* le parcours du système de fichiers ;
* le chargement Python ;
* le stockage des plugins.

Ces responsabilités sont déléguées à des composants spécialisés.

---

# Injection de dépendances

L'ensemble du noyau repose sur l'injection de dépendances.

Les composants reçoivent leurs services lors de leur construction.

Ils ne créent jamais eux-mêmes leurs dépendances.

Cette approche apporte plusieurs bénéfices :

* tests unitaires simplifiés ;
* faible couplage ;
* remplacement facile des implémentations ;
* meilleure lisibilité de l'architecture.

Le noyau reste ainsi entièrement configurable sans modification du code métier.

---

# Le rôle du noyau

Le noyau ne cherche jamais à résoudre un problème métier.

Il fournit uniquement les mécanismes nécessaires pour permettre aux plugins de remplir leur mission.

Cette distinction est essentielle.

Le Core reste volontairement petit.

Les fonctionnalités évoluent dans les plugins.

Ainsi, le noyau peut évoluer lentement tout en permettant l'ajout rapide de nouvelles capacités.

---

# 5. Le SDK de plugins

Le **Plugin SDK** constitue l'API publique officielle d'Ohanna-Agent.

Son objectif est de permettre le développement de nouvelles capacités sans modifier le noyau (*Shikamaru*).

Le SDK garantit un découplage complet entre le Core et les extensions.

---

# Philosophie

Le noyau ne connaît jamais les plugins.

Les plugins ne connaissent jamais le noyau.

Les deux communiquent exclusivement au travers de contrats publics.

Cette séparation permet :

* une API stable ;
* une meilleure testabilité ;
* une évolution indépendante du Core et des plugins ;
* une compatibilité durable des extensions.

---

# Architecture générale

Le SDK est organisé autour d'une succession de composants spécialisés.

```text id="2tt12l"
                    PluginManager
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 PluginDiscovery     PluginLoader      PluginRegistry
        │                  │                  │
        ▼                  ▼                  ▼
 DiscoveryProvider   PluginFactory     PluginRuntime
        │
        ▼
 PluginDescriptor
```

Chaque composant possède une responsabilité unique.

---

# Plugin

Le `Plugin` représente le contrat minimal que doit implémenter toute extension.

Chaque plugin expose :

* son manifeste (`PluginManifest`) ;
* sa méthode `register()`.

Le plugin ne possède aucune connaissance de l'application.

Il reçoit uniquement un `PluginContext`.

---

# PluginContext

Le `PluginContext` constitue la frontière officielle entre le Core et les plugins.

Il expose uniquement les services publics nécessaires au fonctionnement des extensions.

Par exemple :

* EventBus ;
* Scheduler ;
* Dispatcher ;
* Memory ;
* Runtime ;
* Capability Manager ;
* Configuration.

Le contexte est immuable.

Les plugins ne peuvent ni modifier sa structure, ni accéder directement au noyau.

---

# Protocoles publics

Le SDK expose des interfaces (`Protocol`) plutôt que des implémentations.

Les plugins compilent contre ces contrats publics.

Cette décision garantit que les évolutions internes du noyau n'ont pas d'impact sur les extensions.

Les protocoles représentent l'API publique officielle d'Ohanna-Agent.

---

# PluginManifest

Le manifeste décrit l'identité d'un plugin.

Il contient notamment :

* son nom ;
* sa version ;
* son auteur ;
* sa description.

Le manifeste représente les métadonnées fonctionnelles de l'extension.

---

# PluginDescriptor

Le `PluginDescriptor` représente un plugin découvert.

Il décrit uniquement son origine.

Il contient :

* son nom ;
* son emplacement sur le disque ;
* son manifeste (lorsqu'il est disponible).

Le Descriptor ne dépend pas du mécanisme de chargement.

Cette décision permet d'utiliser demain différents fournisseurs de plugins sans modifier sa structure.

---

# PluginDiscovery

Le `PluginDiscovery` orchestre la découverte des plugins disponibles.

Il ne parcourt jamais directement le système de fichiers.

Il délègue cette responsabilité à un ou plusieurs `DiscoveryProvider`.

Cette architecture permet d'ajouter facilement de nouvelles sources de plugins.

---

# DiscoveryProvider

Un `DiscoveryProvider` fournit une liste de `PluginDescriptor`.

Il ne charge jamais les plugins.

Il ne crée jamais d'instances Python.

Son unique responsabilité consiste à découvrir des plugins.

Le premier fournisseur fourni par Ohanna-Agent est :

* `LocalDirectoryProvider`

D'autres fournisseurs pourront être ajoutés ultérieurement :

* Git ;
* ZIP ;
* HTTP ;
* Marketplace ;
* NAS.

---

# PluginLoader

Le `PluginLoader` transforme un `PluginDescriptor` en instance de `Plugin`.

Il ne connaît pas le système de fichiers.

Il ne réalise aucun stockage.

Il délègue l'instanciation au `PluginFactory`.

---

# PluginFactory

Le `PluginFactory` est responsable de la création effective des plugins.

L'implémentation actuelle (`PythonPluginFactory`) :

* charge dynamiquement le module Python ;
* appelle la fonction `create_plugin()` ;
* retourne une instance de `Plugin`.

Cette abstraction permettra, à terme, d'introduire :

* des plugins isolés ;
* des plugins distants ;
* des plugins exécutés dans un environnement sécurisé.

---

# PluginRegistry

Le `PluginRegistry` constitue la source de vérité des plugins chargés.

Il assure uniquement leur stockage.

Il ne contient aucune logique métier.

Ses principales responsabilités sont :

* ajout ;
* suppression ;
* recherche ;
* énumération.

---

# PluginRuntime

Le `PluginRuntime` conserve l'état d'exécution des plugins.

Il est totalement indépendant du registre.

Cette séparation permet de distinguer :

* les objets chargés ;
* leur état courant.

Les états actuellement définis sont :

* DISCOVERED
* LOADED
* REGISTERED
* FAILED
* UNLOADED

Le Runtime constitue la source officielle des informations d'exécution.

---

# PluginManager

Le `PluginManager` orchestre l'ensemble du SDK.

Il coordonne :

* la découverte ;
* le chargement ;
* l'enregistrement ;
* le Runtime ;
* la publication des événements.

Il ne réalise lui-même aucune opération technique.

Toutes les responsabilités sont déléguées aux composants spécialisés.

---

# Cycle de vie

Le cycle de vie d'un plugin est volontairement simple.

```text id="0tywr2"
DISCOVERED
      │
      ▼
LOADED
      │
      ▼
REGISTERED
      │
      ▼
UNLOADED
```

Chaque transition est enregistrée dans le `PluginRuntime`.

Les changements importants peuvent être publiés sur l'EventBus.

---

# Objectifs du SDK

Le Plugin SDK poursuit plusieurs objectifs :

* garantir une API publique stable ;
* préserver le découplage du noyau ;
* simplifier le développement des extensions ;
* préparer le Dashboard Web ;
* préparer l'intégration Home Assistant ;
* préparer un futur Marketplace de plugins.

Le SDK constitue désormais l'un des piliers de l'architecture d'Ohanna-Agent.

---

# 6. Patterns architecturaux

Au fil du développement du projet, plusieurs patterns se sont progressivement imposés.

Ils constituent désormais les règles de conception recommandées pour tous les nouveaux composants.

---

# Registry

Le **Registry** représente la mémoire métier d'un domaine.

Il stocke les objets sans appliquer de logique particulière.

Exemples :

* PluginRegistry
* CapabilityRegistry

Responsabilités :

* ajout ;
* suppression ;
* recherche ;
* énumération.

Le Registry ne connaît jamais l'état d'exécution des objets qu'il stocke.

---

# Runtime

Le **Runtime** représente l'état d'exécution d'un domaine.

Il ne stocke jamais les objets eux-mêmes.

Il conserve uniquement les informations dynamiques.

Exemples :

* PluginRuntime
* SchedulerRuntime

Cette séparation permet d'enrichir progressivement les informations d'exécution sans modifier les objets métier.

À terme, un Runtime pourra contenir :

* état courant ;
* date de démarrage ;
* durée d'exécution ;
* nombre d'erreurs ;
* dernière erreur ;
* métriques.

Le Runtime constitue la source officielle des informations d'exécution.

---

# Manager

Le **Manager** orchestre un sous-système.

Il ne possède ni stockage interne, ni logique technique spécifique.

Son rôle consiste uniquement à coordonner les composants spécialisés.

Exemples :

* PluginManager
* CapabilityManager
* MemoryManager

Le Manager représente le point d'entrée d'un domaine.

---

# Provider

Un **Provider** fournit des informations au noyau.

Il ne stocke aucun état.

Il n'applique aucune logique métier.

Son rôle consiste uniquement à produire des données.

Premier exemple :

* DiscoveryProvider

À terme, d'autres Providers pourront apparaître :

* GitProvider
* HttpProvider
* MarketplaceProvider
* MetricsProvider
* HealthProvider

Cette approche facilite l'ajout de nouvelles sources de données sans modifier les composants existants.

---

# Factory

Une **Factory** est responsable de l'instanciation d'objets complexes.

Elle encapsule les mécanismes de création.

Le reste du système ignore totalement les détails d'instanciation.

Exemple :

* PythonPluginFactory

Cette approche permettra ultérieurement de supporter différents mécanismes de chargement sans modifier le `PluginLoader`.

---

# Architecture cible

Tous les futurs domaines d'Ohanna-Agent sont encouragés à suivre la même organisation.

```text id="b6lqf8"
                 Manager
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
    Registry                  Runtime
        │
        ▼
     Domain Objects
```

Lorsqu'un domaine nécessite plusieurs sources de données, des Providers viennent compléter cette architecture.

Cette homogénéité facilite la maintenance et accélère la compréhension du code.

---

# 7. Flux d'exécution

## Démarrage de l'application

Au lancement d'Ohanna-Agent :

```text id="f7tk44"
Application
      │
      ▼
Création des services
      │
      ▼
Injection des dépendances
      │
      ▼
Initialisation des Managers
      │
      ▼
Démarrage du Scheduler
      │
      ▼
Démarrage du PluginManager
```

Le noyau est alors prêt à accueillir les plugins.

---

## Chargement des plugins

Le cycle complet est le suivant :

```text id="q9tv0d"
Filesystem
      │
      ▼
LocalDirectoryProvider
      │
      ▼
PluginDiscovery
      │
      ▼
PluginDescriptor
      │
      ▼
PluginLoader
      │
      ▼
PythonPluginFactory
      │
      ▼
Plugin
      │
      ▼
PluginRegistry
      │
      ▼
PluginRuntime
      │
      ▼
PluginManager
```

Chaque étape possède une responsabilité clairement définie.

Le noyau reste indépendant des mécanismes techniques utilisés.

---

## Cycle de vie des plugins

```text id="ymjn9d"
DISCOVERED
      │
      ▼
LOADED
      │
      ▼
REGISTERED
      │
      ▼
UNLOADED
```

Chaque changement d'état est enregistré dans le `PluginRuntime`.

Les événements importants sont publiés sur l'EventBus.

---

# 8. Évolutions prévues

Le noyau actuel est désormais considéré comme stable.

Les évolutions futures concerneront principalement les extensions.

---

## Plugins métier

Les prochaines capacités seront développées sous forme de plugins indépendants.

Les premiers plugins prévus sont :

* DNS
* DHCP
* MQTT
* Docker
* Home Assistant
* Sauvegardes
* Reverse Proxy

Le noyau ne nécessitera aucune modification pour les accueillir.

---

## Dashboard Web

Une interface Web indépendante de Home Assistant permettra de visualiser :

* les capacités disponibles ;
* les plugins installés ;
* leur état ;
* les diagnostics ;
* les événements ;
* les actions en cours.

Le Dashboard s'appuiera directement sur les Runtime du noyau.

Aucune logique métier supplémentaire ne sera nécessaire.

---

## Intégration Home Assistant

Une intégration native Home Assistant permettra d'exposer :

* les capacités ;
* les diagnostics ;
* les métriques ;
* les événements ;
* les états des plugins.

Home Assistant deviendra un consommateur des données du noyau, et non l'inverse.

---

## Marketplace

À long terme, Ohanna-Agent pourra intégrer un système de distribution de plugins.

Le SDK actuel a été conçu pour supporter cette évolution sans remise en cause de son architecture.

De nouveaux `DiscoveryProvider` pourront découvrir des plugins depuis :

* Git ;
* HTTP ;
* ZIP ;
* Marketplace ;
* stockage réseau.

Le reste du système restera inchangé.

---

# Conclusion

Le noyau **Shikamaru** est désormais conçu comme une plateforme d'orchestration.

Son rôle n'est pas de superviser des logiciels, mais de garantir durablement les capacités de l'infrastructure.

Le SDK de plugins constitue l'API publique officielle du projet.

Cette architecture privilégie :

* la stabilité ;
* le découplage ;
* la testabilité ;
* l'évolutivité.

Elle permet de faire évoluer Ohanna-Agent par l'ajout de nouvelles extensions plutôt que par la modification du noyau.

Le cœur du système reste ainsi simple, robuste et durable, tandis que les fonctionnalités évoluent indépendamment au rythme des besoins de l'infrastructure.

# CORE.md

# Manuel d'Architecture d'Ohanna-Agent

Version : **4.0**

Version du Framework : **v0.4.0 – Autonomous Core**

---

# Préface

## Pourquoi ce document ?

Le présent document constitue la référence architecturale officielle d'Ohanna-Agent.

Contrairement au `README.md`, dont l'objectif est de présenter le projet et de faciliter sa découverte, le document **CORE.md** décrit en détail les principes de conception, les composants internes et les règles qui structurent le framework.

Il s'adresse principalement :

* aux développeurs souhaitant contribuer au projet ;
* aux architectes logiciels ;
* aux mainteneurs du framework ;
* à toute personne désirant comprendre en profondeur le fonctionnement interne d'Ohanna-Agent.

Ce document n'a pas vocation à expliquer l'utilisation quotidienne du framework. Son rôle est de décrire son architecture, les choix qui la sous-tendent et les règles qui garantissent sa cohérence au fil des évolutions.

---

# 1. Vision

## 1.1 Origine du projet

Ohanna-Agent est né d'un constat simple.

La majorité des solutions d'automatisation sont construites autour d'une accumulation de fonctionnalités répondant à des besoins immédiats. Avec le temps, ces projets deviennent souvent difficiles à maintenir, fortement couplés et complexes à faire évoluer.

L'objectif d'Ohanna-Agent est différent.

Le framework est conçu autour d'une architecture stable, modulaire et extensible, dans laquelle chaque nouvelle fonctionnalité vient naturellement s'intégrer sans remettre en cause les fondations existantes.

L'architecture précède les fonctionnalités.

---

## 1.2 Vision à long terme

Ohanna-Agent ambitionne de devenir un framework généraliste permettant de construire des agents logiciels autonomes.

Ces agents doivent être capables de :

* recevoir des événements provenant de différentes sources ;
* analyser leur contexte ;
* planifier des traitements ;
* orchestrer plusieurs actions ;
* prendre des décisions selon des règles définies ;
* communiquer via MQTT ou d'autres transports ;
* évoluer sans modifier le noyau du framework.

Le projet privilégie la robustesse de son architecture plutôt que la multiplication rapide des fonctionnalités.

---

## 1.3 Le rôle du Kernel

Le noyau d'Ohanna-Agent constitue une plateforme d'exécution.

Il ne contient volontairement aucune logique métier spécifique.

Son rôle est de fournir les mécanismes communs nécessaires à tous les agents :

* gestion du cycle de vie ;
* exécution des commandes ;
* planification des tâches ;
* communication par événements ;
* gestion des capacités ;
* infrastructure MQTT ;
* supervision de l'état d'exécution.

Toutes les fonctionnalités métier doivent être construites au-dessus de ce noyau.

Cette séparation garantit la pérennité de l'architecture.

---

## 1.4 Une architecture orientée plateforme

À partir de la version **0.4.0**, Ohanna-Agent n'est plus simplement un agent logiciel.

Il constitue désormais une plateforme sur laquelle peuvent être développés plusieurs moteurs spécialisés.

Par exemple :

* moteur de workflows ;
* moteur de règles ;
* moteur de pipelines ;
* moteur d'événements complexes ;
* capacités métier spécialisées.

Tous ces composants s'appuient sur les mêmes abstractions définies par le noyau.

---

# 2. Philosophie

## 2.1 L'architecture avant les fonctionnalités

Chaque évolution commence par une réflexion architecturale.

Une fonctionnalité n'est intégrée que lorsqu'elle peut trouver naturellement sa place dans le modèle existant.

Lorsque ce n'est pas le cas, c'est généralement le signe que le problème n'est pas encore suffisamment compris.

Cette discipline permet d'éviter la création de composants redondants ou fortement couplés.

---

## 2.2 Une responsabilité unique

Chaque composant possède un rôle clairement identifié.

Le Scheduler orchestre les tâches.

Le Dispatcher exécute les commandes.

Le Runtime décrit l'état d'exécution.

Une Registry stocke des objets.

Un Executor réalise une action.

Aucun composant ne cumule plusieurs responsabilités.

Cette règle constitue l'un des principes fondamentaux du framework.

---

## 2.3 Le découplage comme principe directeur

Les différents services du noyau ne communiquent jamais directement avec leurs implémentations concrètes.

Ils utilisent des contrats, des abstractions ou des protocoles.

Cette approche permet notamment :

* de remplacer une implémentation sans modifier les consommateurs ;
* de faciliter les tests unitaires ;
* d'introduire de nouvelles stratégies d'exécution ;
* de limiter les dépendances entre modules.

Le découplage est systématiquement privilégié lorsqu'il améliore la lisibilité et l'évolutivité du projet.

---

## 2.4 La testabilité comme exigence

Chaque composant est conçu pour être testé indépendamment.

Cette exigence influence directement les choix d'architecture.

Ainsi :

* les accès au temps utilisent une abstraction (`Clock`) ;
* les registres sont isolés ;
* les exécuteurs sont interchangeables ;
* les dépendances sont injectées plutôt que créées localement.

Grâce à cette approche, l'ensemble du framework peut être validé rapidement par une suite de plusieurs centaines de tests unitaires.

---

## 2.5 La simplicité

La sophistication d'une architecture ne doit jamais provenir de la complexité de ses composants.

Elle doit résulter de leur combinaison.

Chaque classe doit rester suffisamment petite pour être comprise rapidement.

Chaque méthode doit exprimer clairement son intention.

Chaque composant doit pouvoir évoluer indépendamment.

La simplicité constitue un objectif permanent.

---

## 2.6 La stabilité du noyau

Le Kernel représente la partie la plus stable du framework.

Les fonctionnalités évoluent.

Les capacités évoluent.

Les plugins évoluent.

Le noyau, lui, doit rester aussi stable que possible.

Cette stabilité est obtenue grâce à des interfaces bien définies, des responsabilités clairement séparées et une architecture pensée pour durer.

---

## 2.7 L'amélioration continue

L'architecture d'Ohanna-Agent n'est pas figée.

Elle évolue progressivement au rythme des retours d'expérience, des audits d'architecture et des nouveaux besoins.

Toute évolution importante suit le même processus :

1. analyse du besoin ;
2. conception de l'architecture ;
3. implémentation ;
4. tests unitaires ;
5. revue d'architecture ;
6. documentation ;
7. publication.

Ce cycle garantit une évolution maîtrisée du framework.

---

## Conclusion

La philosophie d'Ohanna-Agent repose sur une idée simple :

**Construire un framework dont l'architecture reste plus stable que les fonctionnalités qu'il héberge.**

Cette approche demande davantage de rigueur au début du projet, mais elle offre en retour une excellente évolutivité, une forte testabilité et une maintenance simplifiée.

Les chapitres suivants décrivent les principes d'architecture qui permettent d'atteindre cet objectif.

---

# 3. Principes d'architecture

Les principes décrits dans ce chapitre constituent les règles fondamentales de conception d'Ohanna-Agent.

Ils s'appliquent à l'ensemble du noyau, aux services, aux plugins et aux futures extensions.

Toute évolution du framework doit respecter ces principes afin de préserver la cohérence globale de l'architecture.

---

## 3.1 Responsabilité unique

Chaque composant possède une responsabilité clairement définie.

Le Scheduler planifie.

Le Dispatcher exécute.

Le Runtime décrit l'état d'exécution.

Une Registry stocke des objets.

Un Executor réalise une exécution.

Cette séparation volontaire limite le couplage entre les différentes parties du framework.

Une classe qui commence à remplir plusieurs rôles doit être refactorisée.

---

## 3.2 Découplage

Le découplage constitue le principe directeur de l'ensemble du projet.

Les services ne doivent jamais connaître les détails d'implémentation des autres services.

Par exemple :

```text
Scheduler
      │
      ▼
TaskExecutor
```

et non :

```text
Scheduler
      │
      ▼
Dispatcher
```

Le Scheduler ignore complètement la manière dont une tâche est exécutée.

Il délègue cette responsabilité à un `TaskExecutor`.

Cette approche permet de remplacer une implémentation sans modifier le Scheduler.

---

## 3.3 Composition

Ohanna-Agent privilégie systématiquement la composition.

Les composants collaborent.

Ils ne s'héritent pas.

Par exemple :

```text
Scheduler
│
├── TaskRegistry
├── TaskExecutor
├── SchedulerRuntime
└── Clock
```

Le Scheduler ne dérive d'aucune de ces classes.

Il les utilise.

Cette approche réduit les dépendances et facilite les évolutions.

---

## 3.4 Injection des dépendances

Les dépendances sont injectées lors de la construction des composants.

Exemple :

```python
scheduler = Scheduler(
    executor=DispatcherTaskExecutor(dispatcher),
    clock=FakeClock(),
)
```

Le Scheduler ne crée jamais lui-même son exécuteur ou son horloge.

Cette règle améliore considérablement la testabilité du framework.

---

## 3.5 Contrats avant implémentations

Les composants communiquent au travers de contrats clairement définis.

Par exemple :

* `TaskExecutor`
* `Registry`
* `Executor`

Les implémentations concrètes restent interchangeables.

Cette séparation permet notamment :

* l'utilisation de doubles de test ;
* l'évolution indépendante des implémentations ;
* l'introduction de nouvelles stratégies sans casser l'API.

---

## 3.6 Runtime séparé

Chaque service possède un objet Runtime.

Le Runtime contient exclusivement les informations liées à l'exécution :

* état courant ;
* dates de démarrage ;
* dates d'arrêt ;
* statistiques ;
* informations temporaires.

Il ne contient jamais de logique métier.

Cette séparation permet de distinguer clairement :

* la logique du service ;
* son état d'exécution.

---

## 3.7 Objets spécialisés

Chaque concept important du framework possède son propre type.

Par exemple :

* Runtime
* Registry
* Statistics
* State
* Executor

Cette approche augmente la lisibilité du code et facilite les évolutions futures.

---

## 3.8 Interfaces stables

Les API publiques doivent rester stables.

Les changements d'implémentation ne doivent pas modifier le contrat visible par les autres composants.

Cette stabilité constitue une condition essentielle pour permettre l'évolution indépendante des modules.

---

# 4. Architecture globale

L'architecture d'Ohanna-Agent est organisée autour d'un noyau modulaire.

Chaque service possède une responsabilité unique et communique avec les autres services au travers de contrats bien définis.

Le schéma suivant représente l'organisation générale du framework.

```text
                        Application
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼

  Configuration          Dispatcher          Scheduler
        │                     │                     │
        │                     ▼                     ▼
        │                 Command             TaskRegistry
        │                     │                     │
        │                     ▼                     ▼
        │                  Action                 Task
        │                                           │
        │                                           ▼
        │                                      BaseTrigger
        │
        ├───────────────────────────────────────────────┐
        ▼                                               ▼

 Capability Manager                              MQTT Runtime
        │                                               │
        ▼                                               ▼

   Capabilities                                 Publisher
                                                 Subscriber
```

---

## 4.1 Le rôle de l'Application

L'Application constitue le point d'entrée du framework.

Elle est responsable de :

* l'initialisation des services ;
* leur cycle de vie ;
* leur orchestration générale.

Elle ne contient aucune logique métier.

Son rôle est uniquement de composer les différents composants du noyau.

---

## 4.2 Les services du Kernel

Le noyau est composé de plusieurs services indépendants.

Chaque service est spécialisé.

### Configuration

Gestion de la configuration.

### Dispatcher

Exécution des commandes.

### Scheduler

Planification des traitements.

### MQTT Runtime

Communication avec le broker MQTT.

### Capability Manager

Gestion des capacités disponibles.

### Event Bus

Diffusion des événements internes.

---

## 4.3 Les dépendances

Les dépendances suivent une seule direction.

```text
Application
      │
      ▼
Scheduler
      │
      ▼
TaskExecutor
      │
      ▼
Dispatcher
      │
      ▼
Command
      │
      ▼
Action
```

Aucune couche ne dépend d'une couche supérieure.

Cette règle est impérative.

---

## 4.4 Les composants spécialisés

Chaque grand service est lui-même composé de plusieurs sous-composants.

Par exemple :

```text
Scheduler

Runtime

Registry

Executor

Task

Trigger

Clock
```

Cette organisation facilite les tests et limite la taille de chaque classe.

---

## 4.5 Une architecture orientée plateforme

Le noyau ne contient volontairement aucune logique métier.

Il fournit uniquement les mécanismes communs nécessaires aux futurs moteurs :

* Workflow Engine
* Rule Engine
* Pipeline Engine
* Event Engine

Ces moteurs viendront s'appuyer sur le Kernel sans modifier son architecture.

Cette séparation garantit la stabilité du framework sur le long terme.

---

# 5. Le Kernel

## 5.1 Présentation

Le **Kernel** constitue le cœur d'Ohanna-Agent.

Il fournit l'ensemble des services fondamentaux nécessaires au fonctionnement du framework.

Contrairement aux capacités, aux plugins ou aux futurs moteurs (Workflow, Rule Engine, Pipeline), le Kernel ne contient aucune logique métier.

Son rôle est exclusivement de fournir une infrastructure stable, modulaire et extensible.

L'ensemble des composants du framework repose sur ce noyau.

---

## 5.2 Responsabilités du Kernel

Le Kernel est responsable de :

* l'initialisation du framework ;
* la gestion du cycle de vie des services ;
* la réception et l'exécution des commandes ;
* la planification des traitements ;
* la diffusion des événements internes ;
* la gestion des capacités ;
* l'infrastructure de communication MQTT ;
* les abstractions communes utilisées par les différents services.

Toutes les fonctionnalités métier sont volontairement construites au-dessus de cette couche.

---

## 5.3 Vue d'ensemble

Le Kernel est composé de plusieurs services spécialisés.

```text
                             Application
                                   │
     ┌───────────────┬─────────────┼─────────────┬───────────────┐
     ▼               ▼             ▼             ▼               ▼

Configuration   Dispatcher    Scheduler   Capability Manager   MQTT Runtime
                                      │
                                      ▼
                                 Event Bus
```

Chaque service possède une responsabilité unique.

Aucun service ne cumule plusieurs rôles.

---

# 5.4 L'Application

L'Application constitue le point d'entrée du framework.

Elle assemble les différents services du noyau.

Son rôle est volontairement limité.

L'Application :

* construit les composants ;
* injecte leurs dépendances ;
* initialise le Kernel ;
* démarre les services ;
* orchestre leur arrêt.

Elle ne contient aucune logique métier.

Elle ne traite aucun message MQTT.

Elle ne prend aucune décision.

Elle agit uniquement comme orchestrateur.

---

## Cycle de vie

Le cycle de vie d'une Application suit la séquence suivante.

```text
CREATED
    │
    ▼
INITIALIZING
    │
    ▼
RUNNING
    │
    ▼
STOPPING
    │
    ▼
STOPPED
```

Chaque transition est explicite.

---

# 5.5 Le Dispatcher

Le Dispatcher constitue le centre d'exécution du framework.

Tous les traitements passent obligatoirement par lui.

Sa responsabilité est simple :

> Recevoir une commande et déclencher l'action correspondante.

Le Dispatcher ignore totalement l'origine de cette commande.

Elle peut provenir :

* du Scheduler ;
* du Runtime MQTT ;
* d'un Plugin ;
* d'une Capability ;
* d'un futur Workflow Engine.

Toutes ces sources sont traitées de manière identique.

---

## Architecture

```text
Dispatcher
      │
      ▼
Command
      │
      ▼
Action
```

Le Dispatcher ne connaît jamais les implémentations concrètes des Actions.

---

# 5.6 Le Scheduler

Le Scheduler introduit dans la version **0.4.0** constitue le premier composant permettant à Ohanna-Agent de devenir autonome.

Contrairement au Dispatcher, qui réagit aux événements, le Scheduler est capable d'initier des traitements.

Il ne prend toutefois aucune décision métier.

Sa responsabilité consiste uniquement à déterminer quelles tâches doivent être exécutées.

---

## Architecture

```text
Scheduler
     │
     ├── Runtime
     ├── Registry
     ├── Executor
     ├── Clock
     └── Tasks
```

Chaque sous-composant possède une responsabilité clairement identifiée.

---

## Principe d'exécution

```text
Clock
   │
   ▼
Trigger
   │
   ▼
Task
   │
   ▼
TaskRegistry
   │
   ▼
Scheduler
   │
   ▼
TaskExecutor
   │
   ▼
Dispatcher
```

Le Scheduler ignore complètement la manière dont une tâche est réellement exécutée.

Il délègue cette responsabilité au `TaskExecutor`.

Cette séparation garantit un découplage fort entre la planification et l'exécution.

---

# 5.7 Le Capability Manager

Le Capability Manager gère l'ensemble des capacités installées dans le framework.

Une capacité représente une fonctionnalité autonome pouvant être activée ou désactivée indépendamment.

Exemples :

* Health
* Monitor
* Watchdog
* Heartbeat
* Auto-Recovery

Chaque capacité possède son propre cycle de vie.

Le Capability Manager ne connaît pas leur logique interne.

---

# 5.8 Le Runtime MQTT

Le Runtime MQTT assure la communication avec le broker.

Ses responsabilités sont volontairement limitées :

* établir la connexion ;
* publier les messages ;
* recevoir les abonnements ;
* gérer les reconnexions ;
* notifier le Dispatcher.

Le Runtime MQTT ne contient aucune logique métier.

---

## Architecture

```text
MQTT Runtime
      │
      ├── Publisher
      ├── Subscriber
      ├── Monitor
      ├── Reconnect
      └── Transport
```

Chaque sous-composant reste indépendant.

---

# 5.9 L'Event Bus

L'Event Bus constitue le mécanisme de communication interne du Kernel.

Il permet aux différents services de publier des événements sans connaître leurs consommateurs.

Cette approche réduit fortement les dépendances entre modules.

Le Scheduler pourra, par exemple, publier :

```text
task.started

task.finished

task.failed
```

sans connaître les composants qui les traiteront.

---

# 5.10 Les abstractions communes

L'ensemble des services du Kernel repose sur plusieurs abstractions partagées.

```text
core/

Runtime

Statistics

Registry

Executor
```

Ces abstractions constituent le langage commun du framework.

Tous les nouveaux services sont encouragés à les utiliser lorsqu'elles répondent à leur besoin.

---

# Conclusion

Le Kernel représente la partie la plus stable d'Ohanna-Agent.

Son objectif n'est pas de fournir des fonctionnalités métier, mais une infrastructure fiable, cohérente et extensible sur laquelle pourront être construits les moteurs intelligents des prochaines versions.

Les chapitres suivants détaillent les abstractions communes (`Runtime`, `Registry`, `Executor`, `State`, `Statistics`) qui permettent à l'ensemble des services du Kernel de partager un modèle architectural homogène.

---

# 6. Les Contrats du Kernel (`core`)

## 6.1 Introduction

L'une des évolutions majeures introduites avec la version **0.4.0** est l'apparition d'un ensemble d'abstractions communes regroupées dans le package `core`.

Ces abstractions ne représentent pas des fonctionnalités.

Elles définissent un **langage architectural** partagé par l'ensemble du framework.

Chaque nouveau service peut s'appuyer sur ces contrats afin de respecter les mêmes principes de conception.

Cette approche favorise :

* la cohérence du code ;
* le découplage entre les composants ;
* la réutilisation des concepts ;
* la simplicité de maintenance ;
* l'évolutivité du framework.

---

# 6.2 Les abstractions communes

Le package `core` regroupe les contrats fondamentaux suivants.

```text
core/

Runtime

Statistics

Registry

Executor
```

Ces quatre concepts constituent la base de l'ensemble des services du Kernel.

---

# 6.3 Runtime

## Objectif

Un **Runtime** représente exclusivement l'état d'exécution d'un service.

Il ne contient jamais de logique métier.

Le Runtime est un objet d'observation.

Il décrit le fonctionnement courant d'un composant sans participer à son comportement.

---

## Responsabilités

Un Runtime peut notamment contenir :

* état courant ;
* date de démarrage ;
* date d'arrêt ;
* dernier événement ;
* informations temporaires ;
* statistiques d'exécution.

Il ne réalise jamais de traitement.

---

## Exemple

```text
Scheduler
      │
      ▼
SchedulerRuntime
```

Le Scheduler reste responsable de l'orchestration.

Le Runtime décrit uniquement son état.

---

## Règles

Un Runtime :

* ne contient aucune logique métier ;
* ne décide jamais ;
* n'appelle aucun autre service ;
* peut être observé à tout moment ;
* est sérialisable si nécessaire.

---

# 6.4 Statistics

## Objectif

Les statistiques représentent des mesures cumulées produites par un service.

Elles sont volontairement séparées du Runtime afin de distinguer :

* l'état courant ;
* les indicateurs historiques.

---

## Exemples

```text
SchedulerStatistics

tasks_executed

tasks_failed

tick_count
```

---

D'autres services pourront disposer de leurs propres statistiques :

```text
HeartbeatStatistics

ReconnectStatistics

MonitorStatistics
```

Chaque service reste libre de définir les métriques qui lui sont pertinentes.

---

## Règles

Une classe Statistics :

* contient uniquement des compteurs ;
* ne possède aucune logique métier complexe ;
* ne déclenche jamais d'action ;
* peut être remise à zéro.

---

# 6.5 Registry

## Objectif

Une Registry est responsable du stockage et de la recherche d'objets.

Elle constitue l'unique point d'accès à une collection.

Elle remplace l'utilisation directe des structures de données internes.

---

## Exemple

```text
TaskRegistry

Task

Task

Task
```

Le Scheduler ne manipule jamais directement une collection de tâches.

Toute interaction passe par le TaskRegistry.

---

## Avantages

Cette approche facilite :

* le remplacement du stockage ;
* l'ajout de persistance ;
* les recherches avancées ;
* la validation des accès ;
* la journalisation.

---

## Futures implémentations

À terme, une Registry pourra s'appuyer sur :

* un dictionnaire mémoire ;
* SQLite ;
* PostgreSQL ;
* Redis ;
* un stockage distribué.

Le reste du framework restera inchangé.

---

## Règles

Une Registry :

* ne contient aucune logique métier ;
* ne prend aucune décision ;
* ne déclenche aucune exécution ;
* gère uniquement une collection.

---

# 6.6 Executor

## Objectif

Un Executor représente le composant responsable d'une exécution.

Il ne décide jamais quoi exécuter.

Il exécute ce qui lui est demandé.

---

## Exemple

```text
Scheduler
      │
      ▼
TaskExecutor
      │
      ▼
DispatcherTaskExecutor
```

Le Scheduler décide qu'une tâche doit être exécutée.

Le TaskExecutor réalise effectivement cette exécution.

---

## Pourquoi cette séparation ?

Cette architecture permet de remplacer facilement l'implémentation.

Par exemple :

```text
TaskExecutor
      │
      ├── DispatcherTaskExecutor
      ├── DryRunTaskExecutor
      ├── AsyncTaskExecutor
      ├── RemoteTaskExecutor
      └── WorkflowTaskExecutor
```

Le Scheduler reste strictement identique.

---

## Règles

Un Executor :

* exécute ;
* ne planifie jamais ;
* ne stocke jamais ;
* ne décide jamais.

---

# 6.7 Les contrats comme langage commun

L'ensemble du Kernel repose désormais sur quatre concepts simples.

```text
Service
      │
      ├── Runtime
      ├── Statistics
      ├── Registry
      └── Executor
```

Chaque nouveau service est invité à réutiliser ces abstractions lorsque cela est pertinent.

Cette homogénéité facilite la compréhension du framework.

---

# 6.8 Évolution des services

Le modèle suivant est désormais recommandé.

```text
Service
│
├── Runtime
├── Statistics
├── State
├── Registry
├── Executor
└── Models
```

Tous les services n'utiliseront pas nécessairement chacun de ces composants.

Ils constituent cependant une boîte à outils commune permettant de construire une architecture cohérente.

---

# 6.9 Les bénéfices

L'introduction des contrats `core` apporte plusieurs avantages majeurs.

## Cohérence

Tous les services partagent désormais le même vocabulaire architectural.

---

## Testabilité

Les composants peuvent être testés indépendamment grâce à des contrats clairement définis.

---

## Évolutivité

Les implémentations peuvent évoluer sans modifier les consommateurs.

---

## Lisibilité

Les responsabilités sont immédiatement identifiables.

Le nom d'une classe indique clairement son rôle.

---

## Maintenabilité

Les évolutions futures peuvent s'appuyer sur des concepts déjà présents dans le framework plutôt que d'introduire de nouveaux modèles.

---

# Conclusion

Les abstractions du package `core` constituent désormais le socle architectural d'Ohanna-Agent.

Elles ne représentent pas des fonctionnalités du framework.

Elles définissent sa manière de construire des composants.

Grâce à ces contrats, les futurs services (Workflow Engine, Rule Engine, Pipeline Engine, moteurs d'événements ou nouvelles capacités) pourront être développés selon les mêmes principes de conception, garantissant ainsi la cohérence et la pérennité de l'architecture.

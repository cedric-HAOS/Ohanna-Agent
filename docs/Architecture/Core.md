# CORE

> Architecture interne du noyau **Shikamaru**

Version : 4.0

---

# Objectif

Ce document décrit l'architecture interne du noyau **Shikamaru**, cœur du projet **Ohanna-Agent**.

Il constitue la référence technique de l'implémentation.

Les décisions d'architecture détaillées sont documentées dans les ADR.

Le présent document décrit leur traduction dans le code.

---

# Vision

Shikamaru est un framework Python destiné à construire des agents autonomes capables de fournir des services d'infrastructure.

Le noyau fournit toutes les briques communes :

- cycle de vie de l'application ;
- gestion de la configuration ;
- bus d'événements ;
- commandes ;
- services partagés ;
- runtime MQTT ;
- supervision interne ;
- moteur d'auto-réparation.

Les fonctionnalités métier sont développées sous forme de plugins indépendants.

---

# Principes d'architecture

Le noyau repose sur plusieurs principes fondamentaux.

## Responsabilité unique

Chaque composant possède une responsabilité clairement définie.

Exemples :

- le Dispatcher distribue les événements ;
- le Health Monitor supervise ;
- le Recovery Engine orchestre les récupérations ;
- les plugins implémentent les services métier.

---

## Faible couplage

Les composants communiquent via :

- événements ;
- interfaces ;
- protocoles ;
- services injectés.

Les dépendances directes sont limitées au strict nécessaire.

---

## Architecture événementielle

Toutes les interactions métier transitent par le bus d'événements.

```text
Plugin

↓

Dispatcher

↓

Event Bus

↓

Subscribers
```

Cette architecture facilite :

- l'ajout de nouvelles fonctionnalités ;
- les tests unitaires ;
- l'évolution du framework.

---

## Modularité

Chaque package constitue une brique indépendante.

```text
configuration

core

events

mqtt

health

recovery

plugins

services
```

Chaque package peut évoluer indépendamment des autres.

---

## Résilience

Le noyau surveille en permanence son propre état.

La supervision est séparée de la récupération.

```text
Observation

↓

Diagnostic

↓

Décision

↓

Action
```

Cette séparation est volontaire.

---

# Vue générale

L'architecture complète est organisée selon les couches suivantes.

```text
                     Plugins
                         │
                         ▼
                  Event Dispatcher
                         │
                         ▼
                     Event Bus
                         │
                         ▼
                    Application
                         │
 ┌──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼              ▼
Configuration Services      Scheduler      MQTT
                                            │
                                ┌───────────┴───────────┐
                                ▼                       ▼
                           Publisher              Subscriber

                         ▼
                  Health Monitor
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Health Checks            Watchdogs
                                      │
                                      ▼
                                 Heartbeats

                         ▼
                  Recovery Engine
                         │
                         ▼
                  Recovery Policy
                         │
                         ▼
                 Recovery Strategy
                         │
                         ▼
                  Recovery Action
```

---

# Organisation des packages

Le dépôt est organisé de la manière suivante.

```text
ohanna-agent/

application.py

configuration/

core/

events/

mqtt/

health/

recovery/

plugins/

services/

tests/

docs/

config/
```

Chaque package possède une responsabilité clairement identifiée.

---

# Application

Le point d'entrée du framework est l'application.

Elle orchestre :

- l'initialisation ;
- le démarrage ;
- l'arrêt ;
- les services communs.

```text
Application

↓

Initialize()

↓

Run()

↓

Stop()
```

L'application ne contient aucune logique métier.

Elle agit comme orchestrateur.

---

# Configuration

Le package `configuration` centralise toute la configuration.

Responsabilités :

- lecture des fichiers YAML ;
- validation ;
- valeurs par défaut ;
- exposition des paramètres.

La validation repose sur **Pydantic**.

Les principales sections sont :

```text
Agent

MQTT

Logging

Health

Plugins
```

Chaque section possède son propre modèle fortement typé.

---

# Cycle de vie

Le cycle de vie est entièrement centralisé.

États possibles :

```text
CREATED

↓

INITIALIZING

↓

READY

↓

RUNNING

↓

STOPPING

↓

STOPPED
```

En cas d'erreur fatale :

```text
RUNNING

↓

ERROR
```

Toutes les transitions sont validées par le `LifecycleManager`.

Aucun composant ne modifie directement son état.

---

# Services

Les services représentent les dépendances partagées.

Exemples :

- Logger
- Dispatcher
- MQTT Client
- Scheduler
- Health Monitor
- Recovery Engine

Ils sont injectés aux composants qui en ont besoin.

Cette approche facilite :

- les tests ;
- le remplacement des implémentations ;
- le découplage.

---

# Scheduler

Le Scheduler permet d'exécuter des traitements périodiques.

Exemples futurs :

- Health Checks
- Watchdogs
- Métriques
- Heartbeats
- Maintenance

Le Scheduler reste indépendant des traitements exécutés.

Chaque tâche est enregistrée dynamiquement.

---

# Architecture événementielle

L'architecture de Shikamaru repose entièrement sur un modèle **Event-Driven**.

Les composants ne s'appellent pas directement entre eux.

Ils communiquent exclusivement par des événements.

```text
            Producer
                │
                ▼
          Event Dispatcher
                │
                ▼
            Event Bus
                │
      ┌─────────┴─────────┐
      ▼                   ▼
 Subscriber A       Subscriber B
```

Cette architecture apporte plusieurs avantages :

- faible couplage ;
- extensibilité ;
- testabilité ;
- isolation des composants.

---

# Dispatcher

Le Dispatcher constitue le centre névralgique du framework.

Responsabilités :

- enregistrer les abonnements ;
- distribuer les événements ;
- exécuter les handlers ;
- isoler les producteurs des consommateurs.

Il ne possède aucune connaissance métier.

---

# Événements

Chaque événement est représenté par un objet métier.

Principes :

- immuable ;
- typé ;
- horodaté ;
- sérialisable.

Exemples :

```text
ApplicationStartedEvent

PluginLoadedEvent

PluginStoppedEvent

MQTTConnectedEvent

MQTTDisconnectedEvent

HealthStatusChangedEvent

RecoveryStartedEvent

RecoveryCompletedEvent
```

Les événements constituent le langage interne de Shikamaru.

---

# Commandes

Les commandes représentent les actions demandées au système.

Contrairement aux événements, elles expriment une intention.

Exemples :

```text
StartPluginCommand

StopPluginCommand

RestartPluginCommand

ReloadConfigurationCommand

RunHealthCheckCommand

RecoverPluginCommand
```

Le Dispatcher distribue également les commandes.

---

# Messages

Les messages sont utilisés principalement par le runtime MQTT.

Ils encapsulent :

- un sujet MQTT ;
- une charge utile ;
- des métadonnées.

Ils permettent de conserver une séparation claire entre le domaine métier et le protocole MQTT.

---

# Runtime MQTT

Le runtime MQTT constitue la passerelle entre Shikamaru et son environnement.

Architecture :

```text
MQTT Broker

↓

Transport

↓

MQTT Client

↓

Subscriber

↓

Dispatcher

↓

Application

↓

Publisher

↓

MQTT Client

↓

Broker
```

Le reste du framework ignore complètement le protocole MQTT.

---

# MQTT Client

Le client MQTT est responsable de :

- connexion ;
- déconnexion ;
- reconnexion automatique ;
- publication ;
- souscription.

Il ne contient aucune logique métier.

---

# Publisher

Le Publisher transforme les événements internes en messages MQTT.

Responsabilités :

- sérialisation ;
- publication ;
- gestion des erreurs.

Il ne décide jamais quels événements doivent être publiés.

Cette décision appartient aux couches supérieures.

---

# Subscriber

Le Subscriber reçoit les messages MQTT.

Il :

- désérialise les messages ;
- valide leur contenu ;
- crée les commandes appropriées ;
- les transmet au Dispatcher.

Le Subscriber ne modifie jamais directement l'état du système.

---

# Transport

Le Transport encapsule la bibliothèque MQTT utilisée.

Objectifs :

- faciliter les tests ;
- remplacer facilement l'implémentation ;
- éviter toute dépendance forte.

Le reste du framework dépend uniquement de son interface.

---

# Gestion des plugins

Les plugins représentent les fonctionnalités métier.

Le noyau n'a aucune connaissance de leur implémentation.

```text
Plugin

↓

Initialize()

↓

Run()

↓

Stop()
```

Chaque plugin est indépendant.

---

# Cycle de vie des plugins

Chaque plugin suit le même cycle de vie que l'application.

```text
CREATED

↓

INITIALIZING

↓

READY

↓

RUNNING

↓

STOPPING

↓

STOPPED
```

En cas d'erreur :

```text
RUNNING

↓

ERROR
```

Cette homogénéité simplifie la supervision.

---

# Chargement dynamique

Les plugins sont chargés dynamiquement.

Le gestionnaire de plugins est responsable :

- de leur découverte ;
- de leur création ;
- de leur initialisation ;
- de leur arrêt.

Le noyau ne référence jamais directement un plugin particulier.

---

# Communication des plugins

Les plugins disposent de plusieurs moyens de communication.

Ils peuvent :

- publier des événements ;
- écouter des événements ;
- envoyer des commandes ;
- utiliser les services injectés.

Ils ne doivent jamais communiquer directement entre eux.

---

# Services exposés

Le noyau met plusieurs services à disposition des plugins.

Exemples :

```text
Logger

Dispatcher

MQTT Client

Scheduler

Health Monitor

Recovery Engine
```

Les plugins restent ainsi indépendants des implémentations concrètes.

---

# Injection de dépendances

Toutes les dépendances importantes sont injectées.

Cette approche permet :

- des tests simples ;
- des mocks ;
- le remplacement d'implémentations ;
- un faible couplage.

Exemple conceptuel :

```python
class Plugin:

    def __init__(
        self,
        dispatcher,
        logger,
        mqtt,
        scheduler,
    ):
        ...
```

Le plugin ne crée jamais lui-même ses dépendances.

---

# Principes SOLID

L'architecture du noyau applique les principes SOLID.

## Single Responsibility

Chaque composant possède une responsabilité unique.

Exemples :

- Dispatcher → distribuer.
- Publisher → publier.
- Health Monitor → superviser.
- Recovery Engine → orchestrer.

---

## Open / Closed

Le framework est ouvert à l'extension.

Les nouveaux plugins ne nécessitent pas de modifier le noyau.

---

## Liskov

Toutes les implémentations respectent leurs interfaces.

Les Protocols permettent de garantir cette substituabilité.

---

## Interface Segregation

Les interfaces sont volontairement petites.

Chaque composant ne dépend que des méthodes dont il a réellement besoin.

---

## Dependency Inversion

Les dépendances concrètes sont remplacées par des Protocols ou des interfaces.

Le noyau ne dépend jamais directement d'une implémentation particulière.

---

# Architecture de supervision

Le Sprint 4 introduit une nouvelle couche d'architecture dédiée à la supervision et à la résilience.

Cette couche est totalement indépendante du runtime MQTT et des plugins.

Son objectif est de permettre au noyau de :

- surveiller son propre fonctionnement ;
- détecter les anomalies ;
- tenter des récupérations automatiques ;
- continuer à fonctionner en mode dégradé lorsque cela est possible.

L'architecture est volontairement découpée en deux sous-systèmes indépendants :

- **Health**
- **Recovery**

```text
Application
      │
      ▼
Health Monitor
      │
      ▼
Health Result
      │
      ▼
Recovery Engine
      │
      ▼
Recovery Policy
      │
      ▼
Recovery Strategy
      │
      ▼
Recovery Action
```

Cette séparation constitue l'une des décisions majeures de l'architecture de Shikamaru.

---

# Package Health

Le package `health` est responsable de l'observation.

Il ne modifie jamais le système.

Il fournit uniquement une vision de son état.

Organisation :

```text
health/

heartbeat.py

monitor.py

watchdog.py
```

---

# Health Monitor

Le `HealthMonitor` est le point central de la supervision.

Responsabilités :

- enregistrer les contrôles de santé ;
- exécuter les contrôles ;
- agréger les résultats ;
- calculer l'état global ;
- fournir les informations nécessaires au Recovery Engine.

Il ne réalise aucune récupération.

---

## Agrégation

Le Health Monitor applique les règles suivantes.

```text
Tous HEALTHY

↓

HEALTHY
```

```text
Au moins un DEGRADED

↓

DEGRADED
```

```text
Au moins un UNHEALTHY

↓

UNHEALTHY
```

```text
Aucun contrôle

↓

UNKNOWN
```

Cette logique est volontairement simple.

---

# Health Checks

Les Health Checks représentent les contrôles élémentaires.

Exemples futurs :

- connexion MQTT ;
- plugin actif ;
- mémoire disponible ;
- CPU ;
- disque ;
- disponibilité d'un service.

Chaque Health Check est indépendant.

---

# Heartbeat

Un Heartbeat représente une preuve récente d'activité.

Exemple :

```text
plugin.dns

↓

Heartbeat
```

Le Heartbeat contient :

- la source ;
- l'instant d'émission ;
- des métadonnées éventuelles.

Il est volontairement très léger.

---

# Watchdog

Le Watchdog surveille un Heartbeat.

Principe :

```text
Heartbeat reçu

↓

HEALTHY
```

```text
Heartbeat ancien

↓

DEGRADED
```

```text
Heartbeat expiré

↓

UNHEALTHY
```

Le Watchdog ne déclenche jamais lui-même une récupération.

---

# Surveillance temporelle

Chaque Watchdog possède :

- une source ;
- un délai de dégradation ;
- un délai critique.

Exemple :

```text
Heartbeat

↓

10 s

↓

DEGRADED

↓

30 s

↓

UNHEALTHY
```

Les délais sont entièrement configurables.

---

# Architecture Recovery

Le package `recovery` constitue le second pilier de la résilience.

Organisation :

```text
recovery/

action.py

engine.py

policy.py

result.py

strategy.py
```

Contrairement au package `health`, il est responsable des actions.

---

# Recovery Engine

Le `RecoveryEngine` orchestre les opérations de récupération.

Il reçoit les résultats du Health Monitor.

```text
Health Result

↓

Recovery Engine
```

Le moteur :

- sélectionne une stratégie ;
- empêche les récupérations concurrentes ;
- conserve un historique ;
- exécute les actions.

Il ne contient aucune logique métier.

---

# Recovery Strategy

Une stratégie décrit **comment récupérer une anomalie**.

Exemples :

```text
DNSRecoveryStrategy

DHCPRecoveryStrategy

MQTTRecoveryStrategy

PluginRecoveryStrategy
```

Chaque stratégie est indépendante.

Elle peut être remplacée sans modifier le moteur.

---

# Recovery Policy

La Recovery Policy décide :

- quelles actions effectuer ;
- dans quel ordre ;
- combien de tentatives réaliser ;
- quand abandonner.

Exemple :

```text
Restart

↓

Reload

↓

Disable

↓

Abandon
```

Les politiques sont entièrement configurables.

---

# Recovery History

Chaque récupération possède un historique.

Il mémorise notamment :

- le nombre de tentatives ;
- la dernière action ;
- le dernier résultat ;
- les résultats précédents.

Cette information est utilisée par les Policies.

---

# Recovery Action

Une Action représente une opération élémentaire.

Exemples :

```text
Restart Plugin

Reconnect MQTT

Reload Configuration

Disable Plugin
```

Une Action ne prend aucune décision.

Elle exécute simplement l'opération demandée.

---

# Recovery Result

Chaque tentative retourne un objet `RecoveryResult`.

Il contient :

- succès ou échec ;
- action exécutée ;
- source concernée ;
- message ;
- informations complémentaires.

Le moteur conserve un historique de ces résultats.

---

# Prévention des récupérations concurrentes

Le Recovery Engine garantit qu'une seule récupération peut être exécutée simultanément pour une même source.

Exemple :

```text
plugin.dns

↓

Recovery en cours

↓

Nouvelle demande

↓

Ignorée
```

Cette règle évite :

- les redémarrages multiples ;
- les états incohérents ;
- les courses critiques.

---

# Mode dégradé

Le noyau peut continuer à fonctionner malgré certaines défaillances.

```text
HEALTHY

↓

DEGRADED

↓

UNHEALTHY
```

Le mode dégradé permet :

- de maintenir les services disponibles ;
- d'isoler les composants défaillants ;
- de poursuivre les tentatives de récupération.

Le retour à l'état nominal est automatique lorsque les contrôles redeviennent positifs.

---

# Coopération entre Health et Recovery

Les deux packages collaborent sans dépendance forte.

```text
Health Monitor

↓

Health Result

↓

Recovery Engine

↓

Recovery Policy

↓

Recovery Strategy

↓

Recovery Action
```

Cette architecture garantit une séparation claire entre :

- **l'observation** ;
- **la décision** ;
- **l'exécution**.

Elle constitue aujourd'hui l'un des principaux points forts du noyau Shikamaru.

---

# Organisation des tests

La qualité du noyau repose sur une politique de tests unitaires systématiques.

Chaque composant du framework possède son propre module de tests.

Organisation :

```text
tests/

test_action.py
test_application.py
test_command.py
test_configuration.py
test_dispatcher.py
test_engine.py
test_event.py
test_events.py
test_heartbeat.py
test_lifecycle.py
test_messages.py
test_monitor.py
test_mqtt_client.py
test_plugins.py
test_policy.py
test_publisher.py
test_reconnect.py
test_result.py
test_scheduler.py
test_services.py
test_strategy.py
test_subscriber.py
test_transport.py
test_watchdog.py
```

Les tests sont organisés selon les mêmes responsabilités que les packages du framework.

Cette symétrie facilite la maintenance et la compréhension du projet.

---

# Qualité du code

Le projet applique plusieurs règles de qualité.

## Typage

Le typage statique est utilisé sur l'ensemble du noyau.

Objectifs :

- améliorer la lisibilité ;
- détecter les erreurs précocement ;
- faciliter le refactoring.

---

## Dataclasses

Les objets métiers utilisent principalement les `dataclasses`.

Exemples :

- Event
- Message
- Heartbeat
- HealthResult
- RecoveryResult

Les objets sont immuables dès que cela est possible.

---

## Protocols

Les interfaces reposent principalement sur `typing.Protocol`.

Exemples :

- HealthCheck
- RecoveryAction
- RecoveryStrategy
- RecoveryPolicy

Cette approche évite une hiérarchie de classes trop complexe.

---

## Injection de dépendances

Les composants ne créent jamais directement leurs dépendances.

Toutes les dépendances importantes sont injectées lors de leur création.

Cette règle garantit :

- une excellente testabilité ;
- un faible couplage ;
- un remplacement facile des implémentations.

---

# Performances

Le noyau privilégie la simplicité et la robustesse.

Les optimisations ne sont réalisées que lorsqu'elles sont justifiées.

À ce jour :

- aucune allocation complexe inutile ;
- structures de données simples ;
- faible profondeur d'appel ;
- composants faiblement couplés.

Le framework est conçu pour supporter plusieurs dizaines de plugins sans modification de son architecture.

---

# Gestion des erreurs

Les erreurs sont traitées à plusieurs niveaux.

## Erreurs applicatives

Les exceptions métier sont propagées jusqu'au Dispatcher ou à l'Application.

Les composants évitent autant que possible de masquer les erreurs.

---

## Erreurs de supervision

Les anomalies détectées par le Health Monitor produisent des `HealthResult`.

Aucune récupération n'est réalisée à ce niveau.

---

## Erreurs de récupération

Le Recovery Engine enregistre toutes les tentatives.

Chaque récupération produit un `RecoveryResult`.

Ces informations pourront être utilisées pour :

- les statistiques ;
- les métriques ;
- l'interface Web ;
- Home Assistant.

---

# Journalisation

Le noyau centralise la journalisation.

Objectifs :

- faciliter le diagnostic ;
- tracer les événements importants ;
- conserver une cohérence entre les composants.

Chaque composant reçoit un logger injecté.

Le framework ne dépend pas d'une implémentation particulière.

---

# Configuration

Toute la configuration est regroupée dans un seul package.

```text
configuration/
```

Le modèle repose sur des objets fortement typés.

Les paramètres sont validés au démarrage.

En cas d'erreur de configuration, l'application refuse de démarrer.

Cette approche garantit un comportement déterministe.

---

# Évolutivité

L'architecture actuelle permet d'ajouter facilement :

- de nouveaux plugins ;
- de nouveaux Health Checks ;
- de nouveaux Watchdogs ;
- de nouvelles Recovery Policies ;
- de nouvelles Recovery Strategies ;
- de nouvelles Recovery Actions.

Ces ajouts ne nécessitent pas de modifier les composants existants.

---

# Architecture cible

À moyen terme, le noyau conservera la même organisation générale.

```text
                  Application
                        │
                        ▼
                  Event Dispatcher
                        │
                        ▼
                     Event Bus
                        │
    ┌───────────────────┼───────────────────┐
    ▼                   ▼                   ▼
Configuration       MQTT Runtime        Scheduler
                        │
                        ▼
                     Plugins
                        │
                        ▼
                 Health Monitor
                        │
                        ▼
                   Watchdogs
                        │
                        ▼
                 Recovery Engine
                        │
                        ▼
                 Recovery Policies
                        │
                        ▼
                Recovery Strategies
                        │
                        ▼
                 Recovery Actions
```

Les futures évolutions enrichiront les fonctionnalités sans remettre en cause cette architecture.

---

# Compatibilité

Le noyau est conçu pour rester indépendant :

- du système d'exploitation ;
- du broker MQTT ;
- des plugins ;
- de Home Assistant.

Cette indépendance facilite :

- les tests ;
- les évolutions ;
- la portabilité.

---

# Dette technique

À l'issue du Sprint 4, la dette technique est volontairement limitée.

Quelques évolutions sont déjà identifiées :

- extraire `HealthStatus`, `HealthResult` et `HealthCheck` de `monitor.py` vers des modules dédiés (`status.py`, `result.py`, `check.py`) lorsque l'API sera totalement stabilisée ;
- introduire un `RecoveryContext` pour transmettre les dépendances aux `RecoveryAction` sans couplage supplémentaire ;
- créer un `PolicyRegistry` afin de centraliser l'enregistrement et la sélection des politiques de récupération.

Ces évolutions sont considérées comme des améliorations de conception et non comme des anomalies.

---

# État de l'architecture

À la fin du Sprint 4 :

- Architecture entièrement événementielle.
- Runtime MQTT complet.
- Supervision interne opérationnelle.
- Mécanismes de résilience implémentés.
- Packages fortement découplés.
- Injection de dépendances généralisée.
- Documentation synchronisée avec le code.
- ADR alignées avec l'implémentation.
- 204 tests unitaires validés.
- Ruff conforme.

Le noyau **Shikamaru** constitue désormais une base solide pour développer les futurs plugins d'infrastructure.

---

# Conclusion

Le Sprint 4 marque une étape majeure dans la maturité d'Ohanna-Agent.

Jusqu'au Sprint 3, Shikamaru était principalement un **framework événementiel** capable de communiquer via MQTT.

Avec le Sprint 4, il devient un **framework d'agents résilients**, capable :

- d'observer son propre état ;
- de détecter les défaillances ;
- de raisonner sur les actions à entreprendre ;
- d'exécuter des stratégies de récupération ;
- de continuer à fonctionner en mode dégradé lorsque cela est nécessaire.

Cette évolution repose sur une séparation stricte entre :

- l'observation (`health`) ;
- la décision (`policy` / `strategy`) ;
- l'orchestration (`engine`) ;
- l'exécution (`action`).

Cette architecture, validée par les ADR-0015 à ADR-0019, constitue désormais le socle technique sur lequel seront développés les plugins d'infrastructure des prochains Sprints.

Le noyau est prêt à entrer dans une nouvelle phase du projet : **le développement des services métier**.
# Architecture du cœur d'Ohanna-Agent

Version : **0.8.0**

Dernière mise à jour : **08 juillet 2026**

---

# 1. Objectif

Ce document décrit l'architecture interne du cœur (**Core**) d'Ohanna-Agent.

Il constitue la référence technique du projet et explique :

- les responsabilités des principaux composants ;
- leurs interactions ;
- les décisions d'architecture (ADR) ;
- les principes de conception retenus ;
- les points d'extension prévus pour les futurs sprints.

L'objectif est de garantir une architecture stable, modulaire et évolutive.

---

# 2. Vision

Ohanna-Agent est un framework Python permettant de construire des agents autonomes, pilotés par événements et composés de composants faiblement couplés.

Le framework ne cherche pas à fournir un agent unique, mais une infrastructure sur laquelle différents agents pourront être développés.

Chaque composant possède une responsabilité clairement définie et peut évoluer indépendamment des autres.

---

# 3. Principes d'architecture

Le développement du cœur repose sur plusieurs principes.

## Simplicité

Chaque composant doit être simple à comprendre et à maintenir.

Les abstractions ne sont introduites que lorsqu'elles répondent à un besoin réel.

---

## Responsabilité unique

Chaque classe possède une responsabilité clairement identifiée.

Exemples :

- `CommandDispatcher` route les commandes.
- `Scheduler` planifie les tâches.
- `MemoryManager` orchestre la mémoire.
- `MemoryStorage` gère la persistance.
- `MemorySerializer` convertit les objets mémoire.

---

## Faible couplage

Les composants communiquent principalement via :

- les événements ;
- les interfaces publiques ;
- l'injection de dépendances.

Ils ne doivent pas dépendre directement de l'implémentation interne des autres composants.

---

## Forte cohésion

Toutes les responsabilités liées à un même domaine sont regroupées dans un package dédié.

Exemple :

```text
memory/
```

contient uniquement les composants liés à la mémoire.

---

## Testabilité

Chaque composant doit pouvoir être testé isolément.

Les dépendances sont injectables afin de faciliter les tests unitaires.

L'objectif est de privilégier les tests rapides et déterministes.

---

## Architecture incrémentale

Le framework évolue par petits sprints.

Chaque sprint :

- introduit une nouvelle fonctionnalité ;
- met à jour les ADR ;
- enrichit la documentation ;
- ajoute les tests associés.

---

# 4. Vue d'ensemble

L'architecture actuelle est organisée autour d'un noyau central.

```text
                    Application
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 CommandDispatcher    Scheduler      PluginManager
        │
        ▼
     EventBus
        │
        ▼
 ServiceRegistry
        │
        ▼
  MemoryManager
```

Chaque composant est indépendant.

L'application agit comme un point d'assemblage.

---

# 5. Architecture des packages

Le projet est organisé en packages spécialisés.

```text
application.py

core/
├── dispatcher/
├── events/
├── plugins/
└── services/

memory/
├── memory_entry.py
├── memory_manager.py
├── memory_scope.py
├── memory_serializer.py
├── memory_statistics.py
├── memory_storage.py
├── persistent_memory.py
├── runtime_memory.py
└── session_memory.py

scheduler/

tests/

docs/
├── adr/
└── architecture/
```

Cette organisation facilite :

- la maintenance ;
- la réutilisation ;
- les tests ;
- l'évolution du framework.

---

# 6. Le rôle de l'Application

La classe `Application` constitue le point d'entrée du framework.

Elle est responsable de :

- créer les composants principaux ;
- assembler les dépendances ;
- enregistrer les services cœur ;
- démarrer et arrêter le runtime.

Elle ne contient aucune logique métier.

Son unique responsabilité est l'assemblage des composants.

---

# 7. Les composants du cœur

À la fin du Sprint 7, le cœur d'Ohanna-Agent est constitué des composants suivants.

| Composant | Responsabilité |
|-----------|----------------|
| Application | Assemblage des composants |
| ServiceRegistry | Registre des services |
| EventBus | Communication par événements |
| CommandDispatcher | Routage des commandes |
| Scheduler | Exécution planifiée |
| PluginManager | Gestion des plugins |
| MemoryManager | Gestion unifiée de la mémoire |

Chaque composant est développé indépendamment et possède ses propres tests unitaires.

---

# 8. La mémoire

Le Sprint 7 introduit une nouvelle brique fondamentale : la mémoire.

L'objectif est de fournir un contexte partagé entre les différents composants du framework.

L'architecture retenue est la suivante :

```text
                 MemoryManager
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
RuntimeMemory   SessionMemory   PersistentMemory
                                        │
                                        ▼
                                 MemoryStorage
                                        │
                                        ▼
                                MemorySerializer
```

Cette architecture respecte les principes suivants :

- séparation des responsabilités ;
- faible couplage ;
- forte testabilité ;
- extensibilité ;
- injection de dépendances.

Les composants mémoire sont totalement indépendants du Scheduler, du Dispatcher et du système de plugins.

Ils pourront évoluer sans impact sur le reste du framework.

---

# 9. ServiceRegistry

Le `ServiceRegistry` constitue le conteneur de services du framework.

Il permet de partager les composants principaux sans créer de dépendances directes entre eux.

## Responsabilités

- Enregistrer les services cœur
- Fournir un point d'accès unique
- Faciliter l'injection de dépendances
- Réduire le couplage entre composants

Le registre ne contient aucune logique métier.

---

# 10. EventBus

Le `EventBus` implémente le modèle **Publish / Subscribe**.

Les composants peuvent publier des événements sans connaître leurs consommateurs.

## Responsabilités

- Publication d'événements
- Souscription d'écouteurs
- Diffusion interne
- Découplage des composants

Le bus d'événements constitue le principal moyen de communication interne du framework.

---

# 11. CommandDispatcher

Le `CommandDispatcher` est responsable du routage des commandes.

Une commande représente une intention métier.

Le dispatcher recherche le gestionnaire approprié et déclenche son exécution.

## Responsabilités

- Réception des commandes
- Validation
- Routage
- Exécution
- Gestion des erreurs

Le dispatcher ne contient aucune logique métier.

---

# 12. Scheduler

Le `Scheduler` exécute des tâches planifiées.

Il constitue le moteur d'exécution périodique du framework.

## Architecture

```text
Scheduler
      │
      ▼
DispatcherTaskExecutor
      │
      ▼
CommandDispatcher
```

Cette architecture garantit que toutes les commandes utilisent le même point d'entrée.

## Responsabilités

- Gestion des tâches
- Planification
- Déclenchement
- Exécution
- Statistiques

Le Scheduler est totalement indépendant des plugins et de la mémoire.

---

# 13. PluginManager

Le `PluginManager` permet d'étendre Ohanna-Agent sans modifier son cœur.

Les plugins utilisent les services publics exposés par le framework.

## Responsabilités

- Chargement
- Initialisation
- Arrêt
- Gestion du cycle de vie
- Isolation des extensions

L'objectif est de conserver un cœur minimal tout en permettant des extensions puissantes.

---

# 14. MemoryManager

Le Sprint 7 introduit le sous-système mémoire.

Le `MemoryManager` devient le point d'entrée unique de toute manipulation mémoire.

Les autres composants ne connaissent jamais les implémentations concrètes.

## Architecture

```text
MemoryManager
      │
 ┌────┼──────────────┐
 ▼    ▼              ▼
Runtime Session Persistent
```

Le manager sélectionne automatiquement l'implémentation appropriée selon le `MemoryScope`.

---

# 15. RuntimeMemory

La mémoire runtime est entièrement volatile.

Elle disparaît à l'arrêt de l'application.

## Cas d'utilisation

- Variables temporaires
- État courant
- Résultats intermédiaires
- Cache local

Aucune persistance n'est réalisée.

---

# 16. SessionMemory

La mémoire de session conserve les informations nécessaires pendant toute la durée de vie de l'application.

Elle est indépendante de la mémoire runtime.

## Cas d'utilisation

- Dernière commande exécutée
- Contexte courant
- Informations utilisateur
- Variables de session

La mémoire de session n'est pas persistée.

---

# 17. PersistentMemory

La mémoire persistante contient les données devant survivre à un redémarrage.

Elle est indépendante des deux autres scopes.

## Cas d'utilisation

- Préférences
- Configuration dynamique
- État sauvegardé
- Informations durables

Les données persistantes sont enregistrées via `MemoryStorage`.

---

# 18. MemoryStorage

Le composant `MemoryStorage` est responsable de la persistance.

Sa responsabilité est volontairement limitée.

## Responsabilités

- Sauvegarde
- Chargement
- Vérification d'existence
- Suppression du stockage

Il ne connaît pas la structure interne des objets mémoire.

---

# 19. MemorySerializer

Le `MemorySerializer` transforme les objets Python en représentation persistable.

Cette séparation permet de remplacer ultérieurement le format de stockage sans modifier `MemoryStorage`.

Les formats potentiels sont notamment :

- JSON
- YAML
- TOML
- MessagePack
- CBOR
- SQLite

Cette décision prépare l'évolution future du framework.

---

# 20. MemoryStatistics

Le `MemoryManager` expose des statistiques d'utilisation.

Les compteurs actuellement disponibles sont :

- hits
- misses
- sets
- deletes
- clears
- saves
- loads

Ces informations seront utilisées par les futurs composants :

- Health Manager
- Monitoring
- Diagnostics
- Observabilité

Cette instrumentation a été introduite dès le Sprint 7 afin de préparer les évolutions futures sans modifier l'API publique.

---

# 21. Flux d'exécution

L'application agit comme un point d'assemblage des différents composants.

Le flux général d'exécution est le suivant :

```text
Application
      │
      ▼
Initialisation
      │
      ▼
Enregistrement des services
      │
      ▼
Chargement des plugins
      │
      ▼
Démarrage du Scheduler
      │
      ▼
Boucle d'exécution
```

Chaque composant reste indépendant des autres.

---

# 22. Flux d'une commande

Une commande suit toujours le même chemin d'exécution.

```text
Commande
    │
    ▼
CommandDispatcher
    │
    ▼
Handler
    │
    ▼
EventBus
```

Le Scheduler ne traite jamais directement une commande.

Toutes les commandes transitent par le `CommandDispatcher`.

Cette règle garantit un comportement homogène dans tout le framework.

---

# 23. Flux du Scheduler

Le Scheduler n'exécute jamais directement de logique métier.

```text
Scheduler
      │
      ▼
DispatcherTaskExecutor
      │
      ▼
CommandDispatcher
      │
      ▼
Commande
```

Cette architecture évite la duplication de logique.

Le Scheduler devient ainsi un simple orchestrateur.

---

# 24. Flux mémoire

Toutes les opérations mémoire passent systématiquement par le `MemoryManager`.

```text
Application
      │
      ▼
MemoryManager
      │
      ├───────────────┐
      ▼               ▼
RuntimeMemory   SessionMemory
      │
      ▼
PersistentMemory
      │
      ▼
MemoryStorage
      │
      ▼
MemorySerializer
```

Les composants du framework ne manipulent jamais directement une implémentation mémoire.

---

# 25. Dépendances

Le principe retenu est simple :

Les dépendances doivent toujours pointer vers le cœur.

Jamais l'inverse.

```text
Application
│
├── Dispatcher
├── Scheduler
├── EventBus
├── PluginManager
├── MemoryManager
└── ServiceRegistry
```

Les composants communiquent uniquement via leurs interfaces publiques.

---

# 26. Injection de dépendances

Tous les composants principaux sont injectables.

Par exemple :

```python
Application(
    memory=my_memory,
)
```

ou

```python
MemoryManager(
    storage=my_storage,
)
```

Cette approche facilite :

- les tests ;
- les extensions ;
- les futurs plugins.

---

# 27. Découplage

Le framework applique plusieurs règles.

## Les composants ne connaissent pas leurs implémentations

Exemple :

Le `MemoryManager` connaît l'interface de stockage.

Il ne dépend pas du format JSON.

---

## Les composants communiquent via leurs API publiques

Aucun composant ne doit accéder aux attributs privés d'un autre.

Les interactions passent exclusivement par les méthodes publiques.

---

## Les responsabilités sont isolées

Exemple :

```text
MemoryStorage
```

ne réalise aucune sérialisation.

Inversement :

```text
MemorySerializer
```

ne réalise aucun accès disque.

---

# 28. ADR

Toutes les décisions d'architecture importantes sont documentées.

Les ADR constituent la mémoire technique du projet.

Ils permettent :

- d'expliquer les choix ;
- de documenter les alternatives ;
- de conserver l'historique des décisions.

À la fin du Sprint 7, les principales décisions couvrent notamment :

- architecture du cœur ;
- dispatcher ;
- scheduler ;
- plugins ;
- services ;
- mémoire ;
- politique de persistance.

---

# 29. Principes SOLID

Le développement du framework suit les principes SOLID.

## Single Responsibility

Chaque classe possède une responsabilité unique.

---

## Open / Closed

Les composants sont ouverts à l'extension sans nécessiter de modification du cœur.

---

## Liskov Substitution

Les implémentations mémoire sont interchangeables.

---

## Interface Segregation

Les composants exposent uniquement les méthodes nécessaires.

---

## Dependency Inversion

Les composants dépendent d'abstractions et de leurs interfaces publiques.

---

# 30. Tests

La qualité du framework repose sur une stratégie de tests systématiques.

Chaque nouveau composant est accompagné de tests unitaires.

À la fin du Sprint 7 :

- plus de **420 tests automatisés** ;
- exécution en moins d'une demi-seconde ;
- couverture homogène des composants cœur.

Cette stratégie permet un développement incrémental tout en limitant fortement les risques de régression.

---

# 31. Extensibilité

L'architecture d'Ohanna-Agent a été conçue pour évoluer progressivement sans remettre en cause les composants existants.

Chaque nouveau sprint doit enrichir le framework par composition plutôt que par modification du cœur.

Les principaux points d'extension sont :

- nouveaux plugins ;
- nouveaux handlers de commandes ;
- nouveaux types d'événements ;
- nouveaux backends de stockage ;
- nouveaux sérialiseurs ;
- nouvelles capacités ;
- nouveaux moteurs de raisonnement.

L'objectif est de conserver une API stable malgré l'ajout de nouvelles fonctionnalités.

---

# 32. Évolutions prévues

L'architecture actuelle prépare les prochains sprints.

## Workflows

Le Scheduler et le Dispatcher serviront de base au moteur de workflows.

Architecture cible :

```text
Workflow
     │
     ▼
WorkflowRunner
     │
     ▼
Scheduler
     │
     ▼
CommandDispatcher
```

---

## Observabilité

Les statistiques déjà présentes dans plusieurs composants permettront de construire un système complet de supervision.

Exemples :

- SchedulerStatistics
- MemoryStatistics

Ces informations alimenteront ultérieurement :

- Health Manager
- Diagnostics
- Monitoring
- Dashboard

---

## Mémoire avancée

Le système mémoire pourra évoluer sans modifier son API publique.

Évolutions envisagées :

- TTL
- expiration automatique
- cache
- SQLite
- Redis
- stockage distribué
- chiffrement
- compression

Grâce à la séparation entre `MemoryManager`, `MemoryStorage` et `MemorySerializer`, ces évolutions resteront transparentes pour les autres composants.

---

## Intelligence

Le framework est conçu pour accueillir un moteur de décision.

Les futurs composants pourront notamment inclure :

- Context Engine
- Goal Manager
- Decision Engine
- Rule Engine
- Prompt Manager
- LLM Provider

Ils s'appuieront sur les briques déjà présentes :

- EventBus
- Scheduler
- MemoryManager
- ServiceRegistry

---

# 33. Conventions de développement

Les conventions suivantes sont appliquées dans tout le projet.

## Typage

Toutes les API publiques sont entièrement typées.

---

## Documentation

Chaque module possède :

- une docstring de module ;
- des docstrings de classes ;
- des docstrings de méthodes publiques.

---

## Tests

Chaque fonctionnalité est accompagnée de tests unitaires.

Les nouvelles fonctionnalités ne sont intégrées qu'après validation complète de la suite de tests.

---

## Style

Le projet respecte :

- Ruff
- PEP 8
- annotations de types
- importations explicites

---

## Architecture

Les dépendances doivent toujours respecter le sens suivant :

```text
Application
        │
        ▼
Core Components
        │
        ▼
Infrastructure
```

Jamais l'inverse.

---

# 34. Objectif v1.0.0

La version 1.0.0 sera considérée comme atteinte lorsque les objectifs suivants seront remplis.

## Architecture

- Architecture stabilisée
- API publique figée
- Documentation complète

---

## Fonctionnalités

- Scheduler avancé
- SDK Plugins
- Workflows
- Observabilité
- Raisonnement
- Mémoire avancée

---

## Qualité

- Plus de 1 000 tests automatisés
- Documentation ADR complète
- Couverture homogène
- Refactoring continu

---

# 35. État actuel du projet

À la fin du Sprint 7, Ohanna-Agent dispose :

## Composants

- Application
- ServiceRegistry
- EventBus
- CommandDispatcher
- Scheduler
- PluginManager
- MemoryManager

---

## Mémoire

- RuntimeMemory
- SessionMemory
- PersistentMemory
- MemoryStorage
- MemorySerializer
- MemoryStatistics

---

## Documentation

- ADR
- README
- ROADMAP
- CHANGELOG
- CORE

---

## Qualité

- Plus de **420 tests automatisés**
- Architecture modulaire
- Forte séparation des responsabilités
- Faible couplage
- Forte testabilité
- Injection de dépendances

---

# Conclusion

Ohanna-Agent est désormais structuré autour d'un noyau applicatif stable et modulaire.

Les sept premiers sprints ont permis de construire les fondations du framework :

- architecture ;
- cycle de vie ;
- services cœur ;
- communication par événements ;
- scheduler ;
- plugins ;
- capacités ;
- mémoire.

Les prochains sprints se concentreront principalement sur l'orchestration, le raisonnement et l'intelligence, en s'appuyant sur ces briques déjà éprouvées.

L'objectif reste inchangé :

> construire un framework d'agents autonome, robuste, extensible et durable, dont l'architecture puisse évoluer pendant de nombreuses années sans remettre en cause ses fondations.

---

**Version du document :** v0.8.0

**Sprint :** 7 — Memory

**État :** Validé

**Tests associés :** 422/422 ✔
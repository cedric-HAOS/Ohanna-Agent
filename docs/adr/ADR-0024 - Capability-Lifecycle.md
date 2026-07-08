# ADR-0024 — Capability Lifecycle

- **Statut** : Accepté
- **Date** : 2026-07-08
- **Décideurs** : Équipe Ohanna-Agent
- **Version cible** : v0.4.0

---

# Contexte

L'ADR-0020 introduit les **Capabilities** comme unité fonctionnelle centrale d'Ohanna-Agent.

Les ADR suivants définissent leur gestion, leur découverte et leurs dépendances.

Il reste à définir le cycle de vie d'une Capability afin que toutes les fonctionnalités de l'agent adoptent un comportement homogène.

L'objectif est de permettre au noyau **Shikamaru** d'orchestrer les Capabilities de manière cohérente, quel que soit leur domaine fonctionnel.

---

# Problème

Sans cycle de vie commun :

- chaque Capability définirait ses propres états ;
- les transitions seraient incohérentes ;
- la supervision deviendrait complexe ;
- l'auto-réparation ne pourrait pas fonctionner de manière générique ;
- les API futures devraient gérer plusieurs modèles différents.

Une architecture uniforme nécessite donc un modèle de cycle de vie unique.

---

# Décision

Toutes les Capabilities suivent le même cycle de vie.

Ce cycle est indépendant du plugin qui les implémente.

Le **CapabilityManager** orchestre les transitions, tandis que chaque Capability reste responsable de son comportement interne.

---

# États

Une Capability peut se trouver dans l'un des états suivants :

| État | Description |
|------|-------------|
| `CREATED` | Instance créée mais non enregistrée |
| `REGISTERED` | Enregistrée auprès du CapabilityManager |
| `INITIALIZING` | Initialisation en cours |
| `READY` | Initialisée et prête à démarrer |
| `STARTING` | Démarrage en cours |
| `RUNNING` | Fonctionnelle |
| `DEGRADED` | Fonctionnelle avec limitations |
| `STOPPING` | Arrêt en cours |
| `STOPPED` | Arrêtée proprement |
| `ERROR` | Erreur empêchant le fonctionnement |

Ces états sont communs à toutes les Capabilities.

---

# Diagramme de transitions

```text
            CREATED
                │
                ▼
          REGISTERED
                │
                ▼
         INITIALIZING
                │
                ▼
             READY
                │
                ▼
           STARTING
                │
                ▼
            RUNNING
           ↙        ↘
     DEGRADED      ERROR
           │          │
           └────┬─────┘
                ▼
           STOPPING
                │
                ▼
            STOPPED
```

Toutes les transitions sont contrôlées par le CapabilityManager.

---

# Description des états

## CREATED

La Capability existe en mémoire mais n'est pas encore connue du noyau.

---

## REGISTERED

La Capability est enregistrée dans le registre officiel.

Elle peut désormais être interrogée.

---

## INITIALIZING

Chargement de la configuration.

Initialisation des ressources internes.

Vérification des dépendances locales.

---

## READY

Toutes les conditions sont réunies pour permettre le démarrage.

La Capability attend son activation.

---

## STARTING

Ouverture des connexions.

Création des abonnements.

Initialisation des tâches d'exécution.

---

## RUNNING

La Capability fournit pleinement son service.

Elle peut publier des événements, recevoir des commandes et être supervisée.

---

## DEGRADED

La fonctionnalité reste disponible mais certaines fonctions sont limitées.

Exemples :

- perte d'une dépendance optionnelle ;
- performances réduites ;
- service externe momentanément indisponible.

La Capability reste opérationnelle.

---

## ERROR

Une erreur empêche le fonctionnement normal.

L'auto-réparation peut tenter une récupération.

---

## STOPPING

Libération des ressources.

Fermeture des connexions.

Arrêt des traitements.

---

## STOPPED

La Capability est arrêtée proprement.

Elle peut être redémarrée ultérieurement.

---

# Transitions autorisées

Les transitions sont volontairement limitées afin de garantir la cohérence du système.

Exemples :

```text
READY
    │
    ▼
STARTING
```

autorisé.

```text
RUNNING
    │
    ▼
CREATED
```

interdit.

Le CapabilityManager valide chaque transition.

---

# Dépendances

Une Capability ne peut atteindre l'état `READY` que si toutes ses dépendances obligatoires sont satisfaites.

Une dépendance devenue indisponible peut entraîner :

- le passage à `DEGRADED` ;
- ou le passage à `ERROR`, selon la criticité de la dépendance.

---

# Santé

Le cycle de vie est indépendant de l'état de santé.

Par exemple :

| État | Santé |
|------|--------|
| RUNNING | Healthy |
| RUNNING | Warning |
| RUNNING | Critical |
| DEGRADED | Warning |
| ERROR | Critical |

Cette séparation permet une supervision plus fine.

---

# Auto-réparation

Le module d'auto-réparation agit principalement sur les états :

- `DEGRADED`
- `ERROR`

Il peut notamment :

- relancer une Capability ;
- réinitialiser certaines ressources ;
- attendre le rétablissement d'une dépendance ;
- réévaluer son état.

Le mécanisme est identique pour toutes les Capabilities.

---

# Observabilité

Chaque Capability expose en permanence :

- son état ;
- son état de santé ;
- son horodatage de dernière transition ;
- sa version ;
- son temps d'exécution.

Ces informations pourront être exploitées par :

- l'interface Web ;
- l'API REST ;
- les tableaux de bord ;
- les outils de supervision.

---

# Conséquences

## Avantages

- comportement homogène ;
- supervision simplifiée ;
- transitions prévisibles ;
- orchestration uniforme ;
- intégration facilitée avec l'auto-réparation ;
- préparation des futures interfaces d'administration.

---

## Inconvénients

- certains plugins simples devront implémenter un cycle de vie complet ;
- légère augmentation de la complexité des Capabilities.

---

# Alternatives étudiées

## Cycle de vie propre à chaque plugin

Rejeté.

Cela conduirait à une architecture hétérogène et difficile à superviser.

---

## Réutiliser directement le Lifecycle de l'Application

Rejeté.

Le cycle de vie d'une Capability est plus détaillé et répond à des besoins différents.

---

## Ne gérer que RUNNING et STOPPED

Rejeté.

Cette approche ne permettrait pas de représenter correctement les états intermédiaires ni les situations dégradées.

---

# Conséquences sur l'architecture

Toutes les Capabilities suivent désormais le même modèle d'exécution.

Le CapabilityManager orchestre les transitions.

Le HealthManager supervise leur état de santé.

L'AutoRepairManager peut appliquer des stratégies génériques de récupération.

Cette homogénéité simplifie considérablement l'évolution du noyau **Shikamaru**.

---

# ADR associés

- ADR-0001 — Lifecycle
- ADR-0014 — Auto Repair
- ADR-0020 — Capability Model
- ADR-0021 — Capability Manager
- ADR-0022 — Dependency Resolution
- ADR-0023 — Plugin Discovery

---

# Décision finale

Toutes les **Capabilities** d'Ohanna-Agent suivent un cycle de vie commun, indépendant de leur implémentation.

Le **CapabilityManager** orchestre les transitions d'état, tandis que chaque Capability reste responsable de son comportement interne.

Cette décision garantit un fonctionnement homogène, facilite la supervision, simplifie l'auto-réparation et constitue une base solide pour les futures évolutions de la plateforme.
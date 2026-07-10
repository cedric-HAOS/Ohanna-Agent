# ADR-0028 — Standard d'observation

**Statut** : Accepté

## Contexte

La mission d'Ohanna-Agent est d'observer l'état réel des capacités décrites par l'architecture de référence d'Ohanna-House.

Chaque plugin (DNS, DHCP, MQTT, Internet, WireGuard, sauvegardes, etc.) exécute des vérifications spécifiques et produit des résultats qui lui sont propres.

Sans modèle commun, chaque consommateur de ces résultats (historique, interface Web, MQTT, API, Ohanna-Vision...) devrait connaître le format spécifique de chaque plugin.

Cette approche créerait un fort couplage entre les plugins et les composants consommateurs, rendant le système difficile à maintenir et à faire évoluer.

Il est donc nécessaire de définir un **format d'observation unique**, indépendant des plugins et des mécanismes de transport.

---

# Décision

Toutes les observations produites par Ohanna-Agent seront représentées par une classe unique nommée **Observation**.

Une Observation représente un **fait observé** à un instant donné.

Une Observation ne décrit pas :

- une configuration ;
- une planification ;
- un plugin ;
- un protocole de transport.

Elle décrit uniquement le résultat d'une observation.

Les informations spécifiques à un plugin seront conservées dans un dictionnaire `metadata`.

Ainsi, toutes les observations partageront le même modèle tout en conservant leurs informations spécifiques.

---

# Distinction entre ObservationDefinition et Observation

Afin de lever toute ambiguïté, deux concepts distincts sont définis.

## ObservationDefinition

Une **ObservationDefinition** décrit ce qu'il faut observer.

Elle contient notamment :

- la capacité à observer ;
- le check à exécuter ;
- la fréquence d'exécution ;
- le délai maximal d'exécution ;
- le nombre de tentatives.

Elle est utilisée par le Scheduler afin de déterminer **quoi observer** et **quand l'observer**.

Elle ne contient jamais le résultat d'une observation.

---

## Observation

Une **Observation** représente le résultat produit par une ObservationDefinition.

Elle contient notamment :

- le nœud concerné ;
- le service concerné ;
- la capacité observée ;
- le statut obtenu ;
- le temps de réponse ;
- le message produit ;
- la date de l'observation.

Une Observation est immuable.

Elle constitue le contrat officiel d'échange de l'écosystème Ohanna.

---

# Cycle de vie

Le cycle complet d'une observation est le suivant :

```text
Infrastructure
        │
        ▼
Node
        │
        ▼
Service
        │
        ▼
Capability
        │
        ▼
ObservationDefinition
        │
        ▼
Scheduler
        │
        ▼
Check
        │
        ▼
Observation
        │
        ▼
ObservationManager
        │
        ├── Historique
        ├── Export JSON
        ├── Publication MQTT
        ├── API HTTP
        └── Ohanna-Vision
```

---

# Structure d'une Observation

Une Observation devra contenir les informations suivantes.

| Champ | Description |
|--------|-------------|
| `id` | Identifiant unique de l'observation |
| `timestamp` | Date et heure UTC de l'observation |
| `source` | Plugin ayant produit l'observation |
| `node` | Nœud observé |
| `service` | Service observé |
| `capability` | Capacité évaluée |
| `status` | État normalisé de la capacité |
| `success` | Résultat booléen du check |
| `latency_ms` | Temps de réponse en millisecondes |
| `message` | Message synthétique |
| `metadata` | Informations spécifiques au plugin |

---

# Statuts normalisés

Toutes les observations utiliseront le même ensemble de statuts.

| Statut | Signification |
|---------|---------------|
| `UNKNOWN` | Aucun résultat disponible |
| `HEALTHY` | Fonctionnement normal |
| `DEGRADED` | Fonctionnement partiel ou dégradé |
| `UNHEALTHY` | Capacité indisponible |

Ces statuts sont indépendants du plugin ayant produit l'observation.

Ils permettent à Ohanna-Vision d'afficher l'état d'une capacité sans connaître son implémentation.

---

# Métadonnées

Les informations propres à chaque plugin seront stockées dans le champ `metadata`.

## Exemple — DNS

```text
hostname = example.com
server = 192.168.1.54
resolved_address = 93.184.216.34
```

## Exemple — DHCP

```text
lease_count = 28
pool_usage = 43 %
```

## Exemple — MQTT

```text
broker = mqtt.home
connected_clients = 12
```

Le contenu de `metadata` reste libre.

Il ne fait pas partie du contrat commun.

---

# Consommateurs

Une Observation peut être utilisée simultanément par plusieurs composants.

Par exemple :

- historique local ;
- export JSON ;
- publication MQTT ;
- API REST ;
- Ohanna-Vision ;
- outils de diagnostic.

Aucun de ces composants ne dépend du plugin ayant produit l'observation.

Tous manipulent exactement le même modèle.

---

# Découplage de l'écosystème

Le modèle Observation constitue le contrat d'échange entre les différents projets Ohanna.

```text
                Ohanna-House
             (Architecture cible)
                     │
                     ▼
               Ohanna-Agent
          (Production d'observations)
                     │
             Observation
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Historique     MQTT/API   Ohanna-Vision
```

Ohanna-Agent ne connaît pas Ohanna-Vision.

Ohanna-Vision ne connaît pas les plugins d'Ohanna-Agent.

Les deux projets échangent uniquement des objets Observation.

---

# Conséquences

## Avantages

- Contrat unique pour tous les plugins.
- Séparation claire entre configuration et résultat.
- Découplage complet entre les plugins et les consommateurs.
- Simplification des futurs connecteurs.
- Standard commun à l'ensemble de l'écosystème Ohanna.
- Évolutivité facilitée pour les futurs plugins.
- Réutilisation du même modèle pour MQTT, HTTP, JSON et Ohanna-Vision.

## Inconvénients

- Chaque plugin doit convertir son résultat spécifique en Observation.
- Certaines informations spécifiques restent encapsulées dans `metadata`.

---

# Motivation architecturale

L'architecture d'Ohanna repose sur une séparation stricte des responsabilités.

- **Ohanna-House** décrit l'infrastructure de référence.
- **Ohanna-Agent** observe son état réel.
- **Ohanna-Vision** présente ces observations à l'utilisateur.

L'Observation constitue le langage commun entre ces projets.

Elle permet à chaque composant d'évoluer indépendamment tout en partageant un modèle d'information stable.

Cette décision fait de l'Observation la pierre angulaire des échanges au sein de l'écosystème Ohanna.
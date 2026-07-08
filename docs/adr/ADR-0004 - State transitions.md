# ADR-0004 — State Transitions

**Statut :** Accepté
**Version :** 1.0
**Date :** 2026-07-07
**Décideurs :** Cédric Harnois, ChatGPT

---

# Objectif

Définir la manière dont les changements d'état sont réalisés au sein de Shikamaru.

Cette ADR s'applique au cycle de vie de l'application et constitue une règle générale pouvant être réutilisée par les autres composants.

---

# Contexte

Le cycle de vie de Shikamaru est défini par l'ADR-0001.

Une question reste cependant ouverte :

Comment l'application passe-t-elle d'un état à un autre ?

Deux approches sont possibles :

**Approche 1**

```python
lifecycle.state = AgentState.RUNNING
```

**Approche 2**

```python
lifecycle.transition_to(AgentState.RUNNING)
```

---

# Décision

Toutes les transitions d'état doivent être réalisées par une méthode dédiée.

Exemple :

```python
lifecycle.transition_to(AgentState.RUNNING)
```

La modification directe de l'état est interdite en dehors de la classe responsable de cet état.

---

# Raisons

Une transition représente une action métier.

Elle peut, aujourd'hui ou demain :

- vérifier qu'une transition est autorisée ;
- produire une entrée dans les journaux ;
- publier un événement MQTT ;
- notifier un composant de supervision ;
- déclencher des hooks ;
- mesurer la durée passée dans un état ;
- alimenter des métriques.

Toutes ces actions seraient impossibles avec une simple affectation.

---

# Principe

Le changement d'état n'est pas une donnée.

Le changement d'état est un événement.

---

# Exemple

✔ Correct

```python
lifecycle.transition_to(AgentState.READY)
```

✘ Interdit

```python
lifecycle.state = AgentState.READY
```

---

# Visibilité

L'état courant reste consultable.

Exemple :

```python
print(lifecycle.state)
```

ou

```python
if lifecycle.state == AgentState.RUNNING:
    ...
```

En revanche, seule la classe `Lifecycle` est autorisée à modifier cet état.

---

# Validation des transitions

La méthode `transition_to()` est responsable de vérifier que la transition demandée est cohérente.

Exemple :

✔

```text
CREATED
    ↓
INITIALIZING
```

✔

```text
READY
    ↓
RUNNING
```

✘

```text
RUNNING
    ↓
CREATED
```

Une transition invalide doit provoquer une erreur explicite.

---

# Règles d'architecture

Une transition :

- est atomique ;
- est explicite ;
- est traçable ;
- est validée.

Aucune transition implicite n'est autorisée.

---

# Conséquences

Cette approche permet :

- une meilleure lisibilité du code ;
- une validation centralisée ;
- une journalisation des changements d'état ;
- une supervision facilitée ;
- une future publication d'événements sans modifier les composants existants.

---

# Alternatives étudiées

## Affectation directe

```python
lifecycle.state = ...
```

Simple mais trop limitée.

Rejetée.

---

## Méthodes spécialisées

```python
set_ready()

set_running()

set_stopped()
```

Lisible pour un petit nombre d'états.

Devient difficile à maintenir lorsque le nombre d'états augmente.

Non retenue.

---

## Méthode générique

```python
transition_to(...)
```

Une seule API.

Toutes les règles sont centralisées.

Approche retenue.

---

# Évolutions possibles

La méthode `transition_to()` pourra ultérieurement :

- enregistrer un historique des transitions ;
- calculer le temps passé dans chaque état ;
- publier des événements MQTT ;
- notifier les plugins ;
- déclencher des callbacks ;
- alimenter des métriques Prometheus.

Ces évolutions ne modifieront pas l'API publique.

---

# Références

- ADR-0001 — Lifecycle
- ADR-0002 — Application
- ADR-0003 — Composition
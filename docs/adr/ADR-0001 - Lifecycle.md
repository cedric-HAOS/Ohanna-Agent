# ADR-0001 — Lifecycle

**Statut :** Accepté
**Date :** 2026-07-07
**Auteur :** Cédric Harnois, ChatGPT

---

# Objectif

Définir le cycle de vie officiel de l'application **Shikamaru**.

Ce document décrit les différents états de l'agent, leurs transitions ainsi que l'interface publique permettant de piloter son exécution.

Toutes les futures fonctionnalités devront respecter ce cycle de vie.

---

# Contexte

Shikamaru est conçu comme un agent logiciel modulaire.

Afin de garantir un comportement prévisible, chaque composant doit connaître l'état courant de l'application.

Le cycle de vie constitue donc la référence unique de l'état de l'agent.

---

# Décision

Le cycle de vie officiel est le suivant :

```text
CREATED
    │
    ▼
INITIALIZING
    │
    ▼
READY
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

En cas d'erreur fatale :

```text
ANY STATE
    │
    ▼
ERROR
```

---

# États

## CREATED

L'objet `Application` vient d'être créé.

Aucune initialisation n'a encore été effectuée.

---

## INITIALIZING

L'application prépare son environnement :

- lecture de la configuration ;
- initialisation du logger ;
- création des composants ;
- connexion MQTT ;
- chargement des plugins ;
- vérifications de cohérence.

Aucune tâche métier n'est encore exécutée.

---

## READY

Tous les composants sont initialisés.

L'application est prête à démarrer mais la boucle principale n'est pas encore lancée.

---

## RUNNING

L'application exécute sa boucle principale.

Tous les services sont actifs.

---

## STOPPING

Arrêt contrôlé de l'application.

Les ressources sont libérées proprement :

- arrêt des plugins ;
- publication MQTT OFFLINE ;
- fermeture des connexions ;
- sauvegarde éventuelle.

---

## STOPPED

Toutes les ressources ont été libérées.

L'application est totalement arrêtée.

---

## ERROR

Une erreur fatale empêche le fonctionnement normal.

L'application peut décider d'effectuer un arrêt propre avant de quitter.

---

# Interface publique

Le cycle de vie est piloté exclusivement par trois méthodes publiques.

```python
app.initialize()

app.run()

app.stop()
```

## initialize()

Prépare entièrement l'application.

Cette méthode ne démarre jamais la boucle principale.

À son retour, l'application est dans l'état :

```text
READY
```

---

## run()

Démarre la boucle principale.

À partir de cet instant, l'application passe dans l'état :

```text
RUNNING
```

Cette méthode ne retourne normalement jamais.

---

## stop()

Déclenche un arrêt propre de l'application.

Cette méthode place successivement l'application dans les états :

```text
STOPPING
↓
STOPPED
```

---

# Transitions autorisées

```text
CREATED
    │
    ▼
INITIALIZING
    │
    ├─────────────► ERROR
    ▼
READY
    │
    ▼
RUNNING
    │
    ├─────────────► ERROR
    ▼
STOPPING
    │
    ▼
STOPPED
```

Aucune autre transition n'est autorisée.

---

# Publication externe

Le cycle de vie interne est indépendant de l'état publié aux autres applications.

Par exemple :

| État interne | Publication MQTT |
|--------------|------------------|
| CREATED | OFFLINE |
| INITIALIZING | OFFLINE |
| READY | ONLINE |
| RUNNING | ONLINE |
| STOPPING | OFFLINE |
| STOPPED | OFFLINE |
| ERROR | OFFLINE |

Cette séparation permet de faire évoluer le cycle interne sans impacter les systèmes externes.

---

# Règles d'architecture

Le cycle de vie est piloté exclusivement par la classe `Application`.

Les autres composants ne doivent jamais modifier directement l'état de l'application.

Ils peuvent uniquement signaler des erreurs ou des événements à `Application`, qui reste seule responsable des transitions.

---

# Conséquences

Cette architecture permet :

- un comportement prévisible ;
- des tests unitaires plus simples ;
- une supervision facilitée ;
- une meilleure lisibilité du code ;
- une évolution du projet sans remise en cause du cycle de vie.

---

# Évolutions possibles

Des états complémentaires pourront être ajoutés ultérieurement si nécessaire.

Exemples :

- PAUSED
- UPDATING
- DEGRADED
- RECOVERING

Toute modification du cycle de vie devra faire l'objet d'une nouvelle ADR.
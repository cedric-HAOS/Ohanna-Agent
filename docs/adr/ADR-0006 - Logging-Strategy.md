
# ADR-0006 — Stratégie de journalisation

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 07/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

# 1. Objectif

Définir la stratégie de journalisation de Shikamaru afin d'obtenir une architecture simple, robuste et conforme aux bonnes pratiques Python.

---

# 2. Contexte

Lors de la conception du noyau de Shikamaru, une classe `Logger` dédiée a été envisagée.

Au cours de la revue d'architecture, il est apparu que cette classe ne faisait qu'encapsuler les fonctionnalités déjà offertes par le module standard `logging` de Python.

Cette duplication allait à l'encontre de la philosophie du projet.

---

# 3. Problématique

Deux approches étaient possibles.

## Option A — Développer une classe Logger

```
Logger
    ↓
logging.Logger
```

Cette approche ajoute une abstraction supplémentaire mais n'apporte pas de valeur fonctionnelle.

## Option B — Utiliser directement le module `logging`

```
LoggingConfigurator.configure()

        ↓

logging.getLogger(__name__)
```

Cette approche suit les recommandations officielles de Python.

---

# 4. Décision

Shikamaru utilisera exclusivement le module standard `logging`.

Le projet ne développera pas de classe `Logger` personnalisée.

Un composant unique, `LoggingConfigurator`, sera chargé de configurer le système de journalisation au démarrage de l'application.

Les composants récupéreront ensuite leur logger avec :

```python
import logging

logger = logging.getLogger(__name__)
```

---

# 5. Principes

La stratégie retenue repose sur les principes suivants :

- utiliser la bibliothèque standard lorsqu'elle répond déjà au besoin ;
- configurer le système de journalisation une seule fois ;
- ne jamais encapsuler inutilement `logging` ;
- laisser chaque composant obtenir son propre logger ;
- séparer clairement configuration et utilisation.

---

# 6. Architecture retenue

```
Application.initialize()

        │

        ▼

LoggingConfigurator.configure(configuration.logging)

        │

        ▼

logging

        │

        ▼

logging.getLogger(__name__)
```

---

# 7. Responsabilités

## Application

- appelle `LoggingConfigurator.configure()` pendant l'initialisation.

## LoggingConfigurator

- configure le niveau de logs ;
- configure les handlers ;
- configure les formatters.

Il ne produit jamais de messages de journalisation.

## Composants

Chaque composant :

- récupère son logger via `logging.getLogger(__name__)` ;
- produit uniquement des messages de journalisation.

---

# 8. Alternatives étudiées

## Classe Logger

Avantages :

- API homogène.

Inconvénients :

- duplication des fonctionnalités de `logging` ;
- maintenance supplémentaire ;
- abstraction inutile.

Décision : rejetée.

## Bibliothèque externe

Avantages :

- fonctionnalités avancées.

Inconvénients :

- dépendance supplémentaire ;
- inutile au Sprint 1.

Décision : rejetée.

---

# 9. Conséquences

Cette décision apporte :

- une architecture plus simple ;
- une meilleure compatibilité avec l'écosystème Python ;
- moins de code à maintenir ;
- une prise en main plus rapide par un développeur Python.

---

# 10. Évolutions possibles

La stratégie retenue permet d'ajouter ultérieurement :

- rotation des fichiers de logs ;
- journalisation JSON ;
- handlers MQTT ;
- handlers réseau ;
- couleurs dans la console.

Ces évolutions devront toujours s'appuyer sur le module standard `logging`.

---

# 11. Références

- ADR-0002 — Application
- ADR-0003 — Composition
- ADR-0005 — Configuration Model
- Documentation officielle Python — `logging`

---

## Résumé de la décision

**Décision :** Utiliser le module standard `logging` de Python.

**Impact :** ★★★★☆

**Réversibilité :** ★★★★★

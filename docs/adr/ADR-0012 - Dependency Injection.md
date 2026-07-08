# ADR-0012 — Dependency Injection

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Les composants du noyau utilisent plusieurs services communs, tels que le Logger, la Configuration, le Scheduler ou l'Event Bus.

Afin d'éviter que les composants créent eux-mêmes leurs dépendances, un mécanisme d'injection est nécessaire.

---

## Décision

Shikamaru adopte le principe de **Dependency Injection**.

Les dépendances sont fournies par le noyau lors de la création des composants.

Le **Service Registry** constitue la source de référence des services disponibles.

Les composants ne doivent jamais instancier directement leurs dépendances.

---

## Conséquences

### Avantages

- Réduction du couplage.
- Composants plus faciles à tester.
- Dépendances explicites.
- Architecture plus modulaire et évolutive.

### Inconvénients

- Initialisation du noyau légèrement plus complexe.
- Les dépendances doivent être enregistrées avant leur utilisation.

---

## Alternatives étudiées

### Instanciation directe

Chaque composant crée les services dont il a besoin.

**Rejetée** car elle augmente le couplage et réduit la testabilité.

### Variables globales

Les services sont accessibles via des variables globales.

**Rejetée** car elle nuit à la maintenabilité et au contrôle des dépendances.

### Framework externe d'injection

Utilisation d'un conteneur d'injection de dépendances.

**Rejetée** afin de conserver un noyau léger, simple et entièrement maîtrisé.

---

## Conclusion

Les dépendances des composants sont injectées par le noyau à partir du **Service Registry**, garantissant une architecture faiblement couplée et facilement testable.
# ADR-0010 — Plugin Lifecycle

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Les fonctionnalités de Shikamaru sont implémentées sous forme de plugins.

Afin de garantir un comportement homogène, tous les plugins doivent suivre le même cycle de vie, indépendamment de leur fonction.

---

## Décision

Shikamaru définit un cycle de vie unique pour tous les plugins.

Chaque plugin est chargé, initialisé, démarré, arrêté puis déchargé selon une séquence identique pilotée par le noyau.

Le noyau reste l'unique responsable de la gestion du cycle de vie des plugins.

---

## Conséquences

### Avantages

- Comportement uniforme de tous les plugins.
- Simplification du Plugin Manager.
- Chargement et arrêt contrôlés.
- Facilite les tests et le diagnostic.

### Inconvénients

- Tous les plugins doivent respecter le cycle de vie défini.
- L'ajout d'une nouvelle étape du cycle impacte l'ensemble des plugins.

---

## Alternatives étudiées

### Cycle de vie libre

Chaque plugin gère son propre fonctionnement.

**Rejetée** car elle conduit à des comportements hétérogènes.

### Gestion déléguée aux plugins

Les plugins contrôlent eux-mêmes leur démarrage et leur arrêt.

**Rejetée** afin de conserver un contrôle centralisé par le noyau.

---

## Conclusion

Tous les plugins de Shikamaru suivent un cycle de vie unique, piloté par le noyau, garantissant un fonctionnement cohérent et prévisible.
# ADR-0009 — Scheduler

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Shikamaru exécute des tâches périodiques telles que la supervision, la publication MQTT, les contrôles réseau ou les traitements des plugins.

Afin d'éviter que chaque composant implémente sa propre boucle d'exécution, un mécanisme commun de planification est nécessaire.

---

## Décision

Shikamaru adopte un **Scheduler** central chargé de planifier et d'exécuter les tâches du noyau.

Les composants enregistrent leurs tâches auprès du Scheduler sans gérer eux-mêmes leur exécution.

Le Scheduler est responsable du déclenchement des tâches selon leur planification.

---

## Conséquences

### Avantages

- Planification centralisée.
- Réduction de la duplication de code.
- Comportement homogène de tous les services.
- Facilite la supervision et les tests.

### Inconvénients

- Dépendance supplémentaire du noyau.
- Les tâches longues doivent être conçues pour ne pas bloquer le Scheduler.

---

## Alternatives étudiées

### Boucle propre à chaque composant

Chaque service gère son propre cycle d'exécution.

**Rejetée** car elle multiplie les boucles et complique leur coordination.

### Planificateur externe

Utilisation d'un ordonnanceur du système d'exploitation.

**Rejetée** car les tâches concernent principalement le fonctionnement interne de Shikamaru.

---

## Conclusion

Le **Scheduler** devient le composant unique responsable de la planification des tâches du noyau.
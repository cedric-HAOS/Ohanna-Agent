# ADR-0007 — Service Registry

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Le noyau **Shikamaru** est composé de plusieurs services internes (configuration, journalisation, supervision, MQTT, scheduler, etc.).

Afin de limiter le couplage entre les composants et de préparer l'évolution vers une architecture modulaire, il est nécessaire de disposer d'un mécanisme centralisé permettant de partager ces services.

---

## Décision

Shikamaru adopte un **Service Registry** chargé d'enregistrer et de fournir les services du noyau.

Les services sont créés par l'application puis enregistrés dans le registre au démarrage.

Chaque service est identifié par son type et ne peut être enregistré qu'une seule fois.

Le registre fournit les opérations suivantes :

- `register()`
- `get()`
- `has()`
- `unregister()`

La demande d'un service inexistant ou l'enregistrement d'un service déjà présent provoque une exception explicite.

---

## Conséquences

### Avantages

- Réduction du couplage entre les composants.
- Point d'accès unique aux services du noyau.
- Simplification des tests unitaires.
- Préparation de l'injection de dépendances.
- Architecture plus modulaire et extensible.

### Inconvénients

- Introduction d'un composant central supplémentaire.
- Nécessité d'encadrer son utilisation afin d'éviter qu'il ne devienne un stockage global.

---

## Alternatives étudiées

### Instanciation directe

Chaque composant crée ses propres dépendances.

**Rejetée** car elle augmente fortement le couplage.

### Passage manuel des dépendances

Toutes les dépendances sont transmises dans les constructeurs.

**Non retenue** comme solution générale en raison de la complexité croissante lorsque le nombre de services augmente.

### Conteneur d'injection externe

Utilisation d'un framework d'injection de dépendances.

**Rejetée** afin de conserver un noyau simple, léger et totalement maîtrisé.

---

## Conclusion

Le **Service Registry** devient le point d'accès unique aux services internes de Shikamaru et constitue la première étape vers une architecture orientée services et faiblement couplée.
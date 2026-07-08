# ADR-0008 — Event Bus

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Les différents composants de **Shikamaru** (scheduler, plugins, MQTT, supervision, services réseau, etc.) doivent pouvoir communiquer sans créer de dépendances directes entre eux.

Un mécanisme de communication interne est nécessaire afin de conserver une architecture modulaire et évolutive.

---

## Décision

Shikamaru adopte un **Event Bus** comme mécanisme unique de communication interne.

Les composants publient des événements sur le bus sans connaître leurs destinataires.

Les composants intéressés s'abonnent aux événements qu'ils souhaitent traiter.

L'Event Bus assure le routage des événements vers les abonnés.

---

## Conséquences

### Avantages

- Réduction du couplage entre les composants.
- Communication uniforme au sein du noyau.
- Ajout de nouveaux services sans modifier les composants existants.
- Architecture orientée événements, plus modulaire et extensible.

### Inconvénients

- Suivi du flux d'exécution moins direct.
- Débogage plus complexe qu'avec des appels directs.

---

## Alternatives étudiées

### Appels directs entre composants

Chaque composant appelle directement les autres.

**Rejetée** car elle crée un fort couplage.

### Callbacks dédiés

Chaque composant expose ses propres interfaces de rappel.

**Rejetée** car cette approche devient difficile à maintenir lorsque le nombre de composants augmente.

### Bus de messages externe

Utilisation d'un broker externe (MQTT, RabbitMQ, etc.) pour les communications internes.

**Rejetée** car les échanges internes au noyau doivent rester indépendants des services externes.

---

## Conclusion

L'**Event Bus** devient le mécanisme officiel de communication interne de Shikamaru et constitue la base des interactions entre les services du noyau.
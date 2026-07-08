# ADR-0011 — Command Dispatcher

**Statut :** Acceptée  
**Version :** 1.0  
**Date :** 08/07/2026  
**Auteurs :** Cédric Harnois, ChatGPT

---

## Contexte

Shikamaru reçoit des commandes provenant de différentes sources, telles que MQTT, l'interface Web ou la ligne de commande.

Afin d'assurer un traitement uniforme, il est nécessaire de centraliser leur routage.

---

## Décision

Shikamaru adopte un **Command Dispatcher** chargé de recevoir, identifier et transmettre chaque commande au composant responsable de son exécution.

Le Dispatcher ne contient aucune logique métier. Son unique responsabilité est le routage des commandes.

---

## Conséquences

### Avantages

- Point d'entrée unique pour toutes les commandes.
- Séparation claire entre le routage et la logique métier.
- Ajout simplifié de nouvelles commandes.
- Architecture plus modulaire.

### Inconvénients

- Introduction d'un composant supplémentaire.
- Toute commande doit être enregistrée auprès du Dispatcher.

---

## Alternatives étudiées

### Traitement direct des commandes

Chaque composant traite directement les commandes qui lui sont destinées.

**Rejetée** car cette approche augmente le couplage et multiplie les points d'entrée.

### Routage spécifique par protocole

Chaque interface implémente son propre mécanisme de routage.

**Rejetée** afin de garantir un comportement identique quelle que soit la source de la commande.

---

## Conclusion

Le **Command Dispatcher** devient le point d'entrée unique pour le routage des commandes au sein de Shikamaru.
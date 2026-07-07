# Vision

## Pourquoi Ohanna-Agent existe

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités sont garanties dans le temps.

Les logiciels évoluent.
Les machines tombent en panne.
Les configurations dérivent.
Les dépendances changent.

Pourtant, les capacités attendues de la maison doivent rester disponibles.

Ohanna-Agent est né de cette idée.

Sa mission n'est pas de surveiller des équipements.

Sa mission est de garantir les capacités définies par l'architecture de référence d'Ohanna-House.

---

## Notre vision

Nous considérons qu'une infrastructure ne doit pas être décrite uniquement par les logiciels qui la composent.

Elle doit être décrite par les services qu'elle rend.

DNS.

DHCP.

Home Assistant.

MQTT.

Sauvegardes.

Supervision.

Accès distant.

Chaque capacité possède un niveau de disponibilité attendu.

Ohanna-Agent observe en permanence ces capacités afin de garantir leur fonctionnement.

---

## Ce que fait Ohanna-Agent

Ohanna-Agent :

- observe ;
- comprend ;
- évalue ;
- décide ;
- agit.

Il ne surveille pas simplement des processus.

Il vérifie que les capacités attendues sont réellement fournies.

---

## Ce que ne fait pas Ohanna-Agent

Ohanna-Agent n'est pas un logiciel de supervision classique.

Il ne cherche pas uniquement à savoir si un service est démarré.

Il cherche à savoir si la capacité attendue est réellement garantie.

Par exemple :

Un serveur DNS peut être démarré.

Mais si aucune résolution n'est possible, la capacité DNS est indisponible.

C'est cette différence qui fonde toute la philosophie du projet.

---

## Les principes fondateurs

Toutes les décisions d'architecture d'Ohanna-Agent reposent sur les principes suivants.

### Les capacités avant les implémentations

Une capacité peut être assurée par plusieurs implémentations.

L'agent garantit la capacité.

Il ne dépend jamais d'une implémentation particulière.

---

### Les observations avant les hypothèses

Toutes les décisions doivent être prises à partir d'observations réelles.

Une configuration ne constitue jamais une preuve de fonctionnement.

Seule l'observation permet de garantir une capacité.

---

### Les plugins avant le code spécifique

Chaque capacité doit pouvoir être ajoutée, remplacée ou supprimée sans modifier le cœur du logiciel.

Le noyau reste indépendant des technologies qu'il pilote.

---

### L'autonomie avant l'intervention humaine

Lorsqu'une anomalie est détectée, l'agent privilégie toujours la solution la plus autonome possible.

L'intervention humaine reste le dernier recours.

---

### Une architecture durable

L'architecture doit rester stable.

Les implémentations peuvent évoluer.

Les plugins peuvent évoluer.

Les protocoles peuvent évoluer.

Les capacités, elles, constituent le contrat fondamental du système.

---

## Notre ambition

Construire un agent capable de garantir durablement les capacités d'une infrastructure domestique moderne.

Simple.

Fiable.

Observable.

Extensible.

Résilient.

---

## Une phrase

Ohanna-Agent ne surveille pas des logiciels.

Il garantit des capacités.
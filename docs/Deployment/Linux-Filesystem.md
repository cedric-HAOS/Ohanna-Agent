# Arborescence Linux d’Ohanna-Agent

## Objectif

Ce document définit l’arborescence Linux de référence utilisée pour installer et exécuter Ohanna-Agent en tant que service système.

Cette organisation sépare clairement :

* le logiciel installé ;
* la configuration administrée ;
* les données persistantes ;
* les journaux ;
* le service `systemd`.

Elle constitue le contrat de déploiement d’Ohanna-Agent pour la version 1.0.0.

---

## Principes

L’installation Linux respecte les principes suivants :

* le dépôt Git n’est pas utilisé comme répertoire d’exécution en production ;
* le code installé n’est pas mélangé avec la configuration locale ;
* les fichiers de configuration sont conservés lors d’une mise à jour ;
* l’application s’exécute avec un utilisateur système dédié ;
* les journaux sont transmis à `systemd-journald` ;
* les chemins nécessaires sont fournis explicitement au CLI ;
* aucune donnée modifiable n’est écrite dans l’environnement Python installé.

---

## Arborescence de référence

```text
/
├── etc/
│   ├── ohanna-agent/
│   │   ├── shikamaru.yaml
│   │   ├── infrastructure.yaml
│   │   └── plugins/
│   │       └── dns.yaml
│   │
│   └── systemd/
│       └── system/
│           └── ohanna-agent.service
│
├── opt/
│   └── ohanna-agent/
│       └── venv/
│           ├── bin/
│           │   ├── python
│           │   └── ohanna-agent
│           └── ...
│
└── var/
    └── lib/
        └── ohanna-agent/
```

---

## Logiciel installé

Le logiciel est installé dans un environnement Python isolé :

```text
/opt/ohanna-agent/venv/
```

Le point d’entrée exécutable est :

```text
/opt/ohanna-agent/venv/bin/ohanna-agent
```

Le répertoire `/opt/ohanna-agent` contient uniquement les éléments nécessaires à l’exécution du logiciel installé.

Il ne contient pas :

* les fichiers de configuration de l’utilisateur ;
* une copie de travail du dépôt Git ;
* les tests ;
* les scripts de développement ;
* les journaux ;
* les données persistantes.

Les mises à jour remplacent ou mettent à niveau l’environnement Python sans écraser la configuration située dans `/etc/ohanna-agent`.

---

## Configuration

Les fichiers de configuration actifs sont placés dans :

```text
/etc/ohanna-agent/
```

La structure retenue est :

```text
/etc/ohanna-agent/
├── shikamaru.yaml
├── infrastructure.yaml
└── plugins/
    └── dns.yaml
```

### Configuration principale

```text
/etc/ohanna-agent/shikamaru.yaml
```

Ce fichier contient la configuration générale de l’agent :

* identité de l’agent ;
* environnement ;
* MQTT ;
* journalisation ;
* santé ;
* plugins ;
* connexion à Ohanna-Vision.

### Infrastructure

```text
/etc/ohanna-agent/infrastructure.yaml
```

Ce fichier décrit l’infrastructure observée :

* nœuds ;
* endpoints ;
* services ;
* capacités associées.

### Plugin DNS

```text
/etc/ohanna-agent/plugins/dns.yaml
```

Ce fichier contient la configuration propre au plugin DNS :

* services DNS observés ;
* requêtes de contrôle ;
* délais ;
* tentatives ;
* intervalle d’exécution ;
* politique de santé.

### Fichiers d’exemple

Les fichiers `.example.yaml` appartiennent au dépôt et à la documentation du projet.

Ils ne sont pas utilisés directement par le service de production.

Lors de l’installation initiale, l’installateur peut s’en servir pour créer les fichiers actifs dans `/etc/ohanna-agent`, mais il ne doit pas écraser une configuration déjà présente.

---

## Données persistantes

Le répertoire réservé aux données persistantes est :

```text
/var/lib/ohanna-agent/
```

Il appartient à l’utilisateur système exécutant Ohanna-Agent.

Dans la version actuelle, le bootstrap de production ne persiste encore aucune donnée dans ce répertoire. Celui-ci est réservé aux fonctionnalités futures qui nécessiteront réellement un stockage local, par exemple :

* mémoire persistante ;
* état de reprise ;
* files d’attente temporaires durables ;
* métadonnées d’exécution.

Aucun fichier fictif ne doit être créé pour simuler un besoin de persistance.

Le répertoire peut ne pas être créé tant qu’aucun composant de production ne l’utilise.

---

## Journaux

Ohanna-Agent écrit ses journaux sur la sortie standard et la sortie d’erreur.

En tant que service `systemd`, ces flux sont collectés par :

```text
systemd-journald
```

Aucun répertoire dédié n’est donc requis sous :

```text
/var/log/ohanna-agent/
```

Les journaux sont consultés avec :

```bash
journalctl -u ohanna-agent
```

Pour suivre l’exécution en direct :

```bash
journalctl -u ohanna-agent -f
```

Cette stratégie évite :

* la gestion manuelle de fichiers de log ;
* la rotation propre à l’application ;
* les problèmes de permissions dans `/var/log` ;
* la duplication entre fichiers et journal système.

Si une sortie vers fichiers devient nécessaire ultérieurement, elle devra être décidée explicitement.

---

## Service systemd

Le fichier de service administré localement est placé dans :

```text
/etc/systemd/system/ohanna-agent.service
```

Il démarre l’exécutable :

```text
/opt/ohanna-agent/venv/bin/ohanna-agent
```

avec les chemins de configuration explicites :

```text
--config /etc/ohanna-agent/shikamaru.yaml
--infrastructure /etc/ohanna-agent/infrastructure.yaml
--dns-config /etc/ohanna-agent/plugins/dns.yaml
```

Le service ne doit pas dépendre du répertoire courant pour retrouver ses fichiers.

Le contenu précis de l’unité est défini dans l’étape consacrée au service `systemd`.

---

## Utilisateur système

Ohanna-Agent s’exécute avec un compte système dédié :

```text
ohanna-agent
```

Ce compte :

* ne possède pas de shell interactif ;
* ne possède pas de mot de passe ;
* n’exécute pas l’application avec les droits `root` ;
* peut lire `/etc/ohanna-agent` ;
* peut exécuter l’environnement situé dans `/opt/ohanna-agent/venv` ;
* peut écrire dans `/var/lib/ohanna-agent` seulement lorsque ce répertoire est utilisé.

Le groupe système associé porte également le nom :

```text
ohanna-agent
```

---

## Propriétaires et permissions

### Logiciel

```text
/opt/ohanna-agent
```

Propriétaire recommandé :

```text
root:root
```

Permissions recommandées pour les répertoires :

```text
0755
```

Le compte `ohanna-agent` peut exécuter le logiciel, mais ne peut pas le modifier.

### Configuration

```text
/etc/ohanna-agent
```

Propriétaire recommandé :

```text
root:ohanna-agent
```

Permissions recommandées pour les répertoires :

```text
0750
```

Permissions recommandées pour les fichiers ne contenant aucun secret :

```text
0640
```

Le compte de service peut lire les fichiers, mais ne peut pas les modifier.

Si une configuration contient ultérieurement des secrets, elle doit rester lisible uniquement par `root` et le groupe `ohanna-agent`.

### Données persistantes

```text
/var/lib/ohanna-agent
```

Propriétaire recommandé :

```text
ohanna-agent:ohanna-agent
```

Permissions recommandées :

```text
0750
```

---

## Correspondance avec le CLI

Le service Linux utilise les arguments déjà fournis par Ohanna-Agent :

| Argument           | Chemin Linux                            |
| ------------------ | --------------------------------------- |
| `--config`         | `/etc/ohanna-agent/shikamaru.yaml`      |
| `--infrastructure` | `/etc/ohanna-agent/infrastructure.yaml` |
| `--dns-config`     | `/etc/ohanna-agent/plugins/dns.yaml`    |
| `--log-level`      | niveau choisi par le service            |

Commande de référence :

```bash
/opt/ohanna-agent/venv/bin/ohanna-agent \
  --config /etc/ohanna-agent/shikamaru.yaml \
  --infrastructure /etc/ohanna-agent/infrastructure.yaml \
  --dns-config /etc/ohanna-agent/plugins/dns.yaml \
  --log-level INFO
```

Cette commande ne dépend d’aucun chemin relatif.

---

## Développement et production

Les chemins présents dans le dépôt restent valides pour le développement :

```text
config/shikamaru.yaml
config/infrastructure.yaml
config/plugins/dns.yaml
```

Ils permettent de lancer localement :

```bash
ohanna-agent
```

L’installation de production utilise en revanche les chemins absolus sous `/etc/ohanna-agent`.

Les deux modes ne doivent pas être confondus :

| Contexte             | Configuration             |
| -------------------- | ------------------------- |
| développement        | `config/` dans le dépôt   |
| production Linux     | `/etc/ohanna-agent/`      |
| logiciel installé    | `/opt/ohanna-agent/venv/` |
| données persistantes | `/var/lib/ohanna-agent/`  |
| journaux             | `systemd-journald`        |

---

## Éléments volontairement absents

L’arborescence ne prévoit pas actuellement :

```text
/var/log/ohanna-agent/
/run/ohanna-agent/
/var/cache/ohanna-agent/
/usr/share/ohanna-agent/
/opt/ohanna-agent/config/
```

Ces emplacements ne répondent à aucun besoin réel du bootstrap actuel.

Ils ne devront être ajoutés que lorsqu’un composant de production les utilisera effectivement.

---

## Contrat pour la version 1.0.0

L’arborescence Linux de référence d’Ohanna-Agent 1.0.0 est :

```text
Logiciel       /opt/ohanna-agent/venv
Exécutable     /opt/ohanna-agent/venv/bin/ohanna-agent
Configuration  /etc/ohanna-agent
Service        /etc/systemd/system/ohanna-agent.service
Données        /var/lib/ohanna-agent
Journaux       systemd-journald
Utilisateur    ohanna-agent
Groupe         ohanna-agent
```

Cette structure doit être utilisée par le service `systemd`, les procédures d’installation et le futur Ohanna-Installer.

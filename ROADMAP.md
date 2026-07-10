# ROADMAP

## Vision

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités restent garanties dans le temps.

Ohanna-Agent ne supervise pas des machines.

Il garantit que les **capacités** attendues par l'architecture de référence sont disponibles, observables et mesurables.

Chaque évolution du projet poursuit un objectif unique :

> Transformer des observations techniques en une vision fiable de l'état de l'infrastructure.

---

# État actuel

Le cœur d'Ohanna-Agent est désormais opérationnel.

Les fondations suivantes sont en place :

* Infrastructure déclarative
* Scheduler
* Dispatcher
* EventBus
* Runtime Infrastructure
* Plugin SDK
* Plugin Manager
* Observation Engine
* Observation Export Pipeline
* Vision Exporter
* DNS Plugin
* Configuration déclarative des plugins
* Démonstration complète de bout en bout

Le premier pipeline complet fonctionne désormais :

```text
Infrastructure
        │
        ▼
Plugin DNS
        │
        ▼
Observation Engine
        │
        ▼
Observation Export Pipeline
        │
        ▼
Ohanna-Vision
```

Ce pipeline constitue la base de tous les développements futurs.

---

# Phase 1 — Fondations ✓

Objectif :

Construire le socle technique d'Ohanna-Agent.

Réalisé :

* cycle de vie de l'application ;
* configuration ;
* EventBus ;
* Scheduler ;
* Dispatcher ;
* système de commandes ;
* Runtime ;
* Plugin SDK.

**Statut : terminé.**

---

# Phase 2 — Infrastructure déclarative ✓

Objectif :

Décrire entièrement l'infrastructure sous forme déclarative.

Réalisé :

* modèle Infrastructure ;
* Node ;
* Service ;
* Endpoint ;
* InfrastructureRuntime ;
* InfrastructureLoader ;
* InfrastructureBuilder ;
* validation de cohérence ;
* configuration YAML.

Les plugins utilisent désormais cette infrastructure comme source unique de vérité.

**Statut : terminé.**

---

# Phase 3 — Moteur d'observation ✓

Objectif :

Transformer les résultats des plugins en observations standardisées.

Réalisé :

* Observation ;
* ObservationFactory ;
* ObservationMapper ;
* ObservationEngine ;
* ObservationPublisher ;
* ObservationExportPipeline ;
* VisionObservationExporter ;
* sérialisation JSON ;
* export automatique.

Toutes les observations utilisent désormais un modèle commun.

**Statut : terminé.**

---

# Phase 4 — Plugins déclaratifs ✓

Objectif :

Unifier tous les plugins.

Réalisé :

* contrat `Plugin.execute()` ;
* `ObserverResult` standardisé ;
* DNSConfigurationBuilder ;
* DNSConfigLoader ;
* configuration déclarative des plugins ;
* suppression des adresses IP des configurations des plugins ;
* démonstration réelle de bout en bout.

Le plugin DNS est désormais entièrement intégré au pipeline d'observation.

**Statut : terminé.**

---

# Phase 5 — Plugins de capacités

Objectif :

Étendre Ohanna-Agent à l'ensemble des capacités de l'infrastructure.

Plugins prévus :

* DHCP
* MQTT
* Internet
* NTP
* WireGuard
* HTTP
* HTTPS
* ICMP
* Home Assistant
* Sauvegardes
* Docker
* Certificats TLS
* NAS
* SMB
* SSH

Chaque plugin suivra exactement la même architecture que le plugin DNS.

---

# Phase 6 — Ohanna-Vision

Objectif :

Construire l'interface de supervision.

Fonctionnalités prévues :

* tableau de bord temps réel ;
* historique des observations ;
* visualisation de l'état des capacités ;
* santé globale de l'infrastructure ;
* chronologie des événements ;
* statistiques ;
* graphiques ;
* recherche et filtrage.

Ohanna-Agent deviendra alors le moteur d'observation d'Ohanna-Vision.

---

# Phase 7 — Intégration Home Assistant

Objectif :

Permettre à Home Assistant de consommer directement les observations produites par Ohanna-Agent.

Fonctionnalités prévues :

* publication MQTT ;
* entités diagnostiques ;
* capteurs de santé ;
* événements Home Assistant ;
* automatisations basées sur les capacités.

Home Assistant ne réalisera plus les vérifications lui-même.

Il exploitera celles produites par Ohanna-Agent.

---

# Phase 8 — Auto-réparation

Objectif :

Passer de l'observation à l'action.

Fonctionnalités envisagées :

* redémarrage automatique de services ;
* renouvellement DHCP ;
* redémarrage WireGuard ;
* relance MQTT ;
* bascule DNS ;
* exécution de scripts ;
* notifications.

Les réparations seront déclenchées par des politiques explicites.

---

# Phase 9 — SDK Ohanna

Objectif :

Faciliter le développement de nouveaux plugins.

Le SDK fournira notamment :

* générateur de plugins ;
* modèles de projet ;
* tests automatiques ;
* simulateurs ;
* documentation ;
* outils de validation.

Créer un nouveau plugin devra nécessiter seulement quelques fichiers.

---

# Phase 10 — Écosystème Ohanna

Objectif :

Construire une architecture complète autour d'Ohanna-Agent.

Les principaux projets seront :

* **Ohanna-Agent** : moteur d'observation.
* **Ohanna-Vision** : interface Web.
* **Ohanna-SDK** : développement des plugins.
* **Ohanna-CLI** : administration et diagnostic.
* **Ohanna-House** : description déclarative de l'infrastructure.

Chaque projet possédera une responsabilité clairement définie.

---

# Objectif à long terme

À terme, l'ajout d'une nouvelle capacité devra suivre un processus simple :

1. Déclarer le service dans `infrastructure.yaml`.
2. Ajouter la configuration du plugin dans `config/plugins/`.
3. Développer un plugin implémentant `Plugin.execute()`.
4. Laisser le pipeline produire, publier et exporter automatiquement les observations.

Aucune modification du cœur d'Ohanna-Agent ne devra être nécessaire.

C'est ce principe qui garantit la pérennité et l'extensibilité de l'architecture.

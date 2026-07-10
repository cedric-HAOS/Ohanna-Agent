# Ohanna-Agent

> Garantir les capacités de l'infrastructure, plutôt que surveiller des équipements.

---

# Vision

Une infrastructure fiable n'est pas uniquement une infrastructure qui fonctionne.

C'est une infrastructure dont les capacités restent garanties dans le temps.

Les logiciels évoluent.

Les configurations changent.

Les machines peuvent tomber en panne.

Pourtant, les services attendus par la maison doivent continuer à être disponibles.

**Ohanna-Agent** est un moteur d'observation capable de vérifier ces capacités de manière continue, de produire des observations normalisées et de les transmettre à **Ohanna-Vision**.

L'objectif n'est pas de superviser des machines.

L'objectif est de superviser des **capacités**.

Par exemple :

* Résolution DNS
* Service DHCP
* Broker MQTT
* Home Assistant
* Internet
* WireGuard
* NTP
* Sauvegardes
* etc.

---

# Philosophie

L'architecture repose sur trois principes.

## 1. Infrastructure déclarative

L'infrastructure est décrite une seule fois.

Exemple :

```text
config/infrastructure.yaml
```

Chaque plugin référence des services de cette infrastructure.

Il ne contient jamais d'adresse IP codée en dur.

---

## 2. Plugins indépendants

Chaque capacité est implémentée dans un plugin indépendant.

Exemple :

```
plugins/
    dns/
    mqtt/
    dhcp/
    internet/
    ntp/
```

Chaque plugin possède :

* sa configuration
* son runtime
* ses statistiques
* ses observations

---

## 3. Observations standardisées

Tous les plugins produisent exactement le même modèle d'observation.

Une observation contient notamment :

* la capacité observée
* le nœud concerné
* le service concerné
* le statut
* la latence
* le message
* les métadonnées techniques

Les exporteurs peuvent ensuite envoyer ces observations vers différents systèmes.

---

# Architecture

Le pipeline d'exécution est désormais entièrement unifié.

```text
Scheduler
      │
      ▼
DispatcherTaskExecutor
      │
      ▼
PluginObservationDispatcher
      │
      ▼
PluginObservationExecutor
      │
      ▼
Plugin.execute()
      │
      ▼
ObserverResult
      │
      ▼
ObservationEngine
      │
      ▼
ObservationPublished
      │
      ▼
ObservationExportPipeline
      │
      ▼
VisionObservationExporter
      │
      ▼
Ohanna-Vision
```

Chaque étape possède une responsabilité unique.

---

# Configuration

## Infrastructure

L'infrastructure est décrite dans :

```text
config/infrastructure.yaml
```

Elle définit notamment :

* les nœuds
* les services
* les endpoints
* les ports

Exemple :

```yaml
services:
  - id: dns-primary
    name: DNS principal
    type: dns
    node: zwave-01
    port: 53
```

---

## Plugins

Chaque plugin possède son propre fichier déclaratif.

Exemple :

```text
config/plugins/dns.yaml
```

```yaml
services:
  - dns-primary

queries:
  - example.com
  - openai.com

timeout: 2.0

retries: 1
```

Aucune adresse IP n'est dupliquée.

Le plugin résout automatiquement les services à partir de l'infrastructure.

---

# Démonstration

Une démonstration complète est fournie.

```bash
python -m scripts.demo_dns_pipeline
```

Le script :

* charge l'infrastructure ;
* charge la configuration DNS ;
* résout automatiquement le serveur DNS ;
* exécute une vraie résolution DNS ;
* met à jour le runtime ;
* génère une observation ;
* exporte cette observation vers un faux client Ohanna-Vision.

Exemple de sortie :

```
Resolved DNS server : 192.168.1.11

Hostname            : example.com

Latency             : 3.86 ms

Status              : healthy

Observation exported to Vision
```

---

# Tests

Le projet est fortement orienté qualité.

À ce jour :

* **851 tests unitaires et d'intégration**
* Ruff
* Typage Python
* Architecture modulaire
* Injection de dépendances

Lancer les tests :

```bash
ruff check .
pytest
```

---

# État actuel

Les composants actuellement disponibles sont notamment :

* Infrastructure déclarative
* Scheduler
* Dispatcher
* EventBus
* Plugin SDK
* Plugin Manager
* DNS Plugin
* Observation Engine
* Observation Export Pipeline
* Vision Exporter
* Runtime Infrastructure
* Observation Runtime
* Pipeline d'exécution unifié

---

# Roadmap

Les prochaines étapes concernent notamment :

* nouveaux plugins (DHCP, MQTT, Internet, NTP, WireGuard…) ;
* enrichissement du modèle d'infrastructure ;
* interface Web Ohanna-Vision ;
* intégration native avec Home Assistant.

---

# Licence

Projet développé dans le cadre de l'écosystème **Ohanna**.

© Cédric Harnois

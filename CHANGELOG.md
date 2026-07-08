# CHANGELOG

Toutes les évolutions importantes du projet **Ohanna-Agent** sont documentées dans ce fichier.

Le projet suit les principes du **Semantic Versioning**.

---

# Version 4.0.0

**Date :** Juillet 2026

## Sprint 4 — Health & Recovery

Cette version introduit l'architecture complète de supervision et d'auto-réparation de **Shikamaru**.

Le noyau devient capable de surveiller son propre état, de détecter des anomalies et d'orchestrer des stratégies de récupération, tout en restant totalement découplé des plugins métier.

---

## Nouveautés

### Supervision

Nouveau package :

```text
health/
```

Ajout de :

* Health Monitor
* Heartbeat
* Watchdog

Nouvelles fonctionnalités :

* surveillance des composants ;
* agrégation de l'état de santé ;
* calcul de l'état global ;
* surveillance temporelle ;
* gestion des heartbeats.

---

### Auto-réparation

Nouveau package :

```text
recovery/
```

Ajout de :

* Recovery Engine
* Recovery Strategy
* Recovery Policy
* Recovery Action
* Recovery Result

Nouvelles fonctionnalités :

* orchestration des récupérations ;
* stratégies indépendantes ;
* politiques de récupération ;
* historique des récupérations ;
* prévention des récupérations concurrentes.

---

### Résilience

Implémentation du mode dégradé.

Le noyau peut désormais :

* continuer à fonctionner malgré certaines défaillances ;
* isoler un composant défectueux ;
* préparer une récupération automatique ;
* revenir automatiquement à un état nominal lorsque les conditions le permettent.

---

### Architecture

Validation des ADR suivantes :

* ADR-0015 — Architecture du Health Monitor
* ADR-0016 — Watchdog & Heartbeat
* ADR-0017 — Recovery Engine
* ADR-0018 — Recovery Policies
* ADR-0019 — Mode dégradé

Le code est désormais aligné avec l'ensemble de ces décisions d'architecture.

---

### Documentation

Mise à jour complète des documents :

* README.md
* ROADMAP.md
* CORE.md
* CHANGELOG.md

L'ensemble de la documentation reflète désormais l'état réel du projet après le Sprint 4.

---

### Tests

Ajout de nouveaux modules de tests :

```text
test_action.py
test_engine.py
test_monitor.py
test_policy.py
test_result.py
test_strategy.py
test_watchdog.py
```

Renforcement des tests existants :

* heartbeat ;
* monitor ;
* recovery.

---

## Statistiques

Fin du Sprint 4 :

```text
Python 3.13

204 tests

204 réussis

0 échec

Ruff

100 % conforme
```

---

## Améliorations

### Architecture

* séparation claire entre supervision et récupération ;
* découplage complet entre Health et Recovery ;
* suppression des duplications dans le Recovery Engine ;
* extraction des stratégies dans leur propre module ;
* préparation des futures politiques avancées.

---

### Qualité

Amélioration de :

* la lisibilité ;
* la modularité ;
* la testabilité ;
* l'évolutivité.

---

## Compatibilité

Aucune rupture de compatibilité interne.

Les packages existants restent compatibles avec les versions précédentes du noyau.

---

## Dette technique

Dette technique restante volontairement limitée :

* future extraction de `HealthStatus`, `HealthResult` et `HealthCheck` dans des modules dédiés ;
* introduction d'un `RecoveryContext` ;
* création d'un `PolicyRegistry`.

Ces évolutions sont identifiées mais ne constituent pas des anomalies.

---

# Historique

## Version 3.0.0

### Sprint 3 — MQTT Runtime

Ajout de :

* client MQTT ;
* Publisher ;
* Subscriber ;
* reconnexion automatique ;
* transport MQTT ;
* messages typés.

Architecture événementielle finalisée.

**156 tests validés.**

---

## Version 2.0.0

### Sprint 2 — Core Services

Ajout de :

* Dispatcher ;
* Event Bus ;
* Scheduler ;
* Services ;
* Messages ;
* Plugins.

Architecture du noyau consolidée.

---

## Version 1.0.0

### Sprint 1 — Foundation

Création du noyau Shikamaru.

Ajout de :

* Application ;
* Lifecycle ;
* Configuration ;
* Logger ;
* Services de base.

---

## Version 0.1.0

### Sprint 0 — Architecture

Création du projet.

Définition de :

* Vision ;
* Philosophie ;
* Architecture ;
* Capacités ;
* Conventions MQTT ;
* Documentation ;
* ADR fondatrices.

---

# Perspectives

Le Sprint 5 sera consacré au développement des premiers plugins d'infrastructure :

* DNS ;
* DHCP ;
* NTP ;
* Supervision système ;
* Découverte réseau.

Ces plugins s'appuieront directement sur les nouvelles capacités de supervision et de résilience introduites lors du Sprint 4.

---

# Conclusion

Le Sprint 4 constitue une évolution majeure d'Ohanna-Agent.

Le projet passe d'un framework événementiel centré sur MQTT à un **framework d'agents autonomes**, capable de superviser son état, de détecter les anomalies et d'orchestrer des mécanismes d'auto-réparation.

Cette version établit les fondations techniques qui permettront de développer les futurs plugins d'infrastructure tout en conservant une architecture modulaire, testable et conforme aux ADR.

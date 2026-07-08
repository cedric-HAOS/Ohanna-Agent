# 🌳 Ohanna-Agent

**Ohanna-Agent** est un framework Python modulaire dont le premier agent est **Shikamaru**.

Son objectif est de fournir un noyau robuste, extensible et autonome capable d'orchestrer des capacités techniques telles que la configuration, la supervision, MQTT, les plugins et, à terme, l'intégration avec Home Assistant.

Le projet est développé selon une approche **Architecture First** : les décisions d'architecture sont prises et documentées avant l'écriture du code.

---

# Philosophie

Shikamaru repose sur quelques principes simples.

- L'architecture précède le code.
- Une responsabilité par composant.
- Une classe par fichier.
- Une configuration fortement typée.
- Des composants simples, testables et indépendants.
- Les bibliothèques standards Python sont privilégiées lorsqu'elles répondent déjà au besoin.
- Les décisions importantes sont documentées dans des ADR.

---

# Fonctionnalités

## Actuellement

- ✅ Gestion du cycle de vie de l'agent
- ✅ Configuration typée avec Pydantic
- ✅ Chargement YAML
- ✅ Validation automatique de la configuration
- ✅ Infrastructure de tests
- ✅ Vérification du style avec Ruff

## En cours

- 🚧 Logging
- 🚧 MQTT
- 🚧 Health Monitoring
- 🚧 Plugin Manager

## À venir

- Home Assistant
- Interface Web
- Auto-réparation
- Supervision
- Découverte automatique des plugins

---

# Architecture

```
Ohanna-Agent
│
├── config/                 # Configuration YAML
│
├── configuration/          # Modèles Pydantic
│
├── core/                   # Noyau de l'agent
│
├── docs/
│   ├── adr/
│   ├── architecture/
│   └── standards/
│
├── tests/
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Installation

Créer un environnement virtuel.

```powershell
python -m venv .venv
```

Installer les dépendances.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

# Vérification

Vérifier le style.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Lancer les tests.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

---

# Configuration

La configuration minimale se trouve dans :

```
config/shikamaru.yaml
```

Le fichier de référence documentant toutes les options est :

```
config/shikamaru.example.yaml
```

Les valeurs par défaut sont définies dans le code Python.

Le fichier YAML ne contient que les surcharges nécessaires.

---

# Documentation

Le projet est documenté selon plusieurs niveaux.

## ADR

Les décisions d'architecture sont conservées dans :

```
docs/adr/
```

## Architecture

Les documents décrivant l'architecture sont conservés dans :

```
docs/architecture/
```

## Standards

Les conventions de développement sont décrites dans :

```
docs/standards/
```

---

# Qualité

Le projet utilise :

- Python 3.13
- Pydantic
- PyYAML
- Pytest
- Ruff

Les tests automatisés garantissent la stabilité du noyau.

---

# État du projet

Version actuelle :

```
Sprint 1
```

Composants terminés :

- Lifecycle
- Configuration

Composants en cours :

- Logging
- Health
- MQTT

---

# Roadmap

## Sprint 1

Fondations du noyau

- Lifecycle
- Configuration
- Logging
- MQTT
- Health
- Plugins

## Sprint 2

Intégration Home Assistant

## Sprint 3

Interface Web

## Sprint 4

Auto-réparation

---

# Développement

Le projet suit une démarche **Architecture Driven Development**.

Chaque évolution suit les étapes suivantes :

1. Discussion
2. ADR
3. Implémentation
4. Tests
5. Audit
6. Commit

Cette méthode garantit une architecture cohérente et durable.

---

# Licence

Projet personnel de recherche et développement.

---

# Auteur

**Cédric Harnois**

avec l'assistance de **ChatGPT**.
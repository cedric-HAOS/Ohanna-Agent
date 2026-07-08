# ADR-0005 — Configuration Model

**Statut :** Accepté  
**Version :** 1.0  
**Date :** 2026-07-07  
**Décideurs :** Cédric Harnois, ChatGPT

---

## Objectif

Définir la manière dont Shikamaru représente, charge, valide et distribue sa configuration.

Cette ADR fixe les règles applicables au modèle de configuration, à l'organisation des fichiers, au chargement YAML et à la transmission des paramètres aux composants.

---

## Contexte

Shikamaru est conçu comme un agent modulaire et évolutif.

Au fil des sprints, il intégrera plusieurs composants :

- Lifecycle ;
- Configuration ;
- Logging ;
- MQTT ;
- Health ;
- Plugins ;
- Scheduler ;
- Memory ;
- AI ;
- MCP ;
- API HTTP ;
- CLI ;
- Web UI.

Tous ces composants auront besoin de paramètres de configuration.

Il est donc nécessaire de définir très tôt un modèle de configuration robuste, lisible et extensible.

---

## Décision

Shikamaru utilise un modèle de configuration typé basé sur **Pydantic**.

La configuration est chargée depuis des fichiers YAML situés dans le dossier :

```text
config/
```

Le code Python responsable de la configuration est situé dans le package :

```text
configuration/
```

Les fichiers YAML ne sont jamais lus directement par les composants.

Seul `ConfigurationLoader` est responsable du chargement.

Les composants reçoivent uniquement la section de configuration dont ils ont besoin.

---

## Organisation des dossiers

L'organisation retenue est la suivante :

```text
Ohanna-Agent/
│
├── config/
│   ├── shikamaru.yaml
│   └── shikamaru.example.yaml
│
├── configuration/
│   ├── __init__.py
│   ├── base.py
│   ├── enums.py
│   ├── agent.py
│   ├── mqtt.py
│   ├── logging.py
│   ├── health.py
│   ├── plugins.py
│   ├── configuration.py
│   └── loader.py
```

---

## Séparation code / données

Le dossier `configuration/` contient le **code Python** permettant de représenter et charger la configuration.

Le dossier `config/` contient les **fichiers YAML** utilisés pour paramétrer Shikamaru.

Cette séparation évite toute ambiguïté entre :

- les modèles Python ;
- les fichiers de configuration utilisateur.

---

## Modèle racine

L'objet racine de configuration s'appelle :

```python
Configuration
```

Il regroupe toutes les sections de configuration.

Exemple :

```python
configuration.agent.name
configuration.mqtt.host
configuration.logging.level
configuration.health.interval_seconds
configuration.plugins.directory
```

---

## Classe de base

Tous les modèles de configuration héritent d'une classe commune :

```python
Config
```

Cette classe est définie dans :

```text
configuration/base.py
```

Elle centralise les règles communes à tous les modèles.

Exemple :

```python
class Config(BaseModel):
    """
    Base class for all configuration models.

    Provides immutable and strictly validated configuration objects.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )
```

---

## Immutabilité

Les objets de configuration sont immuables.

Une fois chargée, la configuration ne doit pas être modifiée pendant l'exécution de Shikamaru.

Cette règle permet d'éviter :

- les effets de bord ;
- les modifications accidentelles ;
- les comportements difficiles à reproduire ;
- les divergences entre composants.

Toute modification de configuration nécessite un redémarrage de l'application ou un mécanisme dédié défini dans une future ADR.

---

## Validation stricte

Les modèles de configuration utilisent une validation stricte.

Les clés inconnues sont interdites.

Ainsi, une faute de frappe dans le YAML provoque une erreur au démarrage au lieu d'être silencieusement ignorée.

Exemple d'erreur souhaitée :

```yaml
mqtt:
  hots: localhost
```

La clé `hots` doit être refusée, car la clé correcte est `host`.

---

## Pydantic

Pydantic est utilisé pour :

- valider la structure de la configuration ;
- convertir les types lorsque cela est pertinent ;
- appliquer les valeurs par défaut ;
- produire des erreurs explicites ;
- fournir une meilleure autocomplétion dans VS Code ;
- faciliter les futurs exports JSON ou API.

Pydantic est retenu car Shikamaru est une plateforme appelée à évoluer, pas un simple script.

---

## Fichiers YAML

Deux fichiers YAML sont retenus.

### `config/shikamaru.yaml`

Fichier de configuration principal.

Il doit rester minimal.

Il contient uniquement les valeurs réellement configurées par l'utilisateur.

### `config/shikamaru.example.yaml`

Fichier d'exemple complet.

Il documente toutes les options disponibles.

Il sert de référence pour créer ou modifier `shikamaru.yaml`.

---

## Valeurs par défaut

Les valeurs par défaut vivent dans le code Python, dans les modèles Pydantic.

Le YAML ne doit pas répéter inutilement les valeurs par défaut.

Principe :

> Le code définit les valeurs par défaut, le YAML contient les surcharges.

Exemple :

```python
class HealthConfig(Config):
    enabled: bool = True
    interval_seconds: PositiveInt = 30
```

Le fichier `shikamaru.yaml` peut donc omettre certaines valeurs si les valeurs par défaut conviennent.

---

## Version de configuration

Le fichier YAML contient une version de configuration.

Exemple :

```yaml
version: 1
```

Cette version appartient au modèle racine `Configuration`.

Exemple :

```python
class Configuration(Config):
    version: PositiveInt = 1
```

La version n'est pas une propriété de l'agent.

Elle décrit le format global de la configuration.

Le Sprint 1 ne met pas encore en place de système de migration ou de compatibilité.

Cette possibilité sera étudiée dans une future ADR si nécessaire.

---

## Sections de configuration

Chaque grande section possède son propre fichier et son propre modèle.

Exemples :

```text
configuration/agent.py      → AgentConfig
configuration/mqtt.py       → MQTTConfig
configuration/logging.py    → LoggingConfig
configuration/health.py     → HealthConfig
configuration/plugins.py    → PluginsConfig
```

Cette organisation respecte le principe :

> Une responsabilité = un fichier.

---

## Objet racine Configuration

Le modèle racine est défini dans :

```text
configuration/configuration.py
```

Il assemble toutes les sections.

Exemple :

```python
class Configuration(Config):
    """Root configuration model."""

    version: PositiveInt = 1

    agent: AgentConfig = Field(default_factory=AgentConfig)
    mqtt: MQTTConfig = Field(default_factory=MQTTConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)
    plugins: PluginsConfig = Field(default_factory=PluginsConfig)
```

Ce modèle ne contient pas de logique métier.

Il ne fait qu'assembler les sections de configuration.

---

## ConfigurationLoader

Le chargement de la configuration est assuré par :

```python
ConfigurationLoader
```

Il est défini dans :

```text
configuration/loader.py
```

Sa responsabilité est unique :

> Charger une configuration depuis un fichier YAML et retourner un objet `Configuration` validé.

Exemple :

```python
configuration = ConfigurationLoader.load(Path("config/shikamaru.yaml"))
```

Le chargement suit la chaîne suivante :

```text
YAML
  ↓
yaml.safe_load()
  ↓
Configuration.model_validate()
  ↓
Configuration
```

`ConfigurationLoader` ne réimplémente pas la validation.

La validation est confiée à Pydantic.

---

## Injection minimale de configuration

Un composant ne reçoit jamais toute la configuration s'il n'en a pas besoin.

Exemple correct :

```python
mqtt_client = MQTTClient(configuration.mqtt)
health_monitor = HealthMonitor(configuration.health)
plugin_manager = PluginManager(configuration.plugins)
```

Exemple interdit :

```python
mqtt_client = MQTTClient(configuration)
```

Cette règle limite le couplage entre composants.

Chaque composant ne connaît que sa propre configuration.

---

## Responsabilités

### `Configuration`

Responsable de regrouper les sections de configuration.

Elle ne charge aucun fichier.

Elle ne connaît pas le système de fichiers.

Elle ne contient aucune logique métier.

### `ConfigurationLoader`

Responsable de charger un fichier YAML et de retourner une instance validée de `Configuration`.

Il ne valide pas manuellement la structure.

Il délègue la validation à Pydantic.

### Modèles de section

Chaque modèle décrit une section de configuration.

Exemples :

- `AgentConfig` ;
- `MQTTConfig` ;
- `LoggingConfig` ;
- `HealthConfig` ;
- `PluginsConfig`.

---

## Secrets

Les secrets peuvent être présents dans la configuration au Sprint 1.

Exemples :

- mot de passe MQTT ;
- token API ;
- clé privée ;
- identifiants externes.

Ils ne doivent jamais être affichés dans les logs.

Une gestion plus avancée des secrets pourra être étudiée ultérieurement.

Exemples d'évolutions possibles :

- variables d'environnement ;
- fichier `.env` ;
- coffre de secrets ;
- intégration Home Assistant secrets ;
- chiffrement local.

---

## Exemple de configuration minimale

```yaml
version: 1

agent:
  name: Shikamaru
  environment: development

mqtt:
  host: localhost
  port: 1883

logging:
  level: INFO

health:
  enabled: true
  interval_seconds: 30

plugins:
  enabled: true
  directory: ./plugins
```

---

## Exemple de configuration complète

```yaml
version: 1

agent:
  name: Shikamaru
  environment: development

mqtt:
  host: localhost
  port: 1883
  client_id: null
  keepalive_seconds: 60
  authentication:
    username: null
    password: null

logging:
  level: INFO

health:
  enabled: true
  interval_seconds: 30

plugins:
  enabled: true
  directory: ./plugins
```

---

## Gestion des erreurs

Une configuration invalide doit provoquer une erreur explicite au démarrage.

Exemples d'erreurs :

- fichier YAML introuvable ;
- YAML invalide ;
- champ inconnu ;
- valeur de type incorrect ;
- environnement inconnu ;
- niveau de log inconnu ;
- port invalide ;
- intervalle Health invalide.

Shikamaru ne doit pas démarrer avec une configuration invalide.

---

## Types spécialisés

Lorsque cela améliore la robustesse, les modèles utilisent des types Pydantic spécialisés.

Exemples :

```python
PositiveInt
```

Utilisé pour :

- ports ;
- intervalles ;
- durées ;
- versions ;
- valeurs strictement positives.

Les types trop restrictifs sont évités lorsqu'ils réduisent inutilement la flexibilité.

Exemple : `mqtt.host` reste une chaîne de caractères, car il peut représenter :

- `localhost` ;
- une adresse IP ;
- un nom DNS local ;
- un nom DNS public.

---

## Enums

Lorsqu'un ensemble de valeurs est fermé, un Enum est utilisé.

Exemples :

```python
Environment
LogLevel
```

Les enums textuels utilisent `StrEnum`.

Exemple :

```python
class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"
```

Cette approche évite les fautes de frappe et améliore la lisibilité du code.

---

## Concepts internes

Lorsqu'un groupe de propriétés représente un concept, il peut devenir un modèle dédié.

Exemple :

```python
class MQTTAuthentication(Config):
    username: str | None = None
    password: str | None = None
```

Cette règle permet de garder les modèles lisibles et évolutifs.

Cependant, les modèles ne doivent pas être multipliés sans nécessité réelle.

Le principe YAGNI reste prioritaire.

---

## Alternatives étudiées

### Dictionnaires bruts

Exemple :

```python
config["mqtt"]["host"]
```

Avantages :

- simple ;
- rapide à mettre en place ;
- aucune dépendance externe.

Inconvénients :

- fragile ;
- peu lisible ;
- pas d'autocomplétion fiable ;
- erreurs détectées tardivement ;
- fautes de frappe non détectées avant exécution.

Cette option est rejetée.

---

### Dataclasses

Exemple :

```python
@dataclass(frozen=True)
class MQTTConfig:
    host: str
    port: int = 1883
```

Avantages :

- natif Python ;
- simple ;
- typé ;
- aucune dépendance externe.

Inconvénients :

- validation manuelle ;
- conversion des types à écrire ;
- messages d'erreur moins riches ;
- moins adapté aux configurations imbriquées ;
- moins adapté à une future API ou Web UI.

Cette option est rejetée pour Shikamaru, car le projet est appelé à devenir une plateforme modulaire.

---

### Pydantic

Avantages :

- validation automatique ;
- modèles typés ;
- erreurs explicites ;
- valeurs par défaut ;
- support des modèles imbriqués ;
- sérialisation possible ;
- très adapté aux futures API ;
- bonne intégration avec l'écosystème Python moderne.

Inconvénients :

- dépendance externe ;
- légère complexité supplémentaire ;
- nécessité de fixer une version dans les dépendances.

Cette option est retenue.

---

## Conséquences

Cette décision apporte :

- une configuration typée ;
- une validation centralisée ;
- une meilleure lisibilité ;
- une meilleure autocomplétion ;
- une séparation claire entre code et données ;
- un découplage fort entre composants ;
- une architecture plus facile à faire évoluer.

Elle introduit également une dépendance externe :

```text
pydantic
```

Cette dépendance est acceptée car elle apporte une valeur immédiate et durable.

---

## Non-objectifs

Cette ADR ne définit pas encore :

- la migration automatique entre versions de configuration ;
- le rechargement dynamique de la configuration ;
- la gestion avancée des secrets ;
- la configuration par variables d'environnement ;
- les profils multiples ;
- la configuration spécifique aux plugins ;
- l'interface Web de configuration.

Ces sujets feront l'objet de futures ADR si nécessaire.

---

## Évolutions possibles

Évolutions envisageables :

- support de plusieurs profils (`development`, `production`, etc.) ;
- fusion de plusieurs fichiers YAML ;
- surcharges par variables d'environnement ;
- validation de compatibilité de version ;
- migration automatique de configuration ;
- configuration dynamique par Web UI ;
- secrets externes ;
- configuration par plugin ;
- export JSON de la configuration active.

Ces évolutions devront respecter les principes définis dans cette ADR.

---

## Références

- ADR-0001 — Lifecycle
- ADR-0002 — Application
- ADR-0003 — Composition
- ADR-0004 — State Transitions
- docs/architecture/Core.md
- docs/standards/Python-Style.md

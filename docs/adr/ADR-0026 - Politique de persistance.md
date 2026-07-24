# ADR-0026 — Politique de persistance

## Statut

Accepté

## Date

2026-07-08

## Contexte

Le Sprint 7 introduit la mémoire dans Ohana-Agent.

Certaines informations doivent rester uniquement en mémoire volatile, tandis que d’autres doivent survivre au redémarrage de l’application.

Il est donc nécessaire de définir une politique claire de persistance.

## Décision

Ohana-Agent introduit une politique de persistance explicite basée sur le scope mémoire.

Seules les entrées appartenant au scope suivant peuvent être persistées :

```text
MemoryScope.PERSISTENT
```

Les scopes suivants ne sont jamais persistés automatiquement :

```text
MemoryScope.RUNTIME
MemoryScope.SESSION
```

La persistance initiale repose sur un stockage JSON local.

```text
memory.json
```

## Architecture retenue

```text
MemoryManager
    └── MemoryStorage
            ├── load()
            ├── save()
            ├── exists()
            └── clear()
```

Le stockage persistant est isolé dans un composant dédié :

```text
MemoryStorage
```

Le `MemoryManager` ne manipule pas directement les fichiers.

## Format de stockage

Le format initial est volontairement simple :

```json
{
  "entries": {
    "example.key": {
      "key": "example.key",
      "value": "example",
      "scope": "persistent",
      "created_at": "2026-07-08T00:00:00",
      "updated_at": "2026-07-08T00:00:00",
      "metadata": {}
    }
  }
}
```

## Règles de persistance

Une entrée est persistée uniquement si :

```text
scope == MemoryScope.PERSISTENT
```

Une entrée n’est pas persistée si :

```text
scope == MemoryScope.RUNTIME
scope == MemoryScope.SESSION
```

Le stockage doit être explicite, prévisible et facilement testable.

## Sérialisation

Les valeurs persistées doivent être compatibles JSON.

Les objets non sérialisables ne sont pas acceptés dans la mémoire persistante.

En cas de valeur non sérialisable, le système doit échouer proprement avec une erreur explicite.

## Chargement

Au démarrage, le `MemoryManager` peut recharger les données persistantes via `MemoryStorage`.

Les entrées chargées conservent leur clé, leur valeur, leur scope et leurs métadonnées.

## Écriture

La sauvegarde peut être déclenchée :

```text
manuellement
à l’arrêt de l’application
après modification d’une entrée persistante
```

Le comportement exact peut évoluer, mais la responsabilité reste portée par `MemoryStorage`.

## Ce qui est volontairement exclu

Cette ADR ne couvre pas encore :

* base SQLite ;
* chiffrement ;
* compression ;
* stockage distant ;
* réplication ;
* versionnement avancé du fichier mémoire ;
* migration automatique de schéma ;
* persistance distribuée.

Ces sujets pourront être traités dans des ADR futures.

## Conséquences positives

Cette décision apporte :

* une persistance simple ;
* un stockage lisible ;
* une forte testabilité ;
* une séparation claire entre mémoire et stockage ;
* une évolution future possible vers SQLite ou autre backend ;
* une politique explicite évitant les persistances involontaires.

## Conséquences négatives

Cette décision implique :

* une limitation initiale aux valeurs JSON ;
* une gestion prudente des erreurs d’écriture ;
* une absence de transaction avancée ;
* une attention particulière aux écritures concurrentes futures.

## Alternatives étudiées

### Tout persister automatiquement

Rejeté.

Cela risquerait de conserver des données temporaires ou sensibles sans intention explicite.

### Ne rien persister pour le Sprint 7

Rejeté.

La mémoire persistante est une brique importante pour les prochains sprints.

### Utiliser SQLite immédiatement

Rejeté pour l’instant.

SQLite sera probablement pertinent plus tard, mais JSON est suffisant pour une première version claire, légère et testable.

## Décision finale

Ohana-Agent adopte une persistance explicite, limitée au scope `PERSISTENT`, avec un backend JSON local isolé derrière `MemoryStorage`.

Cette décision garantit une mémoire durable simple, contrôlée et évolutive.

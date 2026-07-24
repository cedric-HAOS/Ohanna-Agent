# Administration graphique d'Ohana-Agent

Ohana-Vision permet de gérer les baux DHCP et l'architecture sans exposer les
fichiers YAML à l'utilisateur. Ohana-Agent reste la source de vérité et le seul
composant autorisé à valider puis écrire les configurations.

## Flux

```text
Navigateur
    |
    | /api/administration/*
    v
Ohana-Vision
    |
    | Bearer token, boucle locale
    v
Ohana-Agent :8765
    |
    +-- infrastructure.yaml
    +-- fichiers dnsmasq gérés
    +-- demande de rechargement systemd
```

Le jeton n'est jamais envoyé au navigateur. Vision le lit dans
`/etc/ohana-vision/management.token` et l'utilise uniquement pour communiquer
avec l'Agent sur la boucle locale.

## Contrat versionné

| Méthode | Endpoint | Rôle |
|---|---|---|
| `GET` | `/v1/capabilities` | Découvrir les opérations disponibles |
| `GET` | `/v1/infrastructure` | Lire l'architecture courante |
| `PUT` | `/v1/infrastructure` | Valider et remplacer l'architecture |
| `GET` | `/v1/dhcp` | Lire les paramètres, réservations et baux |
| `PUT` | `/v1/dhcp` | Valider et remplacer la configuration DHCP |

Les opérations DHCP ne sont annoncées que lorsqu'elles sont activées dans la
configuration de l'Agent.

## Architecture administrable

Le document d'infrastructure transmis par `PUT /v1/infrastructure` contient les
nœuds, services, équipements, liaisons et layouts. Vision peut ainsi :

- déplacer un équipement en modifiant sa cellule `column` / `row` ;
- rattacher un service au nœud d'un équipement ;
- créer ou modifier une liaison et ses extrémités ;
- préciser la technologie, le sens et le débit de cette liaison.

Avant toute écriture, Agent vérifie les identifiants, les références entre
objets, l'unicité des cellules de grille et la validité de l'ensemble du modèle.

## Sécurité des modifications DHCP

L'Agent ne reçoit jamais de chemin de fichier ni de commande système dans la
requête HTTP. Ces valeurs proviennent exclusivement de sa configuration locale.

Lors d'une modification :

1. le document complet est validé par Pydantic ;
2. les fichiers gérés sont écrits atomiquement ;
3. `dnsmasq --test` vérifie la configuration installée ;
4. en cas de rejet, tous les fichiers précédents sont restaurés ;
5. en cas de succès, l'Agent crée
   `/run/ohana-agent/dhcp-reload.request` ;
6. l'unité systemd privilégiée installée par Ohana-Installer recharge dnsmasq.

L'Agent ne dispose donc pas lui-même du droit de lancer une commande privilégiée.

## Fichiers dnsmasq gérés

- `/etc/dnsmasq.d/00-ohana.conf`
- `/etc/dnsmasq.d/10-infrastructure.conf`
- `/etc/dnsmasq.d/20-serveurs.conf`
- `/etc/dnsmasq.d/30-infrastructure-reseau.conf`
- `/etc/dnsmasq.d/40-passerelles-domotiques.conf`
- `/etc/dnsmasq.d/50-equipements-critiques.conf`

Le fichier local `/etc/dnsmasq.d/99-local.conf` reste hors du périmètre
d'Ohana.

## Configuration

L'exemple complet se trouve dans `config/shikamaru.example.yaml`, sous la clé
`administration`. L'écoute doit rester sur `127.0.0.1` lorsque Vision et Agent
sont installés sur le même hôte.

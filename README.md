# X-scrapper

## C'est quoi ?

X-scrapper est un outil en ligne de commande qui extrait les tweets de comptes X (Twitter) et les sauvegarde dans des fichiers CSV. Il utilise la bibliothèque Python `twikit` et tes propres cookies de connexion pour s'authentifier.

---

## Prérequis

- Python 3.8 ou plus récent — [télécharger ici](https://www.python.org/downloads/)
- Un compte X actif (pour récupérer tes cookies d'authentification)

---

## Installation

```bash
git clone https://github.com/ton-compte/X-scrapper.git
cd X-scrapper
chmod +x install.sh run.sh && ./install.sh
```

C'est tout. Le script crée un environnement virtuel et installe les dépendances automatiquement.

---

## Configuration en 3 étapes

### Étape A — Récupérer tes cookies depuis le navigateur

L'outil a besoin de tes cookies de session X pour accéder aux tweets. Voici comment les trouver :

1. Ouvre [x.com](https://x.com) dans Chrome ou Firefox et connecte-toi
2. Ouvre les **DevTools** avec `F12` (ou `Cmd+Option+I` sur Mac)
3. Va dans l'onglet **Application** (Chrome) ou **Stockage** (Firefox)
4. Dans le panneau de gauche, clique sur **Cookies** > `https://x.com`
5. Cherche et copie les valeurs de ces 3 cookies :
   - `auth_token`
   - `ct0`
   - `twid`
6. Ouvre le fichier `cookies.json` et remplace les `"..."` par tes valeurs :

```json
{
    "auth_token": "COLLE_TON_AUTH_TOKEN_ICI",
    "ct0": "COLLE_TON_CT0_ICI",
    "twid": "COLLE_TON_TWID_ICI"
}
```

> **Important :** Ne partage jamais ce fichier et ne le committe pas sur Git. Ces tokens donnent accès à ton compte.

---

### Étape B — Configurer les comptes à scraper

Ouvre `scrapper.py` et modifie la variable `GROUPS` au début du fichier :

```python
GROUPS = {
    "Politiques": [
        "nom_utilisateur1", "nom_utilisateur2"
    ],
    "Journalistes": [
        "nom_utilisateur3", "nom_utilisateur4"
    ]
}
```

- Chaque **clé** (`"Politiques"`, `"Journalistes"`) est le nom du groupe — il sera utilisé comme nom de fichier CSV
- Chaque **liste** contient les pseudos X à scraper (sans le `@`)
- Tu peux créer autant de groupes que tu veux

---

### Étape C — Choisir les paramètres

Toujours dans `scrapper.py`, juste en dessous de `GROUPS` :

```python
MAX_TWEETS_PER_USER = 1000   # Nombre max de tweets à récupérer par compte
MIN_YEAR = 2020              # Ignorer les tweets antérieurs à cette année
```

---

## Lancement

```bash
./run.sh
```

Le script affiche la progression en temps réel et sauvegarde les résultats au fur et à mesure.

---

## Résultats

Les fichiers CSV sont générés dans le dossier `data/`, un fichier par groupe :

```
data/
  Politiques.csv
  Journalistes.csv
```

Chaque CSV contient les colonnes suivantes :

| Colonne | Description |
|---|---|
| `pseudo` | Nom d'utilisateur X |
| `date` | Date et heure du tweet |
| `text` | Contenu du tweet |
| `retweets` | Nombre de retweets |
| `likes` | Nombre de likes |
| `url` | Lien direct vers le tweet |

---

## Problèmes courants

**Erreur : cookies invalides ou session expirée**
Les cookies X expirent régulièrement. Répète l'Étape A pour récupérer de nouveaux cookies.

**Erreur 429 — Rate limit**
X limite le nombre de requêtes. Le script gère ça automatiquement en attendant 15 minutes avant de reprendre. Laisse-le tourner.

**Utilisateur introuvable**
Vérifie que le pseudo est correct et que le compte est public. Les comptes privés ne sont pas accessibles.

**`./install.sh` : permission refusée**
Lance `chmod +x install.sh run.sh` puis réessaie.

---

## Avertissement légal

Cet outil est destiné à un usage personnel et de recherche. Respecte les [Conditions d'utilisation de X](https://twitter.com/en/tos). N'utilise pas cet outil pour du scraping massif, du harcèlement, ou toute activité contraire aux CGU.

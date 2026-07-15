<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp : recherchez sur Marktplaats et 2dehands depuis n'importe quel agent IA" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <b>Français</b>
</p>

# marktplaats-mcp

**marktplaats-mcp** est un serveur MCP qui permet à Claude, Cursor, Codex, opencode et tout autre client MCP de chercher sur Marktplaats et 2dehands, les petites annonces d'occasion néerlandaises et belges. Dénichez de bonnes affaires, vérifiez les vendeurs, parcourez les catégories et surveillez les nouvelles annonces en langage naturel.

[![PyPI version](https://img.shields.io/pypi/v/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE)
[![CI](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml)
[![Downloads](https://img.shields.io/pypi/dm/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)

## ✨ Fonctionnalités

- 🔍 **Recherche puissante** : texte libre, catégories, fourchette de prix, état, distance depuis un code postal, ancienneté, tri
- 🇳🇱🇧🇪 **Deux places de marché, un serveur** : marktplaats.nl (Pays-Bas) et 2dehands.be (Belgique) via un paramètre `site`
- 📄 **Détails complets des annonces** : description complète, toutes les photos, nombre de vues et de favoris, ancienneté
- 🛡️ **Vérification des vendeurs** : compte bancaire, identité et téléphone vérifiés, note des avis
- 🔔 **Surveillance des nouvelles annonces** : interrogez les annonces publiées après un horodatage avec un curseur sans état
- 🧠 **Conçu pour les LLM** : sortie compacte économe en tokens, promotions payantes filtrées, résultats structurés
- 🔁 **Robuste** : nouvelles tentatives avec backoff exponentiel, jitter et prise en charge de `Retry-After`
- 🔓 **Pas de compte, pas de clé API**

## 🚀 Démarrage rapide

Le seul prérequis est [uv](https://docs.astral.sh/uv/) (`brew install uv` ou `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, une seule commande :

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Puis demandez : *« Cherche sur 2dehands un vélo cargo à moins de 1000 € près d'Anvers. »*

## 📦 Installation dans votre client préféré

Chaque configuration lance le même serveur stdio via `uvx marktplaats-mcp`. Le [README anglais](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md#-install-in-your-favorite-client) contient les extraits prêts à l'emploi pour **Claude Desktop, OpenAI Codex, opencode, Cursor, VS Code/Copilot, Windsurf, Gemini CLI et JetBrains**. La configuration est identique partout :

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```

## 🧰 Outils

| Outil | Ce qu'il fait |
|---|---|
| `search_listings` | Recherche avec requête, catégorie, fourchette de prix, état, distance, ancienneté, tri et pagination |
| `get_listing_details` | Annonce complète : description intégrale, toutes les images, vues et favoris, ancienneté |
| `get_seller_profile` | Signaux de confiance : banque, identité et téléphone vérifiés, note et nombre d'avis |
| `list_categories` | Parcourir l'arborescence des catégories (noms + identifiants) pour le filtrage |
| `check_new_listings` | Surveillance des plus récentes avec un curseur sans état : uniquement les annonces publiées après `since` |

Les cinq outils sont en lecture seule et portent les annotations MCP correspondantes : les clients sautent donc les demandes de confirmation.

### Exemples de prompts

- *« Trouve un iPhone 15 d'occasion à moins de 600 €, comme neuf, trié par prix. »*
- *« Cherche sur 2dehands un vélo cargo dans un rayon de 20 km du code postal 2000 Anvers. »*
- *« Le vendeur 12345 est-il fiable ? Vérifie son profil. »*
- *« Vérifie les nouvelles annonces "lampe vintage" depuis ma dernière consultation et résume les plus intéressantes. »*

## ❓ FAQ

**Faut-il un compte Marktplaats ou une clé API ?**
Non. Le serveur utilise les mêmes endpoints JSON publics que le site web lui-même.

**Est-ce un produit officiel de Marktplaats ?**
Non. C'est un projet open source indépendant, sans lien avec Marktplaats ou Adevinta. L'API sous-jacente n'est pas documentée et peut changer.

**Pourquoi vois-je parfois moins de résultats que la limite ?**
Les promotions payantes (DAGTOPPER/TOPADVERTENTIE) sont filtrées par défaut. Passez `include_sponsored=true` pour les inclure.

## 🤝 Contribuer

Les PR sont les bienvenues. Voir [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md). Ce projet réutilise des idées éprouvées de [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) et [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp).

## 📄 Licence

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd

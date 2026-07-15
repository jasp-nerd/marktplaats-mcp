<p align="center">
  <img src="assets/banner.svg" alt="marktplaats-mcp — recherchez sur Marktplaats & 2dehands depuis n'importe quel agent IA" width="760">
</p>

[English](README.md) | [Nederlands](README.nl.md) | **Français**

# marktplaats-mcp

**Le serveur MCP pour Marktplaats & 2dehands** — recherchez dans les petites annonces d'occasion néerlandaises et belges directement depuis Claude, Cursor, Codex, opencode ou tout autre agent IA compatible MCP. Dénichez de bonnes affaires, vérifiez les vendeurs, parcourez les catégories et surveillez les nouvelles annonces, le tout en langage naturel.

[![PyPI version](https://img.shields.io/pypi/v/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg)](https://pypi.org/project/marktplaats-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml)
[![Downloads](https://static.pepy.tech/badge/marktplaats-mcp/month)](https://pepy.tech/project/marktplaats-mcp)

> *« Trouve-moi un vélo de course d'occasion à moins de 500 € dans un rayon de 25 km d'Amsterdam, uniquement auprès de vendeurs vérifiés. »* — c'est désormais un seul prompt.

## ✨ Fonctionnalités

- 🔍 **Recherche puissante** — texte libre, catégories, fourchette de prix, état, distance depuis un code postal, ancienneté, tri
- 🇳🇱🇧🇪 **Deux places de marché, un serveur** — marktplaats.nl (Pays-Bas) et 2dehands.be (Belgique) via un simple paramètre `site`
- 📄 **Détails complets des annonces** — description complète, toutes les photos, nombre de vues/favoris et ancienneté
- 🛡️ **Vérification des vendeurs** — compte bancaire / identité / téléphone vérifiés, note des avis
- 🔔 **Surveillance des nouvelles annonces** — interrogez les annonces publiées après un horodatage avec un curseur sans état ; idéal pour les automatisations d'agents
- 🧠 **Conçu pour les LLM** — sortie compacte économe en tokens, promotions payantes filtrées par défaut, résultats structurés
- 🔁 **Robuste** — nouvelles tentatives automatiques avec backoff exponentiel, jitter et prise en charge de `Retry-After`
- 🔓 **Pas de compte, pas de clé API** — fonctionne immédiatement

## 🚀 Démarrage rapide

Le seul prérequis est [uv](https://docs.astral.sh/uv/) (`brew install uv` ou `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code** — une seule commande :

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Puis demandez simplement : *« Cherche sur 2dehands un vélo cargo à moins de 1000 € près d'Anvers. »*

## 📦 Installation dans votre client préféré

Toutes les configurations lancent le même serveur stdio via `uvx marktplaats-mcp`. Consultez le [README anglais](README.md#-install-in-your-favorite-client) pour les extraits prêts à l'emploi pour **Claude Desktop, OpenAI Codex, opencode, Cursor, VS Code/Copilot, Windsurf, Gemini CLI et JetBrains** — la configuration est identique partout :

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
| `get_listing_details` | Annonce complète : description intégrale, toutes les images, vues/favoris, ancienneté |
| `get_seller_profile` | Signaux de confiance : banque/identité/téléphone vérifiés, note et nombre d'avis |
| `list_categories` | Parcourir l'arborescence des catégories (noms + identifiants) pour le filtrage |
| `check_new_listings` | Surveillance des plus récentes avec un curseur sans état — uniquement les annonces publiées après `since` |

Tous les outils sont en lecture seule et annotés comme tels : les agents ne vous demandent donc pas de confirmation à répétition.

### Exemples de prompts

- *« Trouve un iPhone 15 d'occasion à moins de 600 €, comme neuf, trié par prix. »*
- *« Cherche sur 2dehands un vélo cargo dans un rayon de 20 km du code postal 2000 Anvers. »*
- *« Le vendeur 12345 est-il fiable ? Vérifie son profil. »*
- *« Vérifie les nouvelles annonces "lampe vintage" depuis ma dernière consultation et résume les plus intéressantes. »*

## ❓ FAQ

**Faut-il un compte Marktplaats ou une clé API ?**
Non. Le serveur utilise les mêmes endpoints JSON publics que le site web lui-même.

**Est-ce un produit officiel de Marktplaats ?**
Non — c'est un projet open source indépendant, sans lien avec Marktplaats/Adevinta. L'API sous-jacente n'est pas documentée et peut changer.

**Pourquoi vois-je parfois moins de résultats que la limite ?**
Les promotions payantes (DAGTOPPER/TOPADVERTENTIE) sont filtrées par défaut. Passez `include_sponsored=true` pour les inclure.

## 🤝 Contribuer

Les PR sont les bienvenues ! Voir [CONTRIBUTING.md](.github/CONTRIBUTING.md). Construit sur les épaules de [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) et [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp).

## 📄 Licence

[MIT](LICENSE) © 2026 jasp-nerd

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp : recherchez sur Marktplaats et 2dehands depuis n'importe quel agent IA" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <b>Français</b>
</p>

# marktplaats-mcp : le serveur MCP pour Marktplaats et 2dehands

**marktplaats-mcp** est un serveur MCP pour **Marktplaats.nl** (Pays-Bas) et **2dehands.be** (Belgique, connu en français sous le nom de **2ememain.be**), les petites annonces de seconde main néerlandaises et belges (*tweedehands*, *petites annonces d'occasion*). Il permet à Claude, ChatGPT, Cursor, Codex, Gemini, VS Code Copilot, Cline, opencode et à tout autre client MCP de chercher des annonces, de filtrer sur les attributs propres à chaque catégorie, de vérifier les vendeurs, de comparer les prix, de surveiller les nouvelles annonces et, avec votre propre connexion, de lire et d'envoyer vos messages, de faire des enchères et de gérer vos favoris et vos propres annonces. Pas de clé API. Fonctionne en local via stdio, ou comme point d'accès hébergé que vous collez dans claude.ai en une seule étape.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🌐 Utiliser sur claude.ai (sans installation)

Une copie hébergée de ce serveur tourne sur `https://marktplaats-mcp.jaspnerd.dev/mcp`, prête pour [claude.ai](https://claude.ai) dans votre navigateur ou dans l'application mobile Claude. Les connecteurs personnalisés fonctionnent sur tous les forfaits Claude, y compris Free.

1. Ouvrez [claude.ai](https://claude.ai) → **Settings → Connectors → Add custom connector**.
2. Collez `https://marktplaats-mcp.jaspnerd.dev/mcp` comme URL et cliquez sur **Add**. Aucun compte ni clé requis.
3. Demandez à Claude : *« Cherche sur Marktplaats une TV OLED à moins de 400 € près du code postal 3011 AB et vérifie le vendeur. »*

Le point d'accès hébergé exécute le même code que le paquet PyPI, applique une limite de débit par client et ne propose que les outils en lecture seule. Pour utiliser votre propre compte, installez-le en local, voir ci-dessous.

## 🚀 Démarrage rapide (en local)

Le seul prérequis est [uv](https://docs.astral.sh/uv/) (`brew install uv` ou `curl -LsSf https://astral.sh/uv/install.sh | sh`).

**Claude Code**, une seule commande :

```bash
claude mcp add marktplaats -- uvx marktplaats-mcp
```

Puis demandez : *« Trouve un vélo de course à moins de 500 € dans un rayon de 25 km du code postal 1011 AB, cadre de 57 à 61 cm, et dis-moi si les vendeurs ont l'air fiables. »*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp : un agent IA cherche un vélo de course et vérifie le vendeur, rendu comme une session de terminal CRT rétro" width="800">
</p>

## 👤 Utiliser votre propre compte (messages, favoris, enchères, vos annonces)

Marktplaats n'a pas d'API publique et sa connexion repose sur une authentification à deux facteurs par SMS et sur reCAPTCHA : ce serveur ne vous demande donc jamais votre mot de passe. Il emprunte à la place la session d'un navigateur où vous êtes déjà connecté, comme le fait `yt-dlp --cookies-from-browser` :

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

La commande cherche une session Marktplaats / 2dehands dans Chrome, Firefox, Safari, Edge, Brave, Arc et consorts (sous macOS, une autorisation d'accès au trousseau est demandée une fois ; cliquez sur Autoriser), la vérifie auprès du site et la stocke dans `~/.config/marktplaats-mcp/session.json`, lisible uniquement par votre utilisateur. Redémarrez votre client MCP et les outils de compte apparaissent. Commandes utiles :

```bash
marktplaats-mcp login --read-only     # never send, bid or change favorites
marktplaats-mcp login --paste         # paste a Cookie header from DevTools instead
marktplaats-mcp status                # is the stored session still valid?
marktplaats-mcp logout                # delete it
```

<details>
<summary><b>Si login indique qu'il n'a pas pu lire les cookies de votre navigateur</b></summary>

- **macOS** : le système empêche les outils en ligne de commande de lire les données des navigateurs, sans rien demander. Une seule fois, ouvrez Réglages Système → Confidentialité et sécurité → **Accès complet au disque**, ajoutez votre application de terminal (Terminal, iTerm, Warp ou VS Code), quittez-la complètement et rouvrez-la. Relancez ensuite la commande de connexion.
- **Windows** : Chrome et Edge verrouillent leur fichier de cookies pendant qu'ils tournent ; l'outil le copie d'abord, donc cela fonctionne normalement. Sinon, fermez le navigateur et réessayez, ou utilisez `--paste`.
- **Linux** : les navigateurs Chromium gardent la clé des cookies dans votre trousseau (GNOME Keyring ou KWallet), qui doit être déverrouillé ; Firefox n'a besoin de rien. Les navigateurs Snap ou Flatpak rangent leur profil ailleurs : utilisez `--paste`.
- Partout : `marktplaats-mcp login --paste` ne demande aucune permission. Dans votre navigateur sur marktplaats.nl, appuyez sur F12 → Network, cliquez sur une requête, copiez l'en-tête `Cookie` et collez-le.
</details>

Vous pouvez aussi définir `MARKTPLAATS_COOKIE` / `TWEEDEHANDS_COOKIE` (l'en-tête `Cookie` de la requête) dans la configuration de votre client. Une session reste valable plusieurs semaines ; quand elle expire, les outils vous invitent à vous reconnecter.

**Ce qui peut mal tourner, et ce qui ne le peut pas.** Envoyer un message, contacter un vendeur et placer une enchère renvoient d'abord un aperçu et n'agissent que si l'outil est rappelé avec `confirm=true` : votre agent vous montre donc ce qu'il s'apprête à faire. Une enchère est contraignante sur Marktplaats ; l'outil refuse les enchères inférieures au minimum de l'annonce et est marqué comme destructif, si bien que les clients demandent confirmation avant de l'exécuter. Chaque écriture confirmée est ajoutée à `~/.local/state/marktplaats-mcp/writes.jsonl`. Votre session n'est jamais envoyée ailleurs qu'à marktplaats.nl ou 2dehands.be, et le point d'accès hébergé n'enregistre jamais les outils de compte. Le dépôt automatisé d'annonces est interdit par les conditions d'utilisation de Marktplaats et n'est délibérément pas implémenté.

## 📦 Installation dans votre client préféré

Chaque configuration lance le même serveur stdio via `uvx marktplaats-mcp`.

<details>
<summary><b>Claude Desktop</b></summary>

Ajoutez ceci à `claude_desktop_config.json` (macOS : `~/Library/Application Support/Claude/`, Windows : `%APPDATA%\Claude\`), puis redémarrez complètement Claude Desktop :

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

Si Claude Desktop ne trouve pas `uvx`, utilisez le chemin absolu (`which uvx`, par exemple `/Users/you/.local/bin/uvx`).
</details>

<details>
<summary><b>OpenAI Codex CLI</b></summary>

Ajoutez ceci à `~/.codex/config.toml` :

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Ou : `codex mcp add marktplaats -- uvx marktplaats-mcp`
</details>

<details>
<summary><b>opencode</b></summary>

Ajoutez ceci à `opencode.json` :

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "marktplaats": {
      "type": "local",
      "command": ["uvx", "marktplaats-mcp"],
      "enabled": true
    }
  }
}
```
</details>

<details>
<summary><b>Cursor</b></summary>

Ajoutez ceci à `~/.cursor/mcp.json` (global) ou `.cursor/mcp.json` (projet) :

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
</details>

<details>
<summary><b>VS Code / GitHub Copilot</b></summary>

Ajoutez ceci à `.vscode/mcp.json` (attention à la clé `servers` et au `type` explicite) :

```json
{
  "servers": {
    "marktplaats": {
      "type": "stdio",
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```
</details>

<details>
<summary><b>Cline</b></summary>

MCP Servers → Configure → ajoutez ceci à `cline_mcp_settings.json` :

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
</details>

<details>
<summary><b>Windsurf</b></summary>

Ajoutez ceci à `~/.codeium/windsurf/mcp_config.json` :

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
</details>

<details>
<summary><b>Gemini CLI</b></summary>

Ajoutez ceci à `~/.gemini/settings.json` :

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
</details>

<details>
<summary><b>IDE JetBrains (AI Assistant / Junie)</b></summary>

Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add :

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
</details>

<details>
<summary><b>Tout client compatible avec les serveurs distants (ChatGPT, Gemini, autres)</b></summary>

Utilisez l'URL Streamable HTTP `https://marktplaats-mcp.jaspnerd.dev/mcp`, sans authentification. Outils en lecture seule uniquement.
</details>

## 🧰 Outils

| Outil | Ce qu'il fait | Compte | Écritures |
|---|---|:---:|:---:|
| `search_listings` | Recherche avec requête, catégorie, sous-catégorie, **attributs propres à la catégorie**, fourchette de prix, état, mode de remise (retrait/envoi), distance depuis un code postal, ancienneté, mots-clés à exclure, tri et pagination | | |
| `get_listing_details` | L'annonce complète : description, attributs, statut (active/clôturée), date et heure exactes de publication, nombre de vues et de favoris, état des enchères et enchère minimale, livraison, images, taux de réponse du vendeur et ancienneté du compte. Accepte les URL collées | | |
| `get_seller_profile` | Signaux de confiance : compte bancaire vérifié, identité, téléphone, vérification professionnelle, moyen de paiement, note et nombre d'avis, enchère la plus basse acceptée par le vendeur | | |
| `list_seller_listings` | Tout ce qu'un même vendeur propose : repérez les professionnels qui se font passer pour des particuliers et les annonces en double | | |
| `list_categories` | L'arborescence des catégories (noms et identifiants) utilisée pour le filtrage, également disponible comme ressource MCP | | |
| `list_category_filters` | Découvrez les filtres d'une catégorie (marque, hauteur de cadre, kilométrage, carburant, RAM, etc.) avec leurs valeurs valides et leurs effectifs | | |
| `check_new_listings` | Surveillance des plus récentes avec un curseur sans état : ne renvoie que les annonces publiées après `since`, sans jamais en sauter une | | |
| `analyze_prices` | Prix demandés médian, quartiles, minimum, maximum et moyenne pour une recherche, plus les annonces les moins chères | | |
| `get_my_account` | Vérification de la session, messages et notifications non lus | ✅ | |
| `list_conversations`, `get_conversation` | Votre boîte de réception et les fils de messages complets | ✅ | |
| `list_my_listings`, `list_favorites`, `list_my_bids`, `list_saved_searches` | Vos annonces (vues, favoris, enchère la plus haute, expiration), vos favoris, vos enchères et vos recherches sauvegardées | ✅ | |
| `send_message`, `contact_seller` | Répondre dans un fil, ou poser une question à un vendeur et faire une offre non contraignante. Aperçu d'abord, `confirm=true` pour envoyer | ✅ | ✅ |
| `place_bid` | Enchérir sur une annonce. Aperçu d'abord, refuse les enchères inférieures au minimum, marqué comme destructif | ✅ | ✅ |
| `set_favorite`, `extend_my_listing` | Ajouter/retirer une annonce des favoris ; renouveler une de vos annonces qui arrive à expiration | ✅ | ✅ |

Les outils en lecture seule portent les annotations MCP correspondantes : les clients sautent donc les demandes de confirmation pour ceux-ci et les exigent pour les outils d'écriture. Chaque outil renvoie une sortie structurée avec un vrai schéma. Deux prompts, `bargain_hunt` et `vet_listing`, encodent les usages courants.

### Ce que vous pouvez demander, et ce qui se passe

| Vous dites | L'agent appelle |
|---|---|
| *« 450 €, est-ce un prix correct pour un iPhone 15 128 Go en bon état ? »* | `analyze_prices` → médiane, quartiles et les trois annonces les moins chères |
| *« Trouve une Golf d'occasion, 2018-2022, moins de 100 000 km, essence, chez un particulier »* | `list_category_filters("Auto's")` → `search_listings(attributes={"Bouwjaar": "2018-2022", "Kilometerstand": "-100000", "Brandstof": "Benzine", "Adverteerder": "Particulier"})` |
| *« Ce vendeur est-il fiable ? Qu'est-ce qu'il vend d'autre ? »* | `get_listing_details` → `get_seller_profile` → `list_seller_listings` |
| *« Préviens-moi quand de nouvelles annonces de vélos cargo paraissent près d'Anvers »* | `check_new_listings(site="2dehands", postcode="2000", distance_km=25)` avec le curseur renvoyé à chaque interrogation |
| *« Demande au vendeur si c'est toujours disponible et propose 120 € »* | aperçu de `contact_seller(..., offer_euros=120)` → vous confirmez → envoyé |
| *« Réponds à Piet que je peux venir le chercher samedi »* | `list_conversations` → aperçu de `send_message` → vous confirmez → envoyé |

## 🔒 Modèle de sécurité

- **Aucun identifiant par défaut.** La recherche, les détails, la vérification des vendeurs, les filtres, les statistiques de prix et la surveillance ne nécessitent aucun compte.
- **Votre session reste la vôtre.** Le serveur local lit le cookie depuis votre navigateur ou depuis un fichier que vous seul pouvez lire, ne l'envoie qu'à marktplaats.nl / 2dehands.be et ne le journalise jamais. Le point d'accès hébergé refuse de démarrer si des identifiants de compte sont configurés.
- **Les écritures sont explicites.** L'envoi de messages et les enchères passent d'abord par un aperçu et exigent `confirm=true` ; les enchères inférieures au minimum sont refusées ; `login --read-only` ou `MARKTPLAATS_READ_ONLY=1` désactive entièrement les écritures ; chaque écriture confirmée est journalisée en local.
- **Le contenu non fiable est signalé.** Le texte des annonces et les messages sont écrits par d'autres utilisateurs ; le serveur indique au modèle de les traiter comme des données, jamais comme des instructions.
- **Respectueux de la place de marché.** Les requêtes sont espacées (`MARKTPLAATS_MIN_INTERVAL_MS`, 200 par défaut), réessayées avec backoff et `Retry-After`, et les pages de résultats sont mises en cache une minute. Le point d'accès hébergé est limité en débit par client et globalement.
- **Pas de liens affiliés, pas de pistage.** Les URL des annonces sont renvoyées exactement telles que les places de marché les publient.

## ⚖️ Comparaison

| | **marktplaats-mcp** (celui-ci) | [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) | [gjoris/marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) |
|---|:---:|:---:|:---:|
| Marktplaats.nl | ✅ | ✅ | ✅ |
| 2dehands.be (Belgique), avec filtre de langue | ✅ | ❌ | ✅ |
| Filtre de sous-catégorie réellement appliqué | ✅ | ❌ | ❌ |
| Filtres d'attributs de catégorie (marque, kilométrage, RAM, etc.) par libellé | ✅ | identifiants seulement | identifiants seulement |
| Statistiques de prix, annonces d'un vendeur, suggestions orthographiques | ✅ | ❌ | ❌ |
| Détails d'annonce avec statut, heure exacte, enchères, taux de réponse du vendeur | ✅ | partiel | partiel |
| Compte : messages, favoris, enchères, annonces personnelles | lecture + écriture | ❌ | lecture seule |
| Connexion sans mot de passe (import de la session du navigateur) | ✅ | s.o. | connexion via Playwright |
| Surveillance des nouvelles annonces | ✅ | ❌ | recherches sauvegardées sur disque |
| Promotions payantes filtrées par défaut | ✅ | ❌ | ❌ |
| Installation | `uvx marktplaats-mcp` (PyPI) | `uvx git+https://…` (cassé avec la version actuelle de `mcp`) | depuis les sources |
| Point d'accès hébergé, sans installation | ✅ | ❌ | ❌ |
| Registre MCP officiel | ✅ | ❌ | ❌ |
| Canari quotidien sur l'API en direct | ✅ | ❌ | ✅ |
| Dernière version | actuelle | février 2026 | mai 2026 |

Il faut rendre à César ce qui est à César : le serveur de PonClick est arrivé le premier et sa mise en forme des annonces a inspiré celle-ci, et gjoris a été le premier à analyser les pages embarquées et à mettre en place le canari en direct. Voir [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

## ❓ FAQ

### Existe-t-il un serveur MCP pour Marktplaats ?
Oui, celui-ci. Gratuit, open source (MIT), sans clé API. Collez l'URL hébergée dans claude.ai ou lancez `uvx marktplaats-mcp`.

### Fonctionne-t-il avec 2dehands.be et la Belgique ?
Oui. Chaque outil accepte `site="2dehands"`, et `language="nl"` ou `"fr"` restreint les résultats belges à une seule langue.

### Faut-il un compte Marktplaats ou une clé API ?
Non. Seuls les outils de compte nécessitent votre propre connexion, et ils utilisent la session existante de votre navigateur plutôt qu'un mot de passe.

### L'IA peut-elle lire et envoyer mes messages Marktplaats, ou enchérir ?
Oui, avec le serveur local après `marktplaats-mcp login`. L'envoi de messages et les enchères affichent un aperçu et n'agissent qu'après votre confirmation.

### Où mes identifiants de connexion sont-ils stockés ?
Dans `~/.config/marktplaats-mcp/session.json` sur votre machine, lisible uniquement par votre utilisateur, ou dans les variables d'environnement que vous définissez vous-même. Ils ne sont jamais envoyés ailleurs qu'à marktplaats.nl / 2dehands.be. `marktplaats-mcp logout` les supprime.

### Puis-je l'utiliser sans rien installer ?
Oui : le point d'accès hébergé `https://marktplaats-mcp.jaspnerd.dev/mcp` fonctionne dans claude.ai, y compris avec le forfait Free et les applications mobiles. Il propose les outils en lecture seule.

### Fonctionne-t-il avec ChatGPT, Cursor, Gemini, VS Code et Cline ?
Oui. Tout client capable de lancer des serveurs stdio peut utiliser `uvx marktplaats-mcp` ; les clients compatibles avec les serveurs distants peuvent utiliser l'URL hébergée.

### Est-ce officiel ou affilié à Marktplaats ?
Non. C'est un projet open source indépendant, sans lien avec Marktplaats, 2dehands ou Adevinta. Il utilise les mêmes endpoints JSON publics que les sites web ; cette API n'est pas documentée et peut changer, raison pour laquelle un canari en direct tourne chaque jour.

### Pourquoi vois-je parfois moins de résultats que la limite, ou un `total_count` qui semble élevé ?
Les promotions payantes (DAGTOPPER, TOPADVERTENTIE) sont filtrées par défaut ; passez `include_sponsored=true` pour les voir. `total_count` est le décompte brut de la place de marché, avant ce filtrage.

### Quelles versions de Python sont prises en charge ?
3.10 et ultérieures. L'intégration continue teste 3.11 à 3.13 sous Linux, macOS et Windows.

## ⚙️ Configuration

| Variable | Rôle |
|---|---|
| `MARKTPLAATS_COOKIE`, `TWEEDEHANDS_COOKIE` | En-tête `Cookie` de session par site (alternative à `marktplaats-mcp login`) ; les variantes `*_FILE` le lisent depuis un fichier |
| `MARKTPLAATS_SESSION_FILE` | Emplacement où `login` stocke les sessions (par défaut `~/.config/marktplaats-mcp/session.json`) |
| `MARKTPLAATS_READ_ONLY` | `1` désactive tous les outils d'écriture |
| `MARKTPLAATS_AUDIT_LOG` | Chemin du journal d'audit des écritures, ou `off` |
| `MARKTPLAATS_MIN_INTERVAL_MS` | Espacement minimal entre les requêtes sortantes (200 par défaut) |
| `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT` | `http` sert le transport Streamable HTTP pour l'hébergement (stdio par défaut) |
| `MCP_RPS`, `MCP_GLOBAL_RPS`, `MCP_ALLOWED_HOSTS`, `MCP_ALLOWED_ORIGINS` | Limites de débit et validation Host/Origin en mode hébergé |

## 🗺️ Feuille de route

- Recherche multi-sites (NL et BE en un seul appel)
- Création de recherches sauvegardées depuis l'agent
- Bundle d'extension pour Claude Desktop (MCPB)

## 🤝 Contribuer

Les PR sont les bienvenues. Voir [CONTRIBUTING.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/.github/CONTRIBUTING.md) pour la configuration de développement : `uv sync --all-groups`, puis `uv run pytest`. `uv run python scripts/e2e_smoke.py` lance le canari en direct.

Ce projet réutilise des idées éprouvées de [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py), [marktplaats-monitor](https://github.com/jasp-nerd/marktplaats-monitor), [marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) et [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp). Détails dans [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

Si cela vous a évité un détour par Marktplaats, une étoile aide d'autres personnes à le trouver.

## 📄 Licence

[MIT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE) © 2026 jasp-nerd

---

<sub>mcp-name: io.github.jasp-nerd/marktplaats-mcp</sub>

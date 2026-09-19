<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/banner.svg" alt="marktplaats-mcp : recherchez sur Marktplaats et 2dehands depuis n'importe quel agent IA" width="760">
</p>

<p align="center">
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.md">English</a> | <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/README.nl.md">Nederlands</a> | <b>Français</b>
</p>

# marktplaats-mcp : le serveur MCP pour Marktplaats et 2dehands

**marktplaats-mcp** est un serveur MCP pour **Marktplaats.nl** (Pays-Bas) et **2dehands.be** (Belgique, connu en français sous le nom de **2ememain.be**), les petites annonces de seconde main néerlandaises et belges (*tweedehands*, *petites annonces d'occasion*). Cherchez des annonces, filtrez sur les attributs de catégorie, vérifiez les vendeurs, comparez les prix et surveillez les nouvelles annonces depuis Claude, ChatGPT, Cursor, Codex, Gemini ou tout autre client MCP. Avec votre propre connexion, il lit et envoie aussi vos messages, place des enchères et gère vos favoris et vos annonces. Pas de clé API.

<p align="center">
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/v/marktplaats-mcp.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/pyversions/marktplaats-mcp.svg" alt="Python versions"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml"><img src="https://github.com/jasp-nerd/marktplaats-mcp/actions/workflows/e2e.yml/badge.svg" alt="Live API canary"></a>
  <a href="https://pypi.org/project/marktplaats-mcp/"><img src="https://img.shields.io/pypi/dm/marktplaats-mcp.svg" alt="Downloads"></a>
  <a href="https://registry.modelcontextprotocol.io/v0/servers?search=marktplaats"><img src="https://img.shields.io/badge/MCP%20registry-listed-blue" alt="MCP registry"></a>
</p>

## 🚀 Démarrer

**Sans installation : collez une URL.** Le serveur hébergé, en lecture seule, tourne sur `https://marktplaats-mcp.jaspnerd.dev/mcp`. Ajoutez-le comme connecteur personnalisé dans [claude.ai](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md#claudeai-web-and-mobile) (Settings → Connectors, fonctionne avec le forfait Free et sur mobile), [ChatGPT](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md#chatgpt), [Mistral Le Chat](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md#mistral-le-chat), [Perplexity](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md#perplexity) ou l'[application Gemini](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md#gemini-app).

**Claude Code : une seule commande.**

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

**Tout autre client.** Installez [uv](https://docs.astral.sh/uv/getting-started/installation/) (`brew install uv`, ou `winget install --id=astral-sh.uv -e` sous Windows), puis ajoutez la configuration MCP standard :

```json
{ "mcpServers": { "marktplaats": { "command": "uvx", "args": ["marktplaats-mcp"] } } }
```

En un clic : [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) [![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) [![Add to Kiro](https://img.shields.io/badge/Kiro-Add-7B61FF?style=flat-square)](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Instructions pas à pas pour 40 clients (Cursor, VS Code, Codex, Gemini CLI, Cline, Windsurf, JetBrains, Zed, opencode, Goose, ...), avec le chemin du fichier de configuration par OS et un lien vers le guide officiel de chaque client : **[docs/clients.fr.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md)**.

Puis demandez : *« Trouve un vélo de course à moins de 500 € dans un rayon de 25 km du code postal 1011 AB, cadre de 57 à 61 cm, et dis-moi si les vendeurs ont l'air fiables. »*

<p align="center">
  <img src="https://raw.githubusercontent.com/jasp-nerd/marktplaats-mcp/main/assets/trailer-crt.gif" alt="marktplaats-mcp trailer: an AI agent searches for a racefiets and vets the seller, rendered as a retro CRT terminal session" width="800">
</p>

## 👤 Utiliser votre propre compte (messages, favoris, enchères, vos annonces)

Marktplaats n'a pas d'API publique et sa connexion repose sur une authentification à deux facteurs par SMS : ce serveur ne vous demande donc jamais votre mot de passe. Il emprunte la session d'un navigateur où vous êtes déjà connecté :

```bash
uvx --from 'marktplaats-mcp[login]' marktplaats-mcp login
```

La session est stockée dans `~/.config/marktplaats-mcp/session.json`, lisible uniquement par votre utilisateur. Redémarrez votre client MCP et les outils de compte apparaissent.

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

Envoyer un message, contacter un vendeur et enchérir renvoient d'abord un aperçu et n'agissent que si l'outil est rappelé avec `confirm=true`. Une enchère est contraignante sur Marktplaats ; l'outil refuse les enchères inférieures au minimum. Le dépôt automatisé d'annonces est interdit par les conditions de Marktplaats et n'est délibérément pas implémenté. Voir [Modèle de sécurité](#-modèle-de-sécurité).

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
Oui. Voir [docs/clients.fr.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md) pour les instructions pas à pas par client. Tout client capable de lancer des serveurs stdio peut utiliser `uvx marktplaats-mcp` ; les clients compatibles avec les serveurs distants peuvent utiliser l'URL hébergée.

### Est-ce officiel ou affilié à Marktplaats ?
Non. C'est un projet open source indépendant, sans lien avec Marktplaats, 2dehands ou Adevinta. Il utilise les mêmes endpoints JSON publics que les sites web ; cette API n'est pas documentée et peut changer, raison pour laquelle un canari en direct tourne chaque jour.

### Pourquoi vois-je parfois moins de résultats que la limite, ou un `total_count` qui semble élevé ?
Les promotions payantes (DAGTOPPER, TOPADVERTENTIE) sont filtrées par défaut ; passez `include_sponsored=true` pour les voir. `total_count` est le décompte brut de la place de marché, avant ce filtrage.

### Quelles versions de Python sont prises en charge ?
3.10 et ultérieures. L'intégration continue teste 3.11 à 3.13 sous Linux, macOS et Windows.

## 📚 Documentation

- [Installation dans votre client](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/clients.fr.md) : pas à pas pour 40 clients
- [Configuration](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/configuration.fr.md) : variables d'environnement du serveur local et hébergé
- [Comparaison](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/docs/comparison.fr.md) avec les autres serveurs MCP Marktplaats
- [Changelog](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/CHANGELOG.md)

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

# Installer marktplaats-mcp dans votre client

[← README](../README.fr.md) · English: [clients.md](clients.md) · Nederlands: [clients.nl.md](clients.nl.md)

Il y a deux façons de faire tourner ce serveur. Choisissez celle que votre client prend en charge ; le tableau ci-dessous indique le chemin le plus rapide pour chaque client.

| | **URL hébergée** (rien à installer) | **En local** `uvx marktplaats-mcp` |
|---|---|---|
| Configuration | Collez `https://marktplaats-mcp.jaspnerd.dev/mcp` | Installez [uv](#prerequisite-for-local-installs-uv), puis ajoutez une ligne de configuration |
| Outils | Recherche, détails, vérification des vendeurs, filtres, prix, surveillance | Tout, y compris vos propres messages, favoris, enchères et annonces après `marktplaats-mcp login` |
| Fonctionne dans | Tout client qui accepte un serveur MCP distant (Streamable HTTP) | Tout client qui lance des serveurs MCP locaux (stdio) |

| Client | Le plus rapide | Guide officiel |
|---|---|---|
| [Claude Code](#claude-code) | `claude mcp add --scope user marktplaats -- uvx marktplaats-mcp` | [MCP dans Claude Code](https://code.claude.com/docs/en/mcp) |
| [claude.ai](#claudeai-web-and-mobile) | Settings → Connectors → Add custom connector → collez l'URL | [Connecteurs personnalisés](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) |
| [Claude Desktop](#claude-desktop) | Comme claude.ai, ou modifiez `claude_desktop_config.json` pour les outils de compte | [Serveurs locaux](https://modelcontextprotocol.io/docs/develop/connect-local-servers) |
| [ChatGPT](#chatgpt) | Settings → Security → Developer mode → ajoutez l'URL comme app | [Developer mode](https://developers.openai.com/api/docs/guides/developer-mode) |
| [Cursor](#cursor) | [![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=) | [MCP dans Cursor](https://cursor.com/docs/mcp) |
| [VS Code / Copilot](#vs-code-and-github-copilot) | [Installer dans VS Code](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) ou `code --add-mcp` | [Serveurs MCP dans VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers) |
| [Codex / application ChatGPT de bureau](#openai-codex-and-the-chatgpt-desktop-app) | `codex mcp add marktplaats -- uvx marktplaats-mcp` | [MCP dans Codex](https://developers.openai.com/codex/mcp) |
| [Gemini CLI](#gemini-cli) | `gemini mcp add -s user marktplaats uvx marktplaats-mcp` | [Serveurs MCP](https://geminicli.com/docs/tools/mcp-server/) |
| [Application Gemini](#gemini-app) | Settings → Connected apps → Custom apps → collez l'URL | [Connecter des apps personnalisées](https://support.google.com/gemini/answer/17209137) |
| [Antigravity](#google-antigravity) | MCP Servers → View raw config | [MCP dans Antigravity](https://antigravity.google/docs/mcp?tab=ide) |
| [Windsurf / Devin Desktop](#windsurf-devin-desktop) | `devin mcp add marktplaats -- uvx marktplaats-mcp` | [MCP dans Cascade](https://docs.devin.ai/desktop/cascade/mcp) |
| [Mistral Le Chat](#mistral-le-chat) | Connectors → Add Connector → Custom MCP Connector → collez l'URL | [Connecteurs MCP](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors) |
| [Cline](#cline) | Icône MCP Servers → Configure → Configure MCP Servers | [Vue d'ensemble de MCP](https://docs.cline.bot/mcp/mcp-overview) |
| [Roo Code](#roo-code) | Icône MCP → Edit Global MCP | [Utiliser MCP dans Roo](https://docs.roocode.com/features/mcp/using-mcp-in-roo) |
| [IDE JetBrains](#jetbrains-ides-ai-assistant-and-junie) | Settings → Tools → AI Assistant → MCP → Add | [Configurer un serveur MCP](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) |
| [Zed](#zed) | Settings → AI → MCP Servers → Add Local Server | [MCP dans Zed](https://zed.dev/docs/ai/mcp) |
| [opencode](#opencode) | Ajoutez à `opencode.json` | [Serveurs MCP](https://opencode.ai/docs/mcp-servers/) |
| [Goose](#goose) | `goose configure` → Add Extension → Command-line Extension | [Utiliser les extensions](https://goose-docs.ai/docs/getting-started/using-extensions/) |
| [LM Studio](#lm-studio) | [![Add to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D) | [MCP dans LM Studio](https://lmstudio.ai/docs/app/mcp) |
| [Perplexity](#perplexity) | Account settings → Connectors → Custom connector → collez l'URL | [Connecteurs personnalisés](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors) |
| [GitHub Copilot CLI](#github-copilot-cli) | `copilot mcp add marktplaats -- uvx marktplaats-mcp` | [Ajouter des serveurs MCP](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) |
| [Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio](#more-clients) | Une ligne chacun dans le tableau ci-dessous | |

Toutes les configurations locales ci-dessous lancent la même commande, `uvx marktplaats-mcp`. Quel que soit votre client, la vérification est la même : demandez *« Cherche sur 2dehands un vélo de course à moins de 500 € près de 1000 Bruxelles »* et le client doit appeler `search_listings`.

<a name="prerequisite-for-local-installs-uv"></a>
<details>
<summary><b>Prérequis pour les installations locales : uv (une minute)</b></summary>

[uv](https://docs.astral.sh/uv/getting-started/installation/) fournit `uvx`, qui télécharge `marktplaats-mcp` depuis PyPI au premier lancement et le garde en cache. Il installe aussi Python si vous n'en avez pas.

| OS | Installation |
|---|---|
| macOS | `brew install uv` ou `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows | `winget install --id=astral-sh.uv -e` ou `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Ouvrez ensuite un **nouveau** terminal et lancez une fois `uvx marktplaats-mcp --help`. Le premier lancement prend jusqu'à une minute, le temps de télécharger les paquets ; ensuite, il démarre instantanément.

**Si un client dit qu'il ne trouve pas `uvx`**, c'est que les applications graphiques ne voient souvent pas le PATH de votre shell. Remplacez `"uvx"` dans la configuration par le chemin complet : `~/.local/bin/uvx` sous macOS/Linux (vérifiez avec `which uvx`), `%USERPROFILE%\.local\bin\uvx.exe` sous Windows (`where uvx`). Homebrew l'installe dans `/opt/homebrew/bin/uvx`.
</details>

<a name="claude-code"></a>
<details>
<summary><b>Claude Code</b> (CLI)</summary>

Une seule commande, disponible dans tous vos projets :

```bash
claude mcp add --scope user marktplaats -- uvx marktplaats-mcp
```

Vous préférez le point d'accès hébergé, en lecture seule ? `claude mcp add --scope user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`

- **Vérification :** `claude mcp list` affiche `marktplaats: ✔ Connected`, ou tapez `/mcp` dans une session. Si la première vérification indique « Failed to connect », patientez un instant : `uvx` est encore en train de télécharger le paquet.
- **Utilisation :** demandez, tout simplement. Claude choisit l'outil lui-même et demande la permission la première fois qu'il appelle le serveur.
- **Votre propre compte :** lancez `marktplaats-mcp login` une fois ; aucun changement de configuration nécessaire. Ou passez le cookie avec `--env MARKTPLAATS_COOKIE=...` avant le `--`.
- **Projet d'équipe :** committez un `.mcp.json` avec `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"]}}}` à la racine du dépôt.
- Docs : [MCP dans Claude Code](https://code.claude.com/docs/en/mcp).
</details>

<a name="claudeai-web-and-mobile"></a>
<details>
<summary><b>claude.ai</b> (web et mobile, tous les forfaits, y compris Free)</summary>

1. Sur [claude.ai](https://claude.ai), ouvrez **Settings → Connectors** et cliquez sur **Add custom connector**.
2. Nommez-le *Marktplaats*, collez `https://marktplaats-mcp.jaspnerd.dev/mcp`, laissez l'authentification sur « No sign-in », cliquez sur **Add**.
3. Dans une conversation, le connecteur apparaît sous le bouton **+** (Connectors). Posez vos questions.

Les comptes Free ont droit à un connecteur personnalisé ; Pro et Max sont sans limite. Sur les forfaits Team et Enterprise, un propriétaire l'ajoute sous **Organization settings → Connectors**, puis les membres cliquent sur **Connect**. Une fois ajouté sur le web, il est aussi disponible dans les applications iOS et Android. Outils en lecture seule uniquement ; pour votre propre compte, installez-le en local dans Claude Desktop ou Claude Code.

Docs : [Premiers pas avec les connecteurs personnalisés](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
</details>

<a name="claude-desktop"></a>
<details>
<summary><b>Claude Desktop</b> (macOS et Windows)</summary>

**Le plus rapide, en lecture seule :** Settings (`Ctrl/Cmd+,`) → **Connectors → Add → Add custom connector**, collez `https://marktplaats-mcp.jaspnerd.dev/mcp`. Comme sur claude.ai.

**En local, avec votre propre compte :** ouvrez le menu **Claude** dans la barre de menus → **Settings… → Developer → Edit Config**. Cela ouvre `claude_desktop_config.json` (macOS : `~/Library/Application Support/Claude/`, Windows : `%APPDATA%\Claude\`). Ajoutez :

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

Quittez complètement Claude Desktop et relancez-le. Cliquez ensuite sur **+** dans la zone de saisie → **Connectors** pour voir les outils Marktplaats.

- **Votre propre compte :** lancez `marktplaats-mcp login` dans un terminal, puis redémarrez Claude Desktop.
- **« Could not attach » / serveur absent :** Claude Desktop ne voit généralement pas `uvx` dans votre PATH. Utilisez le chemin absolu (`which uvx`, par exemple `/Users/you/.local/bin/uvx` ou `/opt/homebrew/bin/uvx`). Les chemins Windows nécessitent des doubles barres obliques inverses. Journaux : `~/Library/Logs/Claude/mcp*.log` ou `%APPDATA%\Claude\logs`.
- Docs : [Connecter des serveurs locaux](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Serveurs MCP locaux sur Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop).
</details>

<a name="chatgpt"></a>
<details>
<summary><b>ChatGPT</b> (web ; Plus, Pro, Business, Enterprise et Edu)</summary>

ChatGPT ne se connecte qu'à des serveurs distants : utilisez donc le point d'accès hébergé (outils en lecture seule).

1. Dans ChatGPT, ouvrez **Settings → Security and login** et activez **Developer mode**.
2. Allez sur [chatgpt.com/plugins](https://chatgpt.com/plugins), cliquez sur **+**, choisissez un nom et une description, collez `https://marktplaats-mcp.jaspnerd.dev/mcp` comme URL du serveur MCP, réglez l'authentification sur **No authentication** et cliquez sur **Create**. ChatGPT liste les outils qu'il a découverts.
3. Dans une nouvelle conversation, cliquez sur **+** → **Developer mode**, cochez *Marktplaats*, puis posez votre question.

Sur les espaces de travail Business, Enterprise et Edu, un administrateur doit d'abord autoriser les connecteurs MCP personnalisés sous **Workspace settings → Permissions**. Le forfait Free n'a pas de Developer mode.

Docs : [Developer mode de ChatGPT](https://developers.openai.com/api/docs/guides/developer-mode), [Connecter un serveur MCP à ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt).
</details>

<a name="mistral-le-chat"></a>
<details>
<summary><b>Mistral Le Chat</b> (désormais Vibe ; web, tous les forfaits, y compris Free)</summary>

1. Ouvrez **Connectors** dans la barre latérale → **+ Add Connector** → **Custom MCP Connector**.
2. Nommez-le `marktplaats` (sans espaces), collez `https://marktplaats-mcp.jaspnerd.dev/mcp` comme URL du serveur. L'authentification est détectée automatiquement (aucune n'est nécessaire).
3. Dans une conversation, cliquez sur **+** (ou tapez `/`) → **Tools** et activez *marktplaats*.

Outils en lecture seule. Sur les espaces de travail Team et Enterprise, c'est un administrateur qui ajoute le connecteur. Docs : [Connecteurs MCP](https://docs.mistral.ai/le-chat/knowledge-integrations/connectors/mcp-connectors).
</details>

<a name="cursor"></a>
<details>
<summary><b>Cursor</b></summary>

[![Add marktplaats MCP server to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0=)

Cliquez sur le bouton et confirmez dans Cursor. Ou ajoutez-le à la main dans `~/.cursor/mcp.json` (partout) ou `.cursor/mcp.json` (ce projet seulement) :

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

Alternative hébergée, en lecture seule : `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`, ou [cliquez ici](https://cursor.com/install-mcp?name=marktplaats&config=eyJ1cmwiOiJodHRwczovL21hcmt0cGxhYXRzLW1jcC5qYXNwbmVyZC5kZXYvbWNwIn0=).

- **Vérification :** la barre latérale **Customize → MCPs** affiche le serveur avec un point vert et ses outils ; la liste d'outils en haut du panneau de chat permet de les activer ou de les désactiver.
- **Utilisation :** l'Agent choisit les outils lui-même et demande votre accord avant chaque appel, sauf si vous les mettez en liste blanche sous Settings → Agents → Approvals & Execution.
- S'il ne démarre pas, redémarrez Cursor après avoir installé uv, ou utilisez le chemin absolu vers `uvx`. Journaux : panneau Output → **MCP Logs**.
- Docs : [MCP dans Cursor](https://cursor.com/docs/mcp).
</details>

<a name="vs-code-and-github-copilot"></a>
<details>
<summary><b>VS Code</b> avec GitHub Copilot (tous les forfaits Copilot, y compris Free)</summary>

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_marktplaats-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_marktplaats-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D)

Ou depuis un terminal :

```bash
code --add-mcp '{"name":"marktplaats","command":"uvx","args":["marktplaats-mcp"]}'
```

Ou à la main : Command Palette → **MCP: Open User Configuration** (ou créez `.vscode/mcp.json` dans un projet ; notez la clé `servers` et le `type` explicite) :

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

Alternative hébergée, en lecture seule : `"marktplaats": {"type": "http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

- **Vérification :** Command Palette → **MCP: List Servers** le montre en cours d'exécution (démarrez-le là si ce n'est pas le cas). Dans la vue Chat, choisissez le mode **Agent** et cliquez sur l'icône **Configure Tools** ; les outils Marktplaats y sont listés.
- **Utilisation :** demandez en mode Agent ; VS Code vous demande d'**Allow** (autoriser) les premiers appels. Faites confiance au serveur quand on vous le demande.
- Docs : [Ajouter et gérer des serveurs MCP dans VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
</details>

<a name="openai-codex-and-the-chatgpt-desktop-app"></a>
<details>
<summary><b>OpenAI Codex</b> (CLI, extension IDE et application ChatGPT de bureau)</summary>

```bash
codex mcp add marktplaats -- uvx marktplaats-mcp
```

Cela écrit dans `~/.codex/config.toml`, que la CLI Codex, l'extension IDE Codex et l'application ChatGPT de bureau partagent :

```toml
[mcp_servers.marktplaats]
command = "uvx"
args = ["marktplaats-mcp"]
```

Alternative hébergée, en lecture seule : `codex mcp add marktplaats --url https://marktplaats-mcp.jaspnerd.dev/mcp`.

Dans l'extension IDE ou l'application de bureau, vous pouvez aussi cliquer sur l'engrenage → **MCP servers → Add server**, choisir **STDIO**, saisir la commande `uvx marktplaats-mcp`, enregistrer et cliquer sur **Restart**.

- **Vérification :** `codex mcp list`, ou `/mcp` dans le composeur Codex.
- **Utilisation :** demandez ; Codex vous consulte avant les outils qui ne sont pas en lecture seule. Si le premier démarrage expire pendant que `uvx` télécharge, ajoutez `startup_timeout_sec = 60` sous le serveur.
- Docs : [MCP dans Codex](https://developers.openai.com/codex/mcp).
</details>

<a name="gemini-cli"></a>
<details>
<summary><b>Gemini CLI</b></summary>

```bash
gemini mcp add -s user marktplaats uvx marktplaats-mcp
```

Alternative hébergée, en lecture seule : `gemini mcp add -s user --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`.

Ou ajoutez à `~/.gemini/settings.json` (ou `.gemini/settings.json` dans un projet) :

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

- **Vérification :** `gemini mcp list`, ou `/mcp` dans la CLI affiche CONNECTED et la liste des outils. Les serveurs locaux ne démarrent que dans un dossier de confiance : lancez d'abord `gemini trust` si nécessaire.
- **Utilisation :** demandez ; Gemini propose « Proceed once / Always allow this tool / Always allow this server ».
- Docs : [Serveurs MCP dans Gemini CLI](https://geminicli.com/docs/tools/mcp-server/).
</details>

<a name="gemini-app"></a>
<details>
<summary><b>Application Gemini</b> (gemini.google.com et mobile)</summary>

Sur [gemini.google.com](https://gemini.google.com), ouvrez **Settings → Connected apps**, puis, sous **Custom apps**, ajoutez `https://marktplaats-mcp.jaspnerd.dev/mcp`. Une fois connecté, il fonctionne aussi dans l'application mobile ; mentionnez-le avec `@` dans un prompt. Google limite pour l'instant les apps personnalisées aux comptes personnels, 18 ans et plus, aux États-Unis, avec l'activité Gemini activée. Outils en lecture seule.

Docs : [Connecter des apps personnalisées à Gemini](https://support.google.com/gemini/answer/17209137).
</details>

<a name="google-antigravity"></a>
<details>
<summary><b>Google Antigravity</b></summary>

Dans le panneau de l'agent, cliquez sur **… → MCP Servers → Manage MCP Servers → View raw config** et ajoutez à `~/.gemini/config/mcp_config.json` (ou `.agents/mcp_config.json` dans un projet) :

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

Alternative hébergée, en lecture seule : `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (Antigravity utilise `serverUrl`, pas `url`).

Tapez `/mcp` pour ouvrir le gestionnaire MCP et vérifier que les outils sont listés ; les outils tournent en mode « Ask » par défaut. Docs : [MCP dans Antigravity](https://antigravity.google/docs/mcp?tab=ide).
</details>

<a name="windsurf-devin-desktop"></a>
<details>
<summary><b>Windsurf</b> (désormais Devin Desktop)</summary>

Windsurf a été renommé Devin Desktop. L'agent par défaut, **Devin Local**, se configure depuis un terminal :

```bash
devin mcp add marktplaats -- uvx marktplaats-mcp
```

Cela écrit `~/.config/devin/mcp_config.json` (Windows : `%APPDATA%\devin\mcp_config.json`) ; utilisez `.devin/mcp_config.json` pour un seul projet. Devin demande avant chaque appel d'outil, sauf si vous autorisez `mcp__marktplaats__*` dans ses permissions.

Pour l'ancien agent **Cascade** : **Devin Settings → Cascade → MCP Servers** (ou l'icône MCPs dans le panneau Cascade) → **View raw config**, c'est-à-dire `~/.codeium/windsurf/mcp_config.json` :

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

Alternative hébergée, en lecture seule, pour Cascade : `"marktplaats": {"serverUrl": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Appuyez ensuite sur le bouton d'actualisation du panneau MCP ; Cascade vous limite à 100 outils au total, tous serveurs confondus.

Docs : [MCP dans Cascade](https://docs.devin.ai/desktop/cascade/mcp), [Configuration MCP de la CLI Devin](https://docs.devin.ai/cli/extensibility/mcp/configuration).
</details>

<a name="cline"></a>
<details>
<summary><b>Cline</b> (VS Code, JetBrains, CLI)</summary>

Cliquez sur l'icône **MCP Servers** dans la barre d'outils supérieure de Cline → onglet **Configure** → **Configure MCP Servers**. Cela ouvre `cline_mcp_settings.json` (`~/.cline/data/settings/`) ; ajoutez :

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Alternative hébergée, en lecture seule : onglet **Remote Servers** → nom *marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, transport **Streamable HTTP** → **Add Server**.

- **Vérification :** le serveur apparaît dans le panneau MCP avec la liste de ses outils ; utilisez le bouton de redémarrage qui s'y trouve s'il affiche une erreur.
- **Utilisation :** demandez ; approuvez chaque appel, ou ajoutez les outils sans risque comme `search_listings` à `autoApprove`.
- Docs : [Vue d'ensemble de MCP](https://docs.cline.bot/mcp/mcp-overview).
</details>

<a name="roo-code"></a>
<details>
<summary><b>Roo Code</b></summary>

Cliquez sur l'icône **MCP** dans le volet Roo Code → **Edit Global MCP** (ou **Edit Project MCP** pour `.roo/mcp.json`) :

```json
{
  "mcpServers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"],
      "alwaysAllow": ["search_listings", "get_listing_details", "analyze_prices"]
    }
  }
}
```

Alternative hébergée, en lecture seule : `"marktplaats": {"type": "streamable-http", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}` (le `type` est obligatoire pour les URL). Sous Windows, enveloppez les commandes locales : `"command": "cmd", "args": ["/c", "uvx", "marktplaats-mcp"]`.

Le serveur et ses outils apparaissent dans la même vue MCP ; redémarrez VS Code si ce n'est pas le cas. Docs : [Utiliser MCP dans Roo Code](https://docs.roocode.com/features/mcp/using-mcp-in-roo).
</details>

<a name="jetbrains-ides-ai-assistant-and-junie"></a>
<details>
<summary><b>IDE JetBrains</b> (AI Assistant et Junie)</summary>

**AI Assistant :** **Settings → Tools → AI Assistant → Model Context Protocol (MCP) → Add**, choisissez **STDIO** et collez :

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

Cliquez sur **Apply** ; la colonne **Status** passe à connecté et les outils deviennent disponibles dans le chat IA (l'IA les choisit, ou tapez `/` pour en appeler un). Pour le point d'accès hébergé, choisissez **HTTP** et collez `{"mcpServers": {"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}}}`. Si le statut reste rouge, remplacez `uvx` par son chemin absolu.

**Junie** a sa propre liste : **Settings → Tools → Junie → MCP Settings → Add**, même JSON, stocké dans `~/.junie/mcp/mcp.json` (ou `.junie/mcp/mcp.json` par projet). La CLI Junie lit le même fichier.

Docs : [Configurer un serveur MCP](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html), [Paramètres MCP de Junie](https://junie.jetbrains.com/docs/junie-plugin-mcp-settings.html).
</details>

<a name="zed"></a>
<details>
<summary><b>Zed</b></summary>

**Settings → AI → MCP Servers → Add Server → Add Local Server**, ou mettez ceci dans `settings.json` :

```json
{
  "context_servers": {
    "marktplaats": {
      "command": "uvx",
      "args": ["marktplaats-mcp"]
    }
  }
}
```

Alternative hébergée, en lecture seule : `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`.

Le point à côté du serveur dans **Settings → AI → MCP Servers** passe au vert (« Server is active »). Les outils sont disponibles dans l'Agent Panel et demandent confirmation par défaut. Docs : [MCP dans Zed](https://zed.dev/docs/ai/mcp).
</details>

<a name="opencode"></a>
<details>
<summary><b>opencode</b></summary>

Ajoutez à `~/.config/opencode/opencode.json` (partout) ou à `opencode.json` dans un projet :

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

Alternative hébergée, en lecture seule : `"marktplaats": {"type": "remote", "url": "https://marktplaats-mcp.jaspnerd.dev/mcp", "enabled": true}`.

Vérifiez avec `opencode mcp list` (`opencode mcp debug marktplaats` si quelque chose cloche), puis demandez, tout simplement. Docs : [Serveurs MCP dans opencode](https://opencode.ai/docs/mcp-servers/).
</details>

<a name="goose"></a>
<details>
<summary><b>Goose</b> (CLI et bureau)</summary>

Lancez `goose configure` → **Add Extension** → **Command-line Extension**, nommez-la *marktplaats*, commande `uvx marktplaats-mcp`, acceptez les valeurs par défaut. Ou ajoutez à `~/.config/goose/config.yaml` :

```yaml
extensions:
  marktplaats:
    name: Marktplaats
    type: stdio
    cmd: uvx
    args: [marktplaats-mcp]
    enabled: true
    timeout: 300
```

Alternative hébergée, en lecture seule : `type: streamable_http` avec `uri: https://marktplaats-mcp.jaspnerd.dev/mcp`. Pour l'application de bureau, ouvrez ce lien : `goose://extension?cmd=uvx&arg=marktplaats-mcp&id=marktplaats&name=Marktplaats&description=Search%20Marktplaats%20and%202dehands`.

Vérifiez avec `goose info -v` (liste les extensions activées) ou la barre latérale **Extensions** de l'application de bureau. Docs : [Utiliser les extensions](https://goose-docs.ai/docs/getting-started/using-extensions/).
</details>

<a name="lm-studio"></a>
<details>
<summary><b>LM Studio</b> (modèles locaux)</summary>

[![Add MCP Server marktplaats to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](https://lmstudio.ai/install-mcp?name=marktplaats&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJtYXJrdHBsYWF0cy1tY3AiXX0%3D)

Ou ouvrez l'onglet **Program** dans la barre latérale droite → **Install → Edit mcp.json** (`~/.lmstudio/mcp.json`, Windows `%USERPROFILE%\.lmstudio\mcp.json`) et collez le même JSON que pour Cursor :

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

Alternative hébergée, en lecture seule : `"marktplaats": {"url": "https://marktplaats-mcp.jaspnerd.dev/mcp"}`. Choisissez un modèle qui prend en charge l'appel d'outils ; LM Studio demande confirmation à chaque appel d'outil et vous pouvez choisir « always allow ». `uvx` doit être dans votre PATH : redémarrez donc LM Studio après avoir installé uv. Docs : [MCP dans LM Studio](https://lmstudio.ai/docs/app/mcp).
</details>

<a name="perplexity"></a>
<details>
<summary><b>Perplexity</b> (web et applications de bureau)</summary>

**Hébergé :** **Account settings → Connectors → + Custom connector → Remote**. Nom *Marktplaats*, URL `https://marktplaats-mcp.jaspnerd.dev/mcp`, authentification **None**, transport **Streamable HTTP**, cochez la case de confirmation, **Add**, puis cliquez sur la carte du connecteur pour l'activer. Outils en lecture seule.

**En local (application macOS du Mac App Store) :** même page, installez l'assistant *PerplexityXPC* quand on vous le demande, **Add Connector → Simple**, nom du serveur *Marktplaats*, commande `uvx marktplaats-mcp`, **Save**. Attendez que le statut indique *Running*, puis activez-le sous **Sources** dans une conversation. Les appels d'outils demandent confirmation.

Docs : [Connecteurs distants personnalisés](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors), [MCP locaux et distants](https://www.perplexity.ai/help-center/en/articles/11502712-local-and-remote-mcps-for-perplexity).
</details>

<a name="github-copilot-cli"></a>
<details>
<summary><b>GitHub Copilot CLI</b></summary>

```bash
copilot mcp add marktplaats -- uvx marktplaats-mcp
```

Alternative hébergée, en lecture seule : `copilot mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp`. Dans une session, `/mcp add` ouvre le même formulaire et le serveur est disponible immédiatement. La configuration se trouve dans `~/.copilot/mcp-config.json` ; un dépôt peut fournir un `.github/mcp.json` au format VS Code : `{"mcpServers": {"marktplaats": {"type": "stdio", "command": "uvx", "args": ["marktplaats-mcp"], "tools": ["*"]}}}`.

Vérifiez avec `/mcp show marktplaats` ou `copilot mcp list`. Docs : [Ajouter des serveurs MCP à Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).
</details>

<a name="more-clients"></a>
<details>
<summary><b>Autres clients</b> (Kiro, Warp, Continue, Trae, Amp, Droid, Qwen Code, Kimi, Raycast, Open WebUI, LibreChat, Jan, ChatWise, Msty, Cherry Studio, 5ire, n8n, Docker, Copilot Studio, Ollama)</summary>

Local signifie `uvx marktplaats-mcp` via stdio ; hébergé signifie l'URL en lecture seule `https://marktplaats-mcp.jaspnerd.dev/mcp`. « JSON façon Claude » désigne le bloc `{"mcpServers": {"marktplaats": {"command": "uvx", "args": ["marktplaats-mcp"]}}}` de la section Claude Desktop.

| Client | Installation locale | URL hébergée | Docs |
|---|---|---|---|
| **Kiro** (IDE et CLI, ex-Amazon Q) | [Ajouter à Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22marktplaats-mcp%22%5D%7D), ou le JSON façon Claude dans `~/.kiro/settings/mcp.json` ; CLI : `kiro-cli mcp add --name marktplaats --command "uvx marktplaats-mcp" --scope global`. L'onglet MCP servers du panneau Kiro le montre connecté | [Ajouter à Kiro](https://kiro.dev/launch/mcp/add?name=marktplaats&config=%7B%22url%22%3A%22https%3A%2F%2Fmarktplaats-mcp.jaspnerd.dev%2Fmcp%22%7D) | [Configuration MCP](https://kiro.dev/docs/mcp/configuration/) |
| **Warp** | **Settings → Agents → MCP servers → + Add**, collez le JSON façon Claude (ou écrivez-le dans `~/.warp/.mcp.json`). Warp récupère aussi les serveurs des configurations Claude Code et Codex quand *Auto-spawn servers from third-party agents* est activé | Même boîte de dialogue avec `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [MCP dans Warp](https://docs.warp.dev/agent-platform/capabilities/mcp/) |
| **Continue** | Dans `~/.continue/config.yaml`, sous `mcpServers:`, ajoutez `- name: marktplaats`, `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]` ; ou déposez le JSON façon Claude dans `.continue/mcpServers/`. Les outils n'apparaissent qu'en mode Agent | `type: streamable-http`, `url: …/mcp` | [MCP en détail](https://docs.continue.dev/customize/deep-dives/mcp) |
| **Trae** | Settings → **MCP → Add → Add Manually**, collez le JSON façon Claude (ou `.trae/mcp.json` par projet). L'Agent intégré reçoit tous les serveurs | `{"mcpServers": {"marktplaats": {"url": "…/mcp"}}}` | [Ajouter des serveurs MCP](https://docs.trae.ai/ide/add-mcp-servers) |
| **Amp** | `amp mcp add marktplaats -- uvx marktplaats-mcp` ; vérifiez avec `amp mcp doctor` | `amp mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP dans Amp](https://ampcode.com/docs/customize/mcp) |
| **Factory Droid** | `droid mcp add marktplaats "uvx marktplaats-mcp"` ; vérifiez avec `droid mcp list` ou `/mcp` | `droid mcp add marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp --type http` | [MCP dans Droid](https://docs.factory.ai/cli/configuration/mcp) |
| **Qwen Code** | `qwen mcp add --transport stdio marktplaats uvx marktplaats-mcp` ; vérifiez avec `/mcp` | `qwen mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` (la clé de configuration est `httpUrl`) | [MCP dans Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/) |
| **Kimi CLI** | `kimi mcp add --transport stdio marktplaats -- uvx marktplaats-mcp` ; vérifiez avec `kimi mcp test marktplaats` | `kimi mcp add --transport http marktplaats https://marktplaats-mcp.jaspnerd.dev/mcp` | [MCP dans Kimi CLI](https://moonshotai.github.io/kimi-cli/en/customization/mcp.html) |
| **Raycast AI** (Pro) | Lancez la commande **Install MCP Server**, transport **Standard Input/Output**, commande `uvx`, arguments `marktplaats-mcp` ; tapez ensuite `@marktplaats` dans AI Chat | Même commande, transport **HTTP**, collez l'URL (la seule option sur iOS) | [MCP dans Raycast](https://manual.raycast.com/ai/model-context-protocol) |
| **Open WebUI** | Le MCP natif est HTTP uniquement. Pour le local, passez par un pont : `uvx mcpo --port 8000 -- uvx marktplaats-mcp`, puis ajoutez `http://localhost:8000` comme serveur d'outils OpenAPI | Admin → **Settings → Integrations → External Tool Servers → Add**, type **MCP (Streamable HTTP)**, auth **None** | [MCP dans Open WebUI](https://docs.openwebui.com/features/extensibility/mcp/) |
| **LibreChat** | Dans `librechat.yaml`, sous `mcpServers:`, ajoutez `marktplaats:` avec `type: stdio`, `command: uvx`, `args: ["marktplaats-mcp"]`, puis redémarrez | `type: streamable-http`, `url: …/mcp` | [Serveurs MCP](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/mcp_servers) |
| **Jan** | **Settings → MCP Servers → + Add MCP Server**, transport **STDIO**, commande `uvx`, args `marktplaats-mcp` ; choisissez un modèle doté de la capacité *tools* | Même boîte de dialogue, transport **HTTP** | [Serveurs MCP dans Jan](https://www.jan.ai/docs/desktop/integrations/mcp-servers) |
| **ChatWise** | **Settings → Tools → +**, type **Command Line (stdio)**, commande `uvx marktplaats-mcp` ; ou collez `{"mcpServers": {"marktplaats": {"command": "uvx marktplaats-mcp"}}}` via *Import JSON from Clipboard* | Type **Streamable HTTP** | [Outils](https://docs.chatwise.app/tools) |
| **Msty Studio** | **Toolbox → Add New Tool → STDIO / JSON**, collez `{"command": "uvx", "args": ["marktplaats-mcp"]}` | **Add New Tool → HTTP**, collez l'URL | [Outils](https://docs.msty.ai/studio/toolbox/tools) |
| **Cherry Studio** | **Settings → MCP → Add**, type stdio, commande `uvx`, args `marktplaats-mcp` (ou importez le JSON façon Claude), puis activez-le sur un agent | Même boîte de dialogue, Streamable HTTP | [MCP](https://docs.cherryai.com.cn/advanced-basic/extensions/mcp.md) |
| **5ire** | Tools → ajoutez avec `{"name": "marktplaats", "command": "uvx", "args": ["marktplaats-mcp"]}` | `{"name": "marktplaats", "url": "…/mcp"}` | [Docs 5ire](https://5ire.app/docs) |
| **n8n** | Non pris en charge (distant uniquement) | Ajoutez un nœud **MCP Client Tool** à un AI Agent, transport **HTTP Streamable**, endpoint `…/mcp`, authentification **None** | [MCP Client Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/) |
| **Docker MCP Toolkit** | Construisez l'image à partir du `Dockerfile` de ce dépôt et ajoutez-la à un profil avec `docker mcp profile server add <profile> --server file://marktplaats.yaml` | `docker mcp profile server add <profile> --server https://registry.modelcontextprotocol.io/v0/servers/io.github.jasp-nerd/marktplaats-mcp` | [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/) |
| **Microsoft Copilot Studio** | Non pris en charge (distant uniquement) | Agent → **Tools → Add a tool → New tool → Model Context Protocol**, URL du serveur `…/mcp`, authentification **None**. Le Copilot grand public n'a pas de connecteurs personnalisés | [Ajouter un serveur MCP](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) |
| **Ollama** | Pas de prise en charge de MCP dans l'application ni dans la CLI. Utilisez `ollama launch claude` / `codex` / `opencode` avec un modèle local et ajoutez le serveur dans ce client | Idem | [ollama launch](https://docs.ollama.com/cli) |
</details>

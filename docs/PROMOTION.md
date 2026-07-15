# Promotion playbook

How to get marktplaats-mcp in front of users. Work top-to-bottom: the official
registry feeds most directories.

## 1. Official MCP Registry (feeds everything else)

```bash
brew install mcp-publisher
mcp-publisher login github          # proves the io.github.jasp-nerd namespace
mcp-publisher publish               # uses ./server.json
```

Requirements already in place: `server.json` in the repo root, and the
`mcp-name: io.github.jasp-nerd/marktplaats-mcp` line in the README (the
registry verifies it via the PyPI package README). Bump `version` in
`server.json` in lockstep with `pyproject.toml` on every release.

## 2. Directories (the big four)

| Directory | How |
|---|---|
| [mcpservers.org](https://mcpservers.org/submit) | Submit form (backs wong2/awesome-mcp-servers) |
| [Glama](https://glama.ai/mcp) | Auto-indexes GitHub; claim the listing with your GitHub account |
| [PulseMCP](https://www.pulsemcp.com) | "Submit" button; hand-reviewed |
| [mcp.so](https://mcp.so) | Submit button / GitHub issue |

Also: [Smithery](https://smithery.ai) (optional hosted distribution).

## 3. awesome-mcp-servers PR

Open a PR to [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
under a fitting section (e.g. Search or Commerce/Marketplaces):

```markdown
- [jasp-nerd/marktplaats-mcp](https://github.com/jasp-nerd/marktplaats-mcp) 🐍 🏠 - Search Marktplaats & 2dehands (Dutch/Belgian classifieds): listings, sellers, categories and new-listing monitoring.
```

## 4. GitHub repo polish (one-time, manual)

- [ ] Upload the social preview: Settings → Social preview → 1280×640 PNG
      (generate from `assets/banner.svg`, or use
      `https://socialify.git.ci/jasp-nerd/marktplaats-mcp/image?description=1&language=1&name=1&owner=1&theme=Auto`)
- [ ] Enable Discussions (the issue template links to it)
- [ ] Enable private vulnerability reporting: Settings → Security
- [ ] Settings → General: enable "Sponsorships" only if wanted

## 5. Launch (concentrate for star velocity — Trending rewards bursts)

Post the same week, ideally the same day:

- Reddit: r/mcp, r/ClaudeAI, r/LocalLLaMA (angle: "I let Claude hunt bargains
  on Marktplaats for me")
- Hacker News: Show HN
- Dutch/Belgian dev communities: Tweakers forum, Lowlands dev Discords/Slacks
- X/LinkedIn with a short screen recording of a Claude search session

A demo GIF in the README measurably boosts conversion — record a 20-second
Claude Code session (`asciinema` or QuickTime) and add it under the Quickstart.

## 6. Ongoing

- Ship small releases often (freshness is a ranking factor for GitHub search
  and topic pages).
- Keep topics/description keyword-rich (already set via `gh repo edit`).
- Respond to issues quickly in the first weeks — early responsiveness converts
  users to stargazers and contributors.

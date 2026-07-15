# Security Policy

## Supported versions

Only the latest release of `marktplaats-mcp` receives security fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Use GitHub's private vulnerability reporting instead:
[Report a vulnerability](https://github.com/jasp-nerd/marktplaats-mcp/security/advisories/new).

You can expect an initial response within a week. Once a fix is released,
the report will be credited (unless you prefer otherwise).

## Scope notes

- This server makes read-only requests to public Marktplaats/2dehands
  endpoints and requires no credentials, so there are no secrets to leak
  by design. Reports about prompt-injection hardening (listing content is
  attacker-controlled text) are very welcome.

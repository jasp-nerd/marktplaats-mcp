# How marktplaats-mcp compares

[← README](../README.md)

| | **marktplaats-mcp** (this) | [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) | [gjoris/marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) |
|---|:---:|:---:|:---:|
| Marktplaats.nl | ✅ | ✅ | ✅ |
| 2dehands.be (Belgium), with language filter | ✅ | ❌ | ✅ |
| Subcategory filter that actually applies | ✅ | ❌ | ❌ |
| Category attribute filters (brand, mileage, RAM, ...) by label | ✅ | ids only | ids only |
| Price statistics, seller listings, spelling suggestions | ✅ | ❌ | ❌ |
| Listing details with status, exact time, bids, seller response rate | ✅ | partial | partial |
| Account: messages, favorites, bids, own ads | read + write | ❌ | read-only |
| Login without password (browser session import) | ✅ | n/a | Playwright login |
| New-listing monitoring | ✅ | ❌ | saved searches on disk |
| Paid promotions filtered by default | ✅ | ❌ | ❌ |
| Install | `uvx marktplaats-mcp` (PyPI) | `uvx git+https://…` (broken on current `mcp`) | from source |
| Hosted endpoint, no install | ✅ | ❌ | ❌ |
| Official MCP registry | ✅ | ❌ | ❌ |
| Daily live-API canary | ✅ | ❌ | ✅ |
| Last release | current | Feb 2026 | May 2026 |

Credit where it is due: PonClick's server came first and its listing formatting informed this one, and gjoris pioneered the embedded-page parsing and the live canary. See [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

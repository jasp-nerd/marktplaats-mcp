# Hoe marktplaats-mcp zich verhoudt tot andere servers

[← README](../README.nl.md)

| | **marktplaats-mcp** (deze) | [PonClick/marktplaats-mcp](https://github.com/PonClick/marktplaats-mcp) | [gjoris/marktplaats-2dehands-mcp](https://github.com/gjoris/marktplaats-2dehands-mcp) |
|---|:---:|:---:|:---:|
| Marktplaats.nl | ✅ | ✅ | ✅ |
| 2dehands.be (België), met taalfilter | ✅ | ❌ | ✅ |
| Subcategoriefilter dat echt wordt toegepast | ✅ | ❌ | ❌ |
| Filters op categoriekenmerken (merk, kilometerstand, RAM, ...) op label | ✅ | alleen id's | alleen id's |
| Prijsstatistieken, advertenties per verkoper, spellingsuggesties | ✅ | ❌ | ❌ |
| Advertentiedetails met status, exacte tijd, biedingen, reactiesnelheid verkoper | ✅ | deels | deels |
| Account: berichten, favorieten, biedingen, eigen advertenties | lezen + schrijven | ❌ | alleen lezen |
| Inloggen zonder wachtwoord (browsersessie importeren) | ✅ | n.v.t. | login via Playwright |
| Monitoring van nieuwe advertenties | ✅ | ❌ | opgeslagen zoekopdrachten op schijf |
| Betaalde promoties standaard weggefilterd | ✅ | ❌ | ❌ |
| Installatie | `uvx marktplaats-mcp` (PyPI) | `uvx git+https://…` (kapot op huidige `mcp`) | vanaf de broncode |
| Gehost endpoint, zonder installatie | ✅ | ❌ | ❌ |
| Officieel MCP-register | ✅ | ❌ | ❌ |
| Dagelijkse canary op de live API | ✅ | ❌ | ✅ |
| Laatste release | actueel | feb 2026 | mei 2026 |

Eer wie eer toekomt: de server van PonClick was er als eerste en de opmaak van advertenties daar heeft deze server beïnvloed, en gjoris was de eerste met het parsen van de ingebedde pagina en de live canary. Zie [THIRD_PARTY_NOTICES.md](https://github.com/jasp-nerd/marktplaats-mcp/blob/main/THIRD_PARTY_NOTICES.md).

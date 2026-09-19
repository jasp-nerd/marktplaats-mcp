# Comparaison de marktplaats-mcp avec les autres serveurs

[← README](../README.fr.md)

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

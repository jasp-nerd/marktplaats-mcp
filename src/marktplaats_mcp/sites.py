"""Site registry: marktplaats.nl (NL) and 2dehands.be (BE) share one Adevinta API."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Site:
    key: str
    host: str
    link_host: str

    @property
    def base_url(self) -> str:
        return f"https://{self.host}"

    @property
    def search_url(self) -> str:
        return f"https://{self.host}/lrp/api/search"

    def seller_url(self, seller_id: int) -> str:
        return f"https://{self.host}/v/api/seller-profile/{seller_id}"

    def listing_url(self, item_id: str) -> str:
        return f"https://{self.link_host}/{item_id}"


SITES: dict[str, Site] = {
    "marktplaats": Site("marktplaats", "www.marktplaats.nl", "link.marktplaats.nl"),
    "2dehands": Site("2dehands", "www.2dehands.be", "link.2dehands.be"),
}


def resolve_site(key: str) -> Site:
    site = SITES.get(key.strip().lower())
    if site is None:
        valid = ", ".join(sorted(SITES))
        raise ValueError(f"Unknown site {key!r}. Valid sites: {valid}.")
    return site

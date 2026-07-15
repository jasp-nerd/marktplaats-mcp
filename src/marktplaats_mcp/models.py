"""Pydantic models for tool output. Serialized with exclude_none for token efficiency."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Price(BaseModel):
    euros: float | None = None
    type: str = "UNKNOWN"
    label: str = ""


class Location(BaseModel):
    city: str | None = None
    country: str | None = None
    distance_km: float | None = None


class Seller(BaseModel):
    id: int | None = None
    name: str | None = None
    is_verified: bool | None = None


class Listing(BaseModel):
    id: str
    title: str
    price: str
    url: str
    listed: str | None = None
    city: str | None = None
    description: str | None = None
    distance_km: float | None = None
    seller: Seller | None = None
    image_urls: list[str] | None = None
    attributes: dict[str, str] | None = None
    category_id: int | None = None
    is_sponsored: bool | None = None


class SearchResult(BaseModel):
    site: str
    total_count: int
    offset: int
    limit: int
    returned: int
    listings: list[Listing]
    note: str | None = None


class SellerProfile(BaseModel):
    seller_id: int
    site: str
    bank_account_verified: bool | None = None
    identification_verified: bool | None = None
    phone_number_verified: bool | None = None
    average_score: float | None = None
    number_of_reviews: int | None = None


class ListingDetails(BaseModel):
    id: str
    site: str
    url: str
    title: str | None = None
    description: str | None = None
    price: str | None = None
    city: str | None = None
    view_count: int | None = None
    favorited_count: int | None = None
    since: str | None = None
    seller: Seller | None = None
    image_urls: list[str] | None = None
    attributes: dict[str, str] | None = None


class NewListingsResult(BaseModel):
    site: str
    since: str
    cursor: str
    new_count: int
    listings: list[Listing]
    note: str | None = None


def dump(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(exclude_none=True)

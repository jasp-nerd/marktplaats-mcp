"""Pydantic models for tool output. Serialized with exclude_none for token efficiency."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class Seller(BaseModel):
    id: int | None = None
    name: str | None = None
    is_verified: bool | None = None


class Listing(BaseModel):
    id: str
    title: str
    price: str
    price_euros: float | None = None
    url: str
    listed: str | None = None
    city: str | None = None
    distance_km: float | None = None
    reserved: bool | None = None
    is_business: bool | None = None
    is_sponsored: bool | None = None
    description: str | None = None
    seller: Seller | None = None
    image_urls: list[str] | None = None
    attributes: dict[str, str] | None = None
    category_id: int | None = None


class SearchResult(BaseModel):
    site: str
    total_count: int
    offset: int
    limit: int
    returned: int
    next_offset: int | None = None
    suggested_query: str | None = None
    listings: list[Listing]
    note: str | None = None


class SellerProfile(BaseModel):
    seller_id: int
    site: str
    bank_account_verified: bool | None = None
    identification_verified: bool | None = None
    phone_number_verified: bool | None = None
    business_verified: bool | None = None
    payment_method: str | None = None
    average_score: float | None = None
    number_of_reviews: int | None = None
    low_bid_threshold_percent: int | None = None


class SellerDetails(BaseModel):
    id: int | None = None
    name: str | None = None
    type: str | None = None
    active_since: str | None = None
    response_rate_percent: int | None = None
    response_label: str | None = None
    average_score: float | None = None
    number_of_reviews: int | None = None
    listings_count: int | None = None


class Bidding(BaseModel):
    enabled: bool
    minimum_bid_euros: float | None = None
    bids_count: int | None = None
    highest_bid_euros: float | None = None


class ListingDetails(BaseModel):
    id: str
    site: str
    url: str
    title: str | None = None
    description: str | None = None
    price: str | None = None
    price_euros: float | None = None
    price_type: str | None = None
    status: str | None = None
    listed_at: str | None = None
    since: str | None = None
    category_id: int | None = None
    city: str | None = None
    postcode: str | None = None
    country: str | None = None
    view_count: int | None = None
    favorited_count: int | None = None
    reserved: bool | None = None
    shippable: bool | None = None
    buy_it_now: bool | None = None
    bidding: Bidding | None = None
    attributes: dict[str, str] | None = None
    car_attributes: dict[str, str] | None = None
    image_count: int | None = None
    image_urls: list[str] | None = None
    seller: Seller | SellerDetails | None = None


class NewListingsResult(BaseModel):
    site: str
    since: str
    cursor: str
    new_count: int
    truncated: bool | None = None
    listings: list[Listing]
    note: str | None = None


class FilterOption(BaseModel):
    label: str
    id: int
    count: int | None = None


class SearchFilter(BaseModel):
    key: str
    label: str
    type: Literal["choice", "range"]
    options: list[FilterOption] = []
    min: int | None = None
    max: int | None = None
    unit: str | None = None


class FiltersResult(BaseModel):
    site: str
    category: str | None = None
    subcategory: str | None = None
    query: str | None = None
    filters: list[SearchFilter]
    note: str | None = None


class PriceStats(BaseModel):
    site: str
    query: str
    total_count: int
    sample_size: int
    min: float | None = None
    p25: float | None = None
    median: float | None = None
    p75: float | None = None
    max: float | None = None
    mean: float | None = None
    cheapest: list[Listing] = []
    note: str | None = None


def dump(model: BaseModel, exclude_none: bool = True) -> dict[str, Any]:
    return model.model_dump(exclude_none=exclude_none)

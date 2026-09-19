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


class Category(BaseModel):
    id: int
    name: str
    parent: str | None = None


class CategoriesResult(BaseModel):
    level: Literal["L1", "L2"]
    parent: str | None = None
    categories: list[Category]


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
    delivery: Literal["pickup", "shipping", "both"] | None = None
    buy_it_now: bool | None = None
    bidding: Bidding | None = None
    attributes: dict[str, str] | None = None
    car_attributes: dict[str, str] | None = None
    image_count: int | None = None
    image_urls: list[str] | None = None
    seller: Seller | SellerDetails | None = None
    note: str | None = None


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
    excluded_outliers: int | None = None
    min: float | None = None
    p25: float | None = None
    median: float | None = None
    p75: float | None = None
    max: float | None = None
    mean: float | None = None
    cheapest: list[Listing] = []
    note: str | None = None


class AccountStatus(BaseModel):
    site: str
    logged_in: bool
    user_id: int | None = None
    user_name: str | None = None
    unread_messages: int | None = None
    unread_notifications: int | None = None
    writes_enabled: bool
    note: str | None = None


class Conversation(BaseModel):
    id: str
    listing_id: str | None = None
    title: str | None = None
    role: Literal["buyer", "seller"] | None = None
    other_party: str | None = None
    other_party_id: int | None = None
    last_message: str | None = None
    last_message_from: Literal["me", "them", "system"] | None = None
    last_message_at: str | None = None
    unread_count: int | None = None
    payment_status: str | None = None


class ConversationsResult(BaseModel):
    site: str
    offset: int
    returned: int
    conversations: list[Conversation]
    note: str | None = None


class Message(BaseModel):
    sender: Literal["me", "them", "system", "unknown"]
    text: str
    sent_at: str | None = None
    read: bool | None = None
    type: str | None = None
    offer_euros: float | None = None
    offer_status: str | None = None


class ConversationDetail(BaseModel):
    site: str
    conversation_id: str
    other_party: str | None = None
    other_party_id: int | None = None
    total_count: int | None = None
    messages: list[Message]
    note: str | None = None


class MyListing(BaseModel):
    id: str
    title: str | None = None
    category: str | None = None
    price: str | None = None
    price_euros: float | None = None
    status: str | None = None
    url: str | None = None
    view_count: int | None = None
    favorited_count: int | None = None
    bidding_enabled: bool | None = None
    highest_bid_euros: float | None = None
    created_at: str | None = None
    expires_at: str | None = None
    expiring: bool | None = None
    reserved: bool | None = None


class MyListingsResult(BaseModel):
    site: str
    total_count: int | None = None
    batch: int
    returned: int
    listings: list[MyListing]
    note: str | None = None


class Favorite(BaseModel):
    id: str
    title: str | None = None
    price: str | None = None
    category: str | None = None
    url: str | None = None
    city: str | None = None
    seller: str | None = None
    available: bool | None = None
    highest_bid: str | None = None
    my_bid: str | None = None
    my_bid_is_highest: bool | None = None


class FavoritesResult(BaseModel):
    site: str
    batch: int
    returned: int
    more_available: bool | None = None
    favorites: list[Favorite]


class MyBid(BaseModel):
    listing_id: str
    title: str | None = None
    asking_price: str | None = None
    my_bid: str | None = None
    my_bid_euros: float | None = None
    highest_bid: str | None = None
    status: Literal["highest", "outbid", "unknown"] | None = None
    available: bool | None = None
    url: str | None = None


class MyBidsResult(BaseModel):
    site: str
    returned: int
    more_available: bool | None = None
    bids: list[MyBid]


class SavedSearch(BaseModel):
    id: str | None = None
    name: str | None = None
    type: str | None = None
    url: str | None = None
    email_alerts: bool | None = None
    push_alerts: bool | None = None
    new_ads_count: int | None = None
    created_at: str | None = None


class SavedSearchesResult(BaseModel):
    site: str
    returned: int
    saved_searches: list[SavedSearch]


class WriteReceipt(BaseModel):
    action: str
    site: str
    preview: bool
    target: dict[str, Any]
    success: bool | None = None
    note: str | None = None


def dump(model: BaseModel, exclude_none: bool = True) -> dict[str, Any]:
    return model.model_dump(exclude_none=exclude_none)

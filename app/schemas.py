import re
from datetime import date

from pydantic import BaseModel, field_validator, ConfigDict


ISBN10_PATTERN = r"^\d{9}[\dXx]$"
ISBN13_PATTERN = r"^\d{13}$"


def _normalize_isbn(value: str) -> str:
    return value.replace("-", "").replace(" ", "").strip()


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: date
    genre: str
    price: float
    copies_available: int = 0

    @field_validator("title", "author", "genre")
    @classmethod
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        cleaned = _normalize_isbn(v)
        if re.match(ISBN10_PATTERN, cleaned) or re.match(ISBN13_PATTERN, cleaned):
            return cleaned
        raise ValueError("isbn must be a valid ISBN-10 or ISBN-13")

    @field_validator("published_date")
    @classmethod
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("published_date cannot be in the future")
        return v

    @field_validator("price")
    @classmethod
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be a positive number")
        return v

    @field_validator("copies_available")
    @classmethod
    def copies_not_negative(cls, v):
        if v < 0:
            raise ValueError("copies_available cannot be negative")
        return v


# FIX #2: Removed total_revenue computed field from BookOut.
# The assignment defines total_revenue as a global aggregate returned
# only from GET /books/revenue, not a per-book field.
class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_date: date
    genre: str
    price: float
    copies_available: int
    copies_sold: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("genre", mode="before")
    @classmethod
    def genre_name_only(cls, v):
        if hasattr(v, "name"):
            return v.name
        return v


class RevenueOut(BaseModel):
    total_revenue: float

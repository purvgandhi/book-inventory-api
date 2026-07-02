"""
Unit tests for the BookCreate validation rules.
These don't touch the database or the API layer at all — just the
Pydantic validators in app/schemas.py.
"""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas import BookCreate, BookOut


def make_book(**overrides):
    data = {
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "isbn": "9780321146533",
        "published_date": date(2002, 11, 18),
        "genre": "Non-Fiction",
        "price": 24.99,
        "copies_available": 5,
    }
    data.update(overrides)
    return BookCreate(**data)


# ---------------------------------------------------------------------------
# Basic happy path
# ---------------------------------------------------------------------------

def test_valid_book_passes():
    book = make_book()
    assert book.title == "Test Driven Development"
    assert book.isbn == "9780321146533"


# ---------------------------------------------------------------------------
# Title / Author / Genre validation
# ---------------------------------------------------------------------------

def test_empty_title_rejected():
    with pytest.raises(ValidationError):
        make_book(title="   ")


def test_empty_author_rejected():
    with pytest.raises(ValidationError):
        make_book(author="")


def test_empty_genre_rejected():
    with pytest.raises(ValidationError):
        make_book(genre="")


# ---------------------------------------------------------------------------
# Price validation
# ---------------------------------------------------------------------------

def test_negative_price_rejected():
    with pytest.raises(ValidationError):
        make_book(price=-5)


def test_zero_price_rejected():
    with pytest.raises(ValidationError):
        make_book(price=0)


def test_positive_price_accepted():
    book = make_book(price=0.01)
    assert book.price == 0.01


# ---------------------------------------------------------------------------
# Published date validation
# ---------------------------------------------------------------------------

def test_future_published_date_rejected():
    future_date = date.today() + timedelta(days=30)
    with pytest.raises(ValidationError):
        make_book(published_date=future_date)


def test_today_as_published_date_allowed():
    book = make_book(published_date=date.today())
    assert book.published_date == date.today()


def test_past_published_date_allowed():
    book = make_book(published_date=date(1990, 1, 1))
    assert book.published_date == date(1990, 1, 1)


# ---------------------------------------------------------------------------
# copies_available validation
# ---------------------------------------------------------------------------

def test_negative_copies_available_rejected():
    with pytest.raises(ValidationError):
        make_book(copies_available=-1)


def test_zero_copies_available_accepted():
    book = make_book(copies_available=0)
    assert book.copies_available == 0


# ---------------------------------------------------------------------------
# ISBN validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("isbn", [
    "9780321146533",        # valid ISBN-13 (13 digits)
    "978-0-321-14653-3",    # valid ISBN-13, hyphenated
    "0321146530",           # valid ISBN-10
    "1234567890123",        # 13 digits - valid length
])
def test_valid_isbn_formats_accepted(isbn):
    book = make_book(isbn=isbn)
    assert book.isbn.replace("-", "") == isbn.replace("-", "")


@pytest.mark.parametrize("isbn", [
    "12345",            # too short
    "97803211465",      # 11 digits - not valid
    "abcdefghij",       # not numeric
])
def test_invalid_isbn_formats_rejected(isbn):
    with pytest.raises(ValidationError):
        make_book(isbn=isbn)


# ---------------------------------------------------------------------------
# FIX #2 verification: BookOut should NOT have total_revenue field
# ---------------------------------------------------------------------------

def test_book_out_has_no_total_revenue_field():
    """total_revenue is a global aggregate (GET /books/revenue), not per-book."""
    fields = BookOut.model_fields.keys()
    assert "total_revenue" not in fields

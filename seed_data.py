"""
Adds sample genres and books to the database.

Run:
python seed_data.py
"""

from datetime import date

from app.database import Base, SessionLocal, engine
from app import models

Base.metadata.create_all(bind=engine)

GENRES = [
    "Programming",
    "Database",
    "Software Engineering",
    "Fiction",
]

BOOKS = [
    {
        "title": "Python Basics",
        "author": "John Miller",
        "isbn": "9781234567890",
        "published_date": date(2022, 5, 10),
        "genre": "Programming",
        "price": 499,
        "copies_available": 10,
        "copies_sold": 4,
    },
    {
        "title": "Java Fundamentals",
        "author": "David Brown",
        "isbn": "9781234567891",
        "published_date": date(2021, 8, 15),
        "genre": "Programming",
        "price": 599,
        "copies_available": 12,
        "copies_sold": 6,
    },
    {
        "title": "Learning SQL",
        "author": "Michael Lee",
        "isbn": "9781234567892",
        "published_date": date(2020, 3, 20),
        "genre": "Database",
        "price": 699,
        "copies_available": 8,
        "copies_sold": 3,
    },
    {
        "title": "Database Concepts",
        "author": "Sarah Wilson",
        "isbn": "9781234567893",
        "published_date": date(2019, 11, 18),
        "genre": "Database",
        "price": 649,
        "copies_available": 9,
        "copies_sold": 5,
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "published_date": date(2008, 8, 1),
        "genre": "Software Engineering",
        "price": 899,
        "copies_available": 7,
        "copies_sold": 10,
    },
    {
        "title": "Software Design",
        "author": "Kevin Thomas",
        "isbn": "9781234567894",
        "published_date": date(2023, 1, 5),
        "genre": "Software Engineering",
        "price": 749,
        "copies_available": 11,
        "copies_sold": 2,
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "isbn": "9780061122415",
        "published_date": date(1988, 4, 1),
        "genre": "Fiction",
        "price": 399,
        "copies_available": 15,
        "copies_sold": 8,
    },
    {
        "title": "Think and Grow Rich",
        "author": "Napoleon Hill",
        "isbn": "9781585424337",
        "published_date": date(1937, 1, 1),
        "genre": "Fiction",
        "price": 450,
        "copies_available": 13,
        "copies_sold": 7,
    },
]


def seed():
    db = SessionLocal()

    try:
        genre_lookup = {}

        for name in GENRES:
            genre = db.query(models.Genre).filter(
                models.Genre.name == name
            ).first()

            if not genre:
                genre = models.Genre(name=name)
                db.add(genre)
                db.commit()
                db.refresh(genre)

            genre_lookup[name] = genre.id

        added = 0

        for item in BOOKS:
            existing = db.query(models.Book).filter(
                models.Book.isbn == item["isbn"]
            ).first()

            if existing:
                continue

            book = models.Book(
                title=item["title"],
                author=item["author"],
                isbn=item["isbn"],
                published_date=item["published_date"],
                genre_id=genre_lookup[item["genre"]],
                price=item["price"],
                copies_available=item["copies_available"],
                copies_sold=item["copies_sold"],
            )

            db.add(book)
            added += 1

        db.commit()
        print(f"Added {added} books successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
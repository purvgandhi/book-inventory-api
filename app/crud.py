from sqlalchemy.orm import Session

from app import models, schemas


# ---------------------------------------------------------------------------
# Genre
#
# Genres are resolved on the fly: if the name already exists it's reused,
# otherwise it's created. This keeps referential integrity intact without
# needing a separate genre management API.
# ---------------------------------------------------------------------------

def get_or_create_genre(db: Session, name: str) -> models.Genre:
    genre = db.query(models.Genre).filter(models.Genre.name.ilike(name)).first()
    if genre:
        return genre

    genre = models.Genre(name=name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


# ---------------------------------------------------------------------------
# Book
# ---------------------------------------------------------------------------

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str, exclude_id: int = None):
    query = db.query(models.Book).filter(models.Book.isbn == isbn)
    if exclude_id is not None:
        query = query.filter(models.Book.id != exclude_id)
    return query.first()


def create_book(db: Session, book: schemas.BookCreate):
    genre = get_or_create_genre(db, book.genre)
    data = book.model_dump(exclude={"genre"})
    new_book = models.Book(**data, genre_id=genre.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def update_book(db: Session, book: models.Book, data: schemas.BookCreate):
    genre = get_or_create_genre(db, data.genre)
    for field, value in data.model_dump(exclude={"genre"}).items():
        setattr(book, field, value)
    book.genre_id = genre.id
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: models.Book):
    db.delete(book)
    db.commit()


def search_books(
    db: Session,
    author: str = None,
    title: str = None,
    genre: str = None,
    min_price: float = None,
    max_price: float = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(models.Book)

    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    # FIX #3: Genre search now uses partial match (ilike with wildcards)
    # consistent with title and author search behaviour.
    if genre:
        query = query.join(models.Genre).filter(models.Genre.name.ilike(f"%{genre}%"))

    if min_price is not None:
        query = query.filter(models.Book.price >= min_price)

    if max_price is not None:
        query = query.filter(models.Book.price <= max_price)

    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    return query.offset((page - 1) * limit).limit(limit).all()


def sell_book(db: Session, book: models.Book):
    book.copies_available -= 1
    book.copies_sold += 1
    db.commit()
    db.refresh(book)
    return book


def get_total_revenue(db: Session):
    books = db.query(models.Book).all()
    return round(sum(b.price * b.copies_sold for b in books), 2)

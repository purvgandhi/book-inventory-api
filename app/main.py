import os

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Inventory Microservice",
    description="A small REST API for managing a book inventory, "
                 "built as part of an internship assignment.",
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = [
        {"field": ".".join(str(p) for p in err["loc"] if p != "body"), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(status_code=400, content={"detail": errors})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


@app.get("/")
def home():
    return {"message": "Book Inventory API is running"}


@app.post("/books", response_model=schemas.BookOut, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.get_book_by_isbn(db, book.isbn):
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists")

    try:
        return crud.create_book(db, book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists")


@app.get("/books", response_model=list[schemas.BookOut])
def list_books(
    author: str | None = None,
    title: str | None = None,
    genre: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.search_books(
        db,
        author=author,
        title=title,
        genre=genre,
        min_price=min_price,
        max_price=max_price,
        page=page,
        limit=limit,
    )


# FIX #1: /books/revenue must be defined BEFORE /books/{book_id}
# otherwise FastAPI matches "revenue" as a book_id and returns 422.
@app.get("/books/revenue", response_model=schemas.RevenueOut)
def get_revenue(db: Session = Depends(get_db)):
    total = crud.get_total_revenue(db)
    return schemas.RevenueOut(total_revenue=total)


@app.get("/books/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, data: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if crud.get_book_by_isbn(db, data.isbn, exclude_id=book_id):
        raise HTTPException(status_code=409, detail="Another book already uses this ISBN")

    try:
        return crud.update_book(db, book, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Another book already uses this ISBN")


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return None


@app.post("/books/{book_id}/sell", response_model=schemas.BookOut)
def sell_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.copies_available <= 0:
        raise HTTPException(status_code=400, detail="No copies available to sell")

    return crud.sell_book(db, book)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

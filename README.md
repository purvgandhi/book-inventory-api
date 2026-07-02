# Book Inventory Management API

A REST API built using FastAPI to manage a book inventory. It allows users to create, update, delete, search, and sell books while tracking total revenue.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic v2
- Pytest

## Project Structure

```
book_inv/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── tests/
├── requirements.txt
├── README.md
└── ...
```

## Setup

### 1. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## Running Tests

```bash
pytest
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/books` | Create a new book |
| GET | `/books` | List/Search books |
| GET | `/books/revenue` | Get total revenue |
| GET | `/books/{id}` | Get a book by ID |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
| POST | `/books/{id}/sell` | Sell one copy of a book |

## Query Parameters

`GET /books` supports the following filters:

| Parameter | Description |
|-----------|-------------|
| `title` | Filter by title |
| `author` | Filter by author |
| `genre` | Filter by genre |
| `min_price` | Minimum price |
| `max_price` | Maximum price |
| `page` | Page number |
| `limit` | Number of records per page |

## Validation Rules

- Title and author cannot be empty.
- Genre cannot be empty.
- ISBN must be a valid ISBN-10 or ISBN-13.
- Published date cannot be in the future.
- Price must be greater than zero.
- Copies available cannot be negative.

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request |
| 404 | Book Not Found |
| 409 | Duplicate ISBN |
| 500 | Internal Server Error |

## API Documentation

Interactive API documentation is available through Swagger UI:

http://127.0.0.1:8000/docs
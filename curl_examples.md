# Curl Examples — Book Inventory API

Base URL: `http://127.0.0.1:8000`

---

## Health Check

```bash
curl http://127.0.0.1:8000/
```

---

## Create a Book

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "isbn": "9780135957059",
    "published_date": "1999-10-20",
    "genre": "Technology",
    "price": 49.99,
    "copies_available": 10
  }'
```

**Success response (201):**
```json
{
  "id": 1,
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt",
  "isbn": "9780135957059",
  "published_date": "1999-10-20",
  "genre": "Technology",
  "price": 49.99,
  "copies_available": 10,
  "copies_sold": 0
}
```

**Duplicate ISBN response (409):**
```json
{ "detail": "A book with this ISBN already exists" }
```

---

## Get a Book by ID

```bash
curl http://127.0.0.1:8000/books/1
```

**Not found response (404):**
```json
{ "detail": "Book not found" }
```

---

## Update a Book

```bash
curl -X PUT http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Pragmatic Programmer (20th Anniversary Edition)",
    "author": "Andrew Hunt",
    "isbn": "9780135957059",
    "published_date": "2019-09-13",
    "genre": "Technology",
    "price": 54.99,
    "copies_available": 15
  }'
```

---

## Delete a Book

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

**Success:** HTTP 204 No Content

---

## List & Search Books

```bash
# All books (paginated)
curl "http://127.0.0.1:8000/books?page=1&limit=10"

# Search by title (partial match)
curl "http://127.0.0.1:8000/books?title=pragmatic"

# Search by author (partial match)
curl "http://127.0.0.1:8000/books?author=hunt"

# Filter by genre (partial match)
curl "http://127.0.0.1:8000/books?genre=tech"

# Filter by price range
curl "http://127.0.0.1:8000/books?min_price=10&max_price=50"

# Combined search
curl "http://127.0.0.1:8000/books?author=hunt&genre=tech&min_price=20&page=1&limit=5"
```

---

## Sell a Book

```bash
curl -X POST http://127.0.0.1:8000/books/1/sell
```

**Success response (200):** Returns updated book with decremented `copies_available` and incremented `copies_sold`.

**No stock response (400):**
```json
{ "detail": "No copies available to sell" }
```

---

## Total Revenue

```bash
curl http://127.0.0.1:8000/books/revenue
```

**Success response (200):**
```json
{ "total_revenue": 149.97 }
```

---

## Validation Error Examples

```bash
# Empty title → 400
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "  ", "author": "Someone", "isbn": "9780135957059", "published_date": "2020-01-01", "genre": "Fiction", "price": 9.99}'

# Future date → 400
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Future Book", "author": "Someone", "isbn": "9780135957058", "published_date": "2099-01-01", "genre": "Fiction", "price": 9.99}'

# Invalid ISBN → 400
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Bad ISBN", "author": "Someone", "isbn": "12345", "published_date": "2020-01-01", "genre": "Fiction", "price": 9.99}'

# Negative price → 400
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Cheap Book", "author": "Someone", "isbn": "9780135957057", "published_date": "2020-01-01", "genre": "Fiction", "price": -5}'
```

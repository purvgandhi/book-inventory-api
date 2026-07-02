from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    isbn = Column(String, unique=True, nullable=False, index=True)

    published_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)

    copies_available = Column(Integer, default=0, nullable=False)
    copies_sold = Column(Integer, default=0, nullable=False)

    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre", back_populates="books")

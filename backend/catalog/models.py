from sqlalchemy import String, ForeignKey, Table, Column, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseModel


books_genres = Table(
    "books_genres",
    BaseModel.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(256), unique=True)

    books = relationship("BookModel", back_populates="category")

class GenreModel(BaseModel):
    __tablename__ = 'genres'

    name: Mapped[str] = mapped_column(String(256), unique=True)

    books = relationship("BookModel", secondary=books_genres, back_populates="genres")

class AuthorModel(BaseModel):
    __tablename__ = 'authors'

    name: Mapped[str] = mapped_column(String(256), unique=True)

    books = relationship("BookModel", back_populates="author")

class PublicationModel(BaseModel):
    __tablename__ = 'publications'

    name: Mapped[str] = mapped_column(String(256), unique=True)

    books = relationship("BookModel", back_populates="publication")

class BindingModel(BaseModel):
    __tablename__ = 'bindings'

    name: Mapped[str] = mapped_column(String(256), unique=True)

    books = relationship("BookModel", back_populates="binding")

class BookModel(BaseModel):
    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String(256))
    short_description: Mapped[str] = mapped_column(String(256))
    full_description: Mapped[str]
    category_id: Mapped[str] = mapped_column(ForeignKey('categories.id'))
    author_id: Mapped[str] = mapped_column(ForeignKey('authors.id'))
    price: Mapped[int]
    discount: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(server_default=text('True'))
    amount: Mapped[int]
    publication_id: Mapped[str] = mapped_column(ForeignKey('publications.id'))
    year_of_publication: Mapped[int]
    amount_pages: Mapped[int]
    binding_id: Mapped[str] = mapped_column(ForeignKey('bindings.id'))
    isbn: Mapped[str]
    size: Mapped[str]
    weight: Mapped[float]

    category = relationship("CategoryModel", back_populates="books")
    author = relationship("AuthorModel", back_populates="books")
    publication = relationship("PublicationModel", back_populates="books")
    binding = relationship("BindingModel", back_populates="books")

    genres = relationship("GenreModel", secondary=books_genres, back_populates="books")
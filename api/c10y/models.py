"""Database models."""

from sqlalchemy.orm import DeclarativeBase, Mapped, String, mapped_column


class BaseModel(DeclarativeBase):
    """Base class for all declarative database models.
    
    See: https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models

    Column types and nullability are derived from the type annotations:
    https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation
    """


class Constituent(BaseModel):
    """An elected official's constituent."""

    __tablename__ = "constituent"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(String(12))
    street_address_1: Mapped[str] = mapped_column()
    street_address_2: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column(String(2))
    zip_code: Mapped[str] = mapped_column(String(5))

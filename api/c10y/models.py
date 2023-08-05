"""Database models."""

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base class for all declarative database models.
    
    See: https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models

    Column types and nullability are derived from the type annotations:
    https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation
    """


class Constituent(BaseModel):
    """An elected official's constituent."""

    __tablename__ = "constituent"
    
    # Compound constraint to ensure uniqueness
    __table_args__ = (
        # TODO: Consider adding additional fields to this constraint? I picked these fields
        # since the combination seems "good enough" to ensure uniqueness within a constituency
        UniqueConstraint("first_name", "last_name", "email", "zip_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Store in all uppercase to avoid case sensitivity issues
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    # TODO: should email be unique? Consider case where two constituents share the same email
    # address, for example if you have a married couple with a shared family email address
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column(String(12))
    street_address_1: Mapped[str] = mapped_column()
    street_address_2: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column(String(2))
    zip_code: Mapped[str] = mapped_column(String(5))

    def __repr__(self) -> str:
        return f"Constituent({self.first_name}, {self.last_name}, {self.email}, {self.zip_code})"

"""Database models."""

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Base class for all declarative database models.
    
    See: https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models

    Column types and nullability are derived from the type annotations:
    https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation
    """

"""Constituency API service methods."""

from . import db, models

from sqlalchemy import select


def list_constituents() -> list[models.Constituent]:
    """List all constituents currently in the database, sorted alphabetically."""
    
    # TODO: Implement params to filter, sort, limit results
    with db.session() as db_session:
        stmt = select(models.Constituent).order_by(
            models.Constituent.last_name, models.Constituent.first_name
        )
        constituent_list = db_session.scalars(stmt).all()

    return constituent_list

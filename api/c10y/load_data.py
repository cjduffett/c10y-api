"""Scripts to load challenge data during app startup."""

from csv import DictReader
from pathlib import Path

from . import db, models

CSV_FIELDNAMES = [
    "first_name",
    "last_name",
    "email",
    "phone_number",
    "street_address_1",
    "street_address_2",
    "city",
    "state",
    "zip_code"
]


def existing_constituents() -> int:
    """Load existing constituent data."""

    csv_path = Path("data/existing_constituent_data.csv")
    existing_constituents: list[models.Constituent] = []

    with csv_path.open("r") as f:
        reader = DictReader(f, fieldnames=CSV_FIELDNAMES)

        # Skip header row
        next(reader)

        for row in reader:
            constituent = models.Constituent(
                first_name=row["first_name"].upper(),
                last_name=row["last_name"].upper(),
                email=row["email"].upper(),
                phone_number=row["phone_number"],
                street_address_1=row["street_address_1"],
                street_address_2=row["street_address_2"],  # May be blank
                city=row["city"],
                state=row["state"],
                zip_code=row["zip_code"],
            )
            existing_constituents.append(constituent)

    # Bulk load data
    with db.session() as db_session:
        db_session.add_all(existing_constituents)
        db_session.commit()

    # Return total number of records loaded
    return len(existing_constituents)


"""Scripts to load challenge data during app startup."""

from csv import DictReader
from pathlib import Path
from typing import Tuple

from sqlalchemy.exc import DataError, IntegrityError

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

# Type alias
ConstituentList = list[models.Constituent]


def existing_constituents() -> int:
    """Load existing constituent data."""

    csv_path = Path("data/existing_constituent_data.csv")
    existing = _parse_constituent_file(csv_path)

    # Bulk load data
    with db.session() as db_session:
        db_session.add_all(existing)
        db_session.commit()

    # Return total number of records loaded
    return len(existing)


def updated_constituents() -> Tuple[int, ConstituentList]:
    """Load and merge updated constituent data."""

    csv_path = Path("data/1776_07_04_town_hall.csv")
    updates = _parse_constituent_file(csv_path)
    dupes: ConstituentList = []
    
    with db.session() as db_session:
        for constituent in updates:
            try:
                with db_session.begin_nested():
                    db_session.add(constituent)
            except IntegrityError:
                # Duplicate found, skip update for now. TODO: Evaluate returned 'dupes' to see if
                # there were any false positives, false negatives.
                print(f"Duplicate: {constituent}")
                dupes.append(constituent)
            except DataError as exc:
                # Not a duplicate but something wrong with the data, for example a malformed
                # phone number, state, postal code, etc. TODO: Implement better data cleaning
                # and error handling so we can weed out malformed data but still update other
                # fields for the existing record.
                print(f"Malformed: {constituent}\n{exc._message()}")

        # Commit all updates that didn't cause IntegrityErrors or DataErrors
        db_session.commit()
            
    return len(updates) - len(dupes), dupes   


def _parse_constituent_file(csv_path: Path) -> ConstituentList:
    """Parse a constituent CSV file."""

    constituent_list: ConstituentList = [] 

    with csv_path.open("r") as f:
        reader = DictReader(f, fieldnames=CSV_FIELDNAMES)

        # Skip header row
        next(reader)

        for row in reader:
            constituent = _build_constituent(row)
            constituent_list.append(constituent)
        
    return constituent_list


def _build_constituent(row: dict) -> models.Constituent:
    """Populate a Constituent model from a parsed CSV row."""

    return models.Constituent(
        first_name=row["first_name"].upper(),
        last_name=row["last_name"].upper(),
        email=row["email"].upper(),
        phone_number=row["phone_number"],  # TODO: Format as E.164 phone number
        street_address_1=row["street_address_1"],
        street_address_2=row["street_address_2"],  # May be blank
        city=row["city"],
        state=row["state"],
        zip_code=row["zip_code"],  # TODO: Truncate to first 5 digits?
    )

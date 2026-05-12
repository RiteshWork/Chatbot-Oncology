"""
scripts/check_db.py
Day 1 sanity check. Run with:

    poetry run python -m scripts.check_db

Connects to Postgres, creates any missing tables, lists what exists.
"""

from __future__ import annotations

from sqlalchemy import inspect, text

# Importing the model modules has the side effect of registering each
# model class on Base.metadata. Without these imports, create_all has
# nothing to create. (Linters will flag them as unused — that's fine.)
from db import Base, engine                           # noqa: F401
from library import models as _library_models         # noqa: F401
from states import models as _states_models           # noqa: F401
from processes import models as _processes_models     # noqa: F401
from sessions import models as _sessions_models       # noqa: F401


def main() -> None:
    print(f"Connecting with: {engine.url!r}")

    # Step 1: prove we can connect.
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar_one()
        print(f"Connected. Postgres reports: {version}")

    # Step 2: create any missing tables.
    print("Running Base.metadata.create_all() ...")
    Base.metadata.create_all(engine)
    print("create_all done.")

    # Step 3: list what's there now.
    inspector = inspect(engine)
    tables = sorted(inspector.get_table_names())
    print("\nTables currently in the database:")
    for t in tables:
        print(f"  - {t}")

    expected = {"library_items", "states", "processes", "sessions"}
    missing = expected - set(tables)
    if missing:
        print(f"\nWARNING: expected tables not found: {sorted(missing)}")
    else:
        print("\nAll Day 1 tables present.")


if __name__ == "__main__":
    main()
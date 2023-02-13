import sqlite3
from sqlite3 import Error
import pathlib


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """ create a database connection to a SQLite database """
    ROOT = pathlib.Path(__file__).resolve()
    DATABASE_FILENAME = ROOT/'var'/'calpal.sqlite3'

    db = sqlite3.connect(str(DATABASE_FILENAME))
    db.row_factory = dict_factory
    db.execute("PRAGMA foreign_keys = ON")

    return db

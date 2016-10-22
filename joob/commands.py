import argparse

from joob.rhyme_dictionary import build_database


def build_dict():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    parser.add_argument("--trim",
                        help="Trim level for generating rhyme phonemes",
                        type=int)
    args = parser.parse_args()

    # Get arguments or set to defaults
    database = args.db or "db.sqlite3"
    trim = args.trim or 2

    # Build database
    print("Building database %s" % database)
    build_database(database, trim)

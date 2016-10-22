import argparse

from joob.rhyme_dictionary import build_database


DEFAULT_DATABASE = "db.sqlite3"


def build_dict():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    parser.add_argument("--trim",
                        help="Trim level for generating rhyme phonemes",
                        type=int)

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    trim = args.trim or 2

    # Build database
    print("Building database %s" % database)
    build_database(database, trim)


def generate_song():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    parser.add_argument("file", help="Output file")

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    filename = args.file
    print("Generating a song...")


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    parser.add_argument("dir", help="Input directory")

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    directory = args.dir
    print("Training...")

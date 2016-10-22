import argparse

from joob.rhyme_dictionary import (
    build_database, connect_to_database, RhymeDictionary
)


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

    # Connect to the database
    session = connect_to_database(database)
    rhyme_dict = RhymeDictionary(session, 2)

    print("Generating a song...")
    with open(filename, "wb") as output_file:
        output_file.write(rhyme_dict.random_rhyme("lips"))


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    parser.add_argument("dir", help="Input directory")

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    directory = args.dir

    # Connect to the database
    session = connect_to_database(database)
    rhyme_dict = RhymeDictionary(session, 2)

    print("Training...")

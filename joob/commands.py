import argparse
import glob

from joob.rhyme_dictionary import (
    build_database, DatabaseExistsException, connect_to_database, RhymeDictionary
)
from joob.song_generator import SongGenerator

DEFAULT_DATABASE = "db.sqlite3"


def get_base_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", help="Filename for sqlite3 database")
    return parser


def build_dict():
    parser = get_base_parser()
    parser.add_argument("--trim",
                        help="Trim level for generating rhyme phonemes",
                        type=int)

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    trim = args.trim or 2

    # Build database
    print("Building database %s..." % database)
    try:
        build_database(database, trim)
    except DatabaseExistsException:
        print("Database already exists!")


def generate_song():
    parser = get_base_parser()
    parser.add_argument("file", help="Output file")

    song_gen = SongGenerator()

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    filename = args.file

    # Connect to the database
    session = connect_to_database(database)
    rhyme_dict = RhymeDictionary(session, 2)

    print("Generating a song...")
    with open(filename, "wb") as output_file:
        output_file.write(song_gen.generate(mock=True))


def train():
    parser = get_base_parser()
    parser.add_argument("dir", help="Input directory")

    # Get arguments or set to defaults
    args = parser.parse_args()
    database = args.db or DEFAULT_DATABASE
    directory = args.dir

    # Connect to the database
    session = connect_to_database(database)
    rhyme_dict = RhymeDictionary(session, 2)

    print("Training...")

    # Get all files within directory
    files = glob.glob("joob/%s/*" % directory)

    for filename in files:
        with open(filename, "rb") as training_file:
            for line in training_file.readlines():
                print(line.rstrip())

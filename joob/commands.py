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
    trim = args.trim or 0

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


def train_old():
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

    # Initialize song generator
    song_gen = SongGenerator()

    for filename in files:
        with open(filename, "rb") as training_file:
            for line in training_file.readlines():
                print(line.rstrip())

def train():
    parser = get_base_parser()
    parser.add_argument("pickle_file_path", help="Pickle file")
    parser.add_argument("--random", dest="random", action="store_true", default=False)

    args = parser.parse_args()

    print("Training...")

    song_gen = SongGenerator()
    if args.random:
        try:
            data = song_gen.get_initialized_array(start=1,end=100)
            print("Generating random pickle file {}: {}".format(args.pickle_file_path, data))
            song_gen.write_pickle_file(data, args.pickle_file_path)
        except Exception as e:
            print("Exception: {}".format(e))
    if not args.random:
        try:
            data = song_gen.read_pickle_file(args.pickle_file_path)
            print("Loading data from pickle_file: {}".format(args.pickle_file_path))
            print("Results: {}".format(data))
        except IOError:
            print("Error: File might not exist?")

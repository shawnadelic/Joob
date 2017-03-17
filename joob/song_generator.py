import pickle
import random
import string

import nltk
from nltk.tokenize import word_tokenize

import rhyme_dictionary


class Song:
    def __init__(self, title, songs):
        self.title = title
        self.songs = songs
        self.lines = list()

    def __repr__(self):
        return self.title


class SongGenerator:
    def __init__(self):
        self.songs = dict()
        self.data = None
        self.training_dimensions = (2, 3)
        filename = "001.txt"
        try:
            input_file = open("data/" + filename)
            title = input_file.readline().strip()
            song_buffer = Song(title, self.songs)
            for line in input_file:
                song_buffer.lines.append([
                    token for
                    token in word_tokenize(line)
                    if token not in string.punctuation])
                self.songs[title] = song_buffer
            print(self.songs[title])
        except:
            pass

        self.read_training_data()

    def train(self, pickle_file_path):
        print("RESULTS: {}".format(self.read_pickle_file(pickle_file_path)))

    def write_pickle_file(self, data, pickle_file_path):
        with open(pickle_file_path, "wb") as pickle_file:
            pickle.dump(data, pickle_file, pickle.HIGHEST_PROTOCOL)

    def read_pickle_file(self, pickle_file_path):
        with open(pickle_file_path, "r") as pickle_file:
            return pickle.load(pickle_file)

    def get_initialized_array(self, start=1, end=1):
        width, height = self.training_dimensions
        return [[random.randint(start, end) for _ in range(width)]
                for _ in range(height)]

    def initialize_training_file(self, training_file_path):
        self.data = self.get_initialized_array(start=1, end=1)
        self.write_pickle_file(self.data, training_file_path)

    def read_training_data(self):
        self.data = None
        training_file_path = "joob/training.pickle"
        try:
            self.data = self.read_pickle_file(training_file_path)
        except (EOFError, IOError):
            print("Couldn't find training file, generating file at {}".format(
                training_file_path))

        if self.data is None:
            self.initialize_training_file(training_file_path)
            print("Generated initial pickle file {}...".format(
                str(self.data)[:100]))
        else:
            print("Loaded {}...".format(str(self.data)[:100]))

    def generate(self, mock=True):
        if mock:
            return "TEST MOCK STRING"


def scan_song(lyric_file, rhyme_dict):
    nltk.download('punkt', quiet=True)
    end_words = []
    with open(lyric_file) as lyric_input:
        for line in lyric_input:
            if line:
                end_word = [
                    w.lower() for w in
                    nltk.word_tokenize(line) if w.isalpha()]
                if end_word:
                    end_words.append([
                        w.lower() for w in
                        nltk.word_tokenize(line) if w.isalpha()][-1])

    size = len(end_words)
    matrix = [[0 for i in range(size)] for j in range(size)]

    print end_words

    for row in range(size):
        for col in range(size):
            score = 0
            print "Before call"
            if (col >= row):
                score = rhyme_dict.rhyme_strength(
                    end_words[row], end_words[col])
            print "After call"
            matrix[col][row] = score
            print "%s" % score,
        print


if __name__ == "__main__":
    Session = rhyme_dictionary.connect_to_database('test2.db')
    rhyme_dict = rhyme_dictionary.RhymeDictionary(Session, 0)
    song_generator = SongGenerator()
    #scan_song("data/003.txt", rhyme_dict)

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

    def train(self, data):
        pass

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
    scan_song("data/003.txt", rhyme_dict)

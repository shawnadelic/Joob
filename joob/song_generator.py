import os
import string
import rhyme_dictionary
import nltk
from nltk.tokenize import word_tokenize

class Song:
    def __init__(self,title,songs):
        self.title = title
        self.songs = songs
        self.lines = list()
    def __repr__(self):
        return self.title

class SongGenerator:
    def __init__(self):
        self.songs = dict()
        ##for filename in os.listdir("data"):
        filename = "001.txt"
        try:
            input_file = open("data/" + filename)
            title = input_file.readline().strip()
            song_buffer = Song(title,self.songs)
            for line in input_file:
                song_buffer.lines.append([token for token in word_tokenize(line) if token not in string.punctuation])
                self.songs[title] = song_buffer
            print self.songs[title]
        except:
            pass

def scan_song(lyric_file):
    nltk.download('punkt', quiet=True)
    end_words = []
    with open(lyric_file) as lyric_input:
        song_title = lyric_input.readline()
        for line in lyric_input:
            if line:
                end_word = [w.lower() for w in
                        nltk.word_tokenize(line) if w.isalpha()]
                if end_word:
                    end_words.append([w.lower() for w in
                        nltk.word_tokenize(line) if w.isalpha()][-1])

    size = len(end_words)
    matrix = [[0 for i in range(size)] for j in range(size)]

    for row in range(size):
        for col in range(size):
            matrix[col][row] = row + col

    print matrix


if __name__ == "__main__":
    #rhymes = rhyme_dictionary.RhymeDictionary(db_file="test.db")
    song_generator = SongGenerator()
    scan_song("data/003.txt")
    scan_song("data/004.txt")

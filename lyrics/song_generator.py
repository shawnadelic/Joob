import os
import string
import rhyme_dictionary
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

if __name__ == "__main__":
    rhymes = rhyme_dictionary.RhymeDictionary(db_file="test.db")
    song_generator = SongGenerator()

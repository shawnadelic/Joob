from nltk.corpus import cmudict as cmu
from nltk.corpus import wordnet
import random
import sqlite3
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///test.db', echo=True)
engine.connect()
engine.execute("CREATE TABLE jerks ( id int )")

class RhymeDictionary(Base):
    __tablename__ = "rhyme_dict_entries"
    id = Column(Integer, primary_key = True)

    def __init__(self, db_file, syllable_trim = 2, match_trim = 5):
        self.connection = None
        try:
            #self.connection = sqlite3.connect(db_file)
            #self.cursor = self.connection.cursor()
            pass
        except:
            pass
            #print("Building rhyme dictionary")
            #self.syllable_trim = syllable_trim
            #self.match_trim = match_trim
            #self.cmu_dict = dict()
            #self.pronunciation_dict = dict()
            #self.matching_syllables_dict = dict()
            #self.matching_syllables_by_length_dict = dict()
            #self.matching_syllables_by_word_dict = dict()
            #self.build_cmu_dict()
            #self.build_pronunciation_dict()
            #self.build_matching_syllables_dict()
            #self.build_matching_syllables_by_word_dict()
            #self.write_to_db(db_file)
            #print("Finished building rhyme dictionary")
    #def __del__(self):
    #    if self.connection:
    #        self.close_connection()
    def __getitem__(self,key):
        result = self.get_all_rhymes(key)
        if result:
            return result
        else:
            raise IndexError
    def build_cmu_dict(self):
        for entry in cmu.entries():
            if entry[0] not in self.cmu_dict:
                self.cmu_dict[entry[0]] = [tuple(entry[1])]
            else:
                self.cmu_dict[entry[0]].append(tuple(entry[1]))
    def build_pronunciation_dict(self):
        for entry in self.cmu_dict:
            self.pronunciation_dict[entry] = self.get_rhyme_classes(entry)
    def build_matching_syllables_dict(self):
        for entry in self.pronunciation_dict:
            for pron in self.pronunciation_dict[entry]:
                if pron not in self.matching_syllables_dict and len(pron) > self.syllable_trim:
                    self.matching_syllables_dict[pron] = [entry]
                    self.matching_syllables_by_length_dict[len(pron)] = [pron]
                elif len(pron) > self.syllable_trim:
                    self.matching_syllables_dict[pron].append(entry)
                    self.matching_syllables_by_length_dict[len(pron)].append(pron)
    def build_matching_syllables_by_word_dict(self, include_self = False):
        for word in self.pronunciation_dict:
            result = []
            syllables = [pron for pron in self.get_rhyme_classes(word)]
            for syllable in syllables:
                if len(syllable) > self.syllable_trim:
                    match_list = [entry for entry in self.matching_syllables_dict[syllable] if include_self or word != entry]
                    result += match_list
            if result:
                self.matching_syllables_by_word_dict[word] = result
    def display_cmu_dict(self):
        for entry in self.cmu_dict:
            print entry, self.cmu_dict[entry]
    def display_matching_syllables_dict(self):
        for entry in self.matching_syllables_dict:
            if len(self.matching_syllables_dict[entry]) > self.match_trim:
                print entry, self.matching_syllables_dict[entry]
        for entry in self.matching_syllables_by_length_dict:
            print entry, ":"
            for pron in self.matching_syllables_by_length_dict[entry]:
                if len(self.matching_syllables_dict[pron]) > self.match_trim:
                    print pron, self.matching_syllables_dict[pron]
    def get_word_pron(self,word):
        if word not in self.cmu_dict:
            return False
        else:
            return self.cmu_dict[word]
    def rhymes_with(self,word1,word2):
        rhymes = 0
        for pron in self.pronunciation_dict[word1]:
            if pron in self.pronunciation_dict[word2]:
                print pron
                rhymes += 1
        return rhymes
    def get_all_rhymes(self,word):
        if self.connection:
            self.cursor.execute('''SELECT * FROM word_dict WHERE word = ?''',(word,))
            try:
                entry = self.cursor.next()
                return [str(w) for w in json.loads(entry[1])]
            except:
                return None
        else:
            if word in self.matching_syllables_by_word_dict:
                return self.matching_syllables_by_word_dict[word]
            else:
                return None
    def random(self,word):
        if self.connection:
            results = self.get_all_rhymes(word)
            return random.choice(results) if results else None
        else:
            if word in self.matching_syllables_by_word_dict:
                return random.choice(self.matching_syllables_by_word_dict[word])
            else:
                return None
    def get_rhyme_classes(self,word):
        if word not in self.cmu_dict:
            return False
        else:
            return {rhyme_class for pron in self.cmu_dict[word] for rhyme_class in self.get_rhyme_class(pron)}
    def get_rhyme_class(self,pron):
        for phon in pron:
            for a in range(len(pron)-1,-1,-1):
                yield pron[a:]
    def is_vowel(self,phon):
        if phon[-1].isdigit():
            return True
        else:
            return False
    def write_to_file(self,filename):
        with open(filename,"wb") as output_file:
            for key in self.matching_syllables_by_word_dict:
                output_file.write( str([key] + self.matching_syllables_by_word_dict[key]) )
    def write_to_db(self,filename):
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS word_dict(word TEXT, matches TEXT)")
        for word in self.matching_syllables_by_word_dict:
            json_string = json.dumps(self.matching_syllables_by_word_dict[word])
            cursor.execute("INSERT INTO word_dict (word, matches) VALUES(?,?)",(word,json_string))
        connection.commit()
        connection.close()
    def read_from_db(self,filename):
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM word_dict");
        for row in cursor:
            self.matching_syllables_by_word_dict[str(row[0])] = json.loads(row[1])
        connection.close()
    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    rhyme_dict = RhymeDictionary(db_file="test.db")
    while True: 
        word = str(raw_input("Enter a word to test: "))
        if word == "/quit":
            break
        #print rhyme_dict.get_all_rhymes(word)
        #print rhyme_dict.random(word)

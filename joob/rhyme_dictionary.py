import os.path
import random
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from collections import defaultdict
from nltk.corpus import cmudict as cmu

Base = declarative_base()

class_match_table = Table('class_match', Base.metadata,
    Column('rhyme_class_pron', String, ForeignKey('rhyme_class.pron'), primary_key=True),
    Column('entry_word', String, ForeignKey('entry.word'), primary_key=True))

class Entry(Base):
    __tablename__ = "entry"
    word = Column(String, primary_key=True)
    class_matches = relationship("RhymeClass", secondary=class_match_table,
        backref="word_match")

    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return self.word

class RhymeClass(Base):
    __tablename__ = "rhyme_class"
    pron = Column(String, primary_key=True)

    def __init__(self, pron):
        self.pron = pron

    def __repr__(self):
        return self.pron

class RhymeDictionary(object):

    def __init__(self, db_file, syllable_trim=1, match_trim=5):
        # Set parameters and create dictionaries
        self.syllable_trim = syllable_trim
        self.rhyme_dict = dict()
        self.reverse_rhyme_dict = defaultdict(list)

        # Connect to database
        database_exists = os.path.isfile(db_file)
        #engine = create_engine('sqlite:///' + db_file, echo=True)
        #engine.connect()

        # Create SessionMaker
        #self.SessionMaker = sessionmaker(bind=engine)
        #session = self.SessionMaker()
    
        # Check if database existed prior to connection, otherwise define
        # schema
        #if not database_exists:
        #    Base.metadata.create_all(engine)
       
        print "Building rhyme dictionary..."
        self.build_dictionaries()

        # Write to database
        #session.commit()

    # Build dictionaries from CMU entries
    def build_dictionaries(self):
        for word, pron_list in cmu.dict().items():
            rhyme_classes = self.get_rhyme_classes(pron_list)
            self.rhyme_dict[word] = rhyme_classes
            for rhyme_class in rhyme_classes:
                if word not in self.reverse_rhyme_dict[rhyme_class]:
                    self.reverse_rhyme_dict[rhyme_class].append(word)

    # Return all entries in reverse rhyme dictionary
    def get_rhymes(self, word):
        result = []
        try:
            rhyme_classes = sorted(self.rhyme_dict[word],
                    key=lambda pron_list: len(pron_list))
            for rhyme_class in rhyme_classes:
                rhyme_list = self.reverse_rhyme_dict[rhyme_class]
                if len(rhyme_list) > 1:
                    result.append([rhyme_class, rhyme_list])
        finally:
            return result

    def all_rhymes(self, word):
        result = []
        rhymes = self.get_rhymes(word)
        for word, rhyme_list in rhymes:
            result += rhyme_list
        return result

    # Return random rhyme for word
    def random_rhyme(self, word):
        all_rhymes = self.all_rhymes(word)
        try:
            print self.rhyme_dict[word]
            print all_rhymes
            return random.choice(all_rhymes)
        except IndexError:
            return None

    # Generates all possible rhyme classes from pronuncation
    def get_rhyme_classes(self, pron_list):
        rhyme_classes = []
        for pron in pron_list: 
            for a in range(len(pron)):
                rhyme_class = tuple(pron[a:])
                if len(rhyme_class) > self.syllable_trim:
                    rhyme_classes.append(rhyme_class)
        return rhyme_classes

if __name__ == "__main__":
    rhyme_dict = RhymeDictionary(db_file="test.db")
    while True: 
        word = str(raw_input("Enter a word to test (or /quit to exit): "))
        if word == "/quit":
            break
        print rhyme_dict.random_rhyme(word)

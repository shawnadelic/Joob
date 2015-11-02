import os.path
import random
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from collections import defaultdict
from nltk.corpus import cmudict as cmu

Base = declarative_base()

ClassMatchTable = Table('ClassMatch', Base.metadata,
    Column('rhyme_class_pron', String, ForeignKey('RhymeClass.pron'), primary_key=True),
    Column('entry_word', String, ForeignKey('Entry.word'), primary_key=True))

class Entry(Base):
    __tablename__ = "Entry"
    word = Column(String, primary_key=True)
    class_matches = relationship("RhymeClass", secondary=ClassMatchTable,
        backref="Entry")

    def __repr__(self):
        return "<Entry(word='%s')>" % self.word

class RhymeClass(Base):
    __tablename__ = "RhymeClass"
    pron = Column(String, primary_key=True)
    word_matches = relationship("Entry", secondary=ClassMatchTable,
            backref="RhymeClass")

    def __repr__(self):
        return "<RhymeClass(pron='%s')>" % self.pron

class RhymeDictionary(object):

    def __init__(self, db_file, syllable_trim=1, match_trim=5):
        # Set parameters and create dictionaries
        self.syllable_trim = syllable_trim
        self.rhyme_dict = dict()
        self.reverse_rhyme_dict = defaultdict(list)

        # Connect to database
        database_exists = os.path.isfile(db_file)
        engine = create_engine('sqlite:///' + db_file, echo=True)
        engine.connect()

        # Create SessionMaker
        self.SessionMaker = sessionmaker(bind=engine)

        # Check if database existed prior to connection, otherwise define
        if database_exists: 
            print "Opening database"
            # Read from database
        else:
            print "Building database"
            Base.metadata.create_all(engine)
            #session = self.SessionMaker()
            #entry = Entry(word="Jeb")
            #session.add(entry)
            #rhyme_class = RhymeClass(pron="Presidents")
            #session.add(rhyme_class)
            #entry.class_matches.append(rhyme_class)
            #session.commit()
            #session = self.SessionMaker()
            #lookup = session.query(RhymeClass).filter_by(pron="Presidents").one()
            #print lookup, lookup.word_matches

            print "Building rhyme dictionary..."
            self.build_dictionaries()
            # Build database 

        # Write to database

    # Build dictionaries from CMU entries
    def build_dictionaries(self):
        # Initialize dictionaries
        rhyme_dict = dict()
        reverse_rhyme_dict = defaultdict(list)
        entry_dict = dict()
        rhyme_class_dict = dict()

        # Open session
        session = self.SessionMaker()

        # Iterate through CMU dictionary and add entries to database
        for word, pron_list in cmu.dict().items():
            entry = Entry(word=word)
            entry_dict[word] = entry
            session.add(entry)

            rhyme_classes = self.get_rhyme_classes(pron_list)
            rhyme_dict[word] = rhyme_classes
            for rhyme_class in rhyme_classes:
                if word not in reverse_rhyme_dict[rhyme_class]:
                    reverse_rhyme_dict[rhyme_class].append(word)

        # Iterate through reverse_rhyme_dict, connecting rhyme class to words
        for rhyme_class, word_list in reverse_rhyme_dict.items():
            pron = " ".join(rhyme_class)
            rhyme_class = RhymeClass(pron=pron)
            rhyme_class_dict[pron] = rhyme_class
            session.add(rhyme_class)

            for word in word_list:
                entry_dict[word].class_matches.append(rhyme_class)

        # Commit changes to database
        session.commit()

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
        print rhymes
        for word, rhyme_list in rhymes:
            result += rhyme_list
        return result

    # Return random rhyme for word
    def random_rhyme(self, word):
        all_rhymes = self.all_rhymes(word)
        try:
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
        rhyme_dict.all_rhymes(word)
        print rhyme_dict.random_rhyme(word)

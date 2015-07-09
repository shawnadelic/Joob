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

    def __init__(self, db_file, syllable_trim=2, match_trim=5):
        # Save parameters
        self.syllable_trim = syllable_trim

        # Connect to database
        database_exists = os.path.isfile(db_file)
        engine = create_engine('sqlite:///' + db_file, echo=True)
        engine.connect()
    
        # Check if database existed prior to connection, otherwise define
        # schema
        if not database_exists:
            Base.metadata.create_all(engine)

        # Create SessionMaker
        self.SessionMaker = sessionmaker(bind=engine)
        session = self.SessionMaker()

        # Build dict from CMU entries
        self.rhyme_dict = dict()
        self.reverse_rhyme_dict = defaultdict(list)
        counter = 0
        for word, pron_list in cmu.dict().items():
            rhyme_classes = self.get_rhyme_classes(pron_list)
            self.rhyme_dict[word] = rhyme_classes
            for rhyme_class in rhyme_classes:
                if word not in self.reverse_rhyme_dict[rhyme_class]:
                    self.reverse_rhyme_dict[rhyme_class].append(word)
        word = "comically"
        for rhyme_class in sorted(self.rhyme_dict[word], key=lambda pron_list: len(pron_list)):
            rhyme_list = self.reverse_rhyme_dict[rhyme_class]
            if len(rhyme_list) > 1:
                print rhyme_class, rhyme_list
        #print len(seen)
        #print seen[:20]
        #cmu_dict = self.build_cmu_dict()
        #seen = []
        #for word, rhyme_classes in cmu_dict.items():
        #    entry = Entry(word)
        #    for rhyme_class in rhyme_classes:
        #        rhyme_class = str(rhyme_class)
        #        if rhyme_class not in seen:
        #            rhyme = RhymeClass(rhyme_class)
        #            session.add(rhyme)
        #            seen.append(rhyme_class)
        #    session.add(entry)
            #session.commit()
            #session = self.SessionMaker()
            #print item, sorted(set(r for r in self.get_rhyme_classes(item[1])))
        # Idea for test - Verify comically results in two different pronunciations
        # Build pronunciation dict from CMU dict - Integrated into build_cmu_dict
        # Build matching syllables dict (rhyme dict)
        # Build matching syllables by word dict
        # Write to database
        session.commit()

    # Generates all possible rhyme classes from pronuncation
    def get_rhyme_classes(self, pron_list):
        rhyme_classes = []
        for pron in pron_list: 
            for a in range(len(pron)):
                rhyme_class = tuple(pron[a:])
                if len(rhyme_class) > self.syllable_trim:
                    rhyme_classes.append(rhyme_class)

        # Return results as a sorted list of unique items, sorted by length
        # then alphanumerically
        return rhyme_classes
        #return sorted(set(rhyme_classes),
            #key=lambda rhyme_class: (len(rhyme_class), rhyme_class))

if __name__ == "__main__":
    rhyme_dict = RhymeDictionary(db_file="test.db")
    while True: 
        word = str(raw_input("Enter a word to test: "))
        if word == "/quit":
            break
        #print rhyme_dict.get_all_rhymes(word)
        #print rhyme_dict.random(word)

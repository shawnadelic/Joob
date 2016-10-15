#######################################################################
#                                                                     #
#  joob - a lyric generator                                           #
#                                                                     #
#######################################################################

import os
import random
import re
import sys
from collections import defaultdict

import nltk
from sqlalchemy import Column, ForeignKey, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Setup ORM
Base = declarative_base()

ClassMatchTable = Table(
    'ClassMatch', Base.metadata,
    Column(
        'rhyme_class_pron',
        String,
        ForeignKey('RhymeClass.pron'),
        primary_key=True
    ),
    Column(
        'entry_word',
        String,
        ForeignKey('Entry.word'),
        primary_key=True
    )
)


class Entry(Base):
    __tablename__ = "Entry"
    word = Column(String, primary_key=True)
    class_matches = relationship(
        "RhymeClass", secondary=ClassMatchTable,
        backref="Entry"
    )

    def __repr__(self):
        return "<Entry(word='%s')>" % self.word


class RhymeClass(Base):
    __tablename__ = "RhymeClass"
    pron = Column(String, primary_key=True)
    word_matches = relationship(
        "Entry", secondary=ClassMatchTable,
        backref="RhymeClass"
    )

    def __repr__(self):
        return "<RhymeClass(pron='%s')>" % self.pron


def get_rhyme_classes(pron_list, syllable_trim):
    """
    Return a list of all "rhyme classes" for a given pronunciation
    """
    rhyme_classes = []
    for pron in pron_list:
        for a in range(len(pron)):
            rhyme_class = tuple(pron[a:])
            if len(rhyme_class) > syllable_trim:
                rhyme_classes.append(rhyme_class)
    return rhyme_classes


def build_database(db_file, syllable_trim=0):
    """
    Build the database from CMU dictionary
    """

    # Download correct corpus, if not already downloaded
    nltk.download('cmudict', quiet=False)
    cmu = nltk.corpus.cmudict

    # Initialize dictionaries
    rhyme_dict = dict()
    reverse_rhyme_dict = defaultdict(list)
    entry_dict = dict()
    rhyme_class_dict = dict()

    # Connect to database
    engine = create_engine('sqlite:///' + db_file, echo=True)
    engine.connect()

    # Create SessionMaker
    Session = sessionmaker(bind=engine)

    print("Building database...")
    Base.metadata.create_all(engine)

    # Open session
    session = Session()

    # Iterate through CMU dictionary and add entries to database
    print("Adding words...")
    for word, pron_list in cmu.dict().items():
        entry = Entry(word=word)
        entry_dict[word] = entry
        session.add(entry)

        rhyme_classes = get_rhyme_classes(pron_list, syllable_trim)
        rhyme_dict[word] = rhyme_classes
        for rhyme_class in rhyme_classes:
            if word not in reverse_rhyme_dict[rhyme_class]:
                reverse_rhyme_dict[rhyme_class].append(word)

    # Iterate through reverse_rhyme_dict, connecting rhyme class to words
    print("Adding rhyme classes...")
    for rhyme_class, word_list in reverse_rhyme_dict.items():
        pron = " ".join(rhyme_class)
        rhyme_class = RhymeClass(pron=pron)
        rhyme_class_dict[pron] = rhyme_class.pron
        session.add(rhyme_class)

        for word in word_list:
            entry_dict[word].class_matches.append(rhyme_class)

    # Commit changes to database
    session.commit()

    return Session


def connect_to_database(db_file):
    """
    Connect to a database and return Session
    """

    # Connect to database
    print("Connecting with database...")
    engine = create_engine('sqlite:///' + db_file, echo=False)
    engine.connect()

    # Create SessionMaker
    Session = sessionmaker(bind=engine)

    return Session


class RhymeDictionary(object):

    def __init__(self, Session, trim=2):
        self.Session = Session
        self.trim = trim

    def get_rhymes(self, word):
        session = self.Session()
        all_results = []
        word_object = session.query(Entry).filter(Entry.word == word).first()
        if word_object:
            rhyme_classes = session.query(RhymeClass).filter(
                RhymeClass.word_matches.contains(word_object)
            ).all()
            for rhyme_class in filter(
                lambda c: len(c.pron.split()) >= self.trim,
                sorted(rhyme_classes, key=lambda rhyme: len(rhyme.pron))
            ):
                rhyme_class_results = []
                word_matches = session.query(Entry).filter(
                    Entry.class_matches.contains(rhyme_class)
                )
                rhyme_class_results.append(rhyme_class.pron)
                word_results = []
                for entry in word_matches:
                    if entry.word != word:
                        word_results.append(entry.word)
                if word_results:
                    rhyme_class_results.append(word_results)
                if len(rhyme_class_results) > 1:
                    all_results.append(rhyme_class_results)
        session.close()
        return all_results

    def random_rhyme(self, word):
        all_rhymes = self.get_rhymes(word)
        if all_rhymes:
            random_rhyme_class = random.choice(all_rhymes)[1]
            random_word = random.choice(random_rhyme_class)
            return random_word
        else:
            return None

    def rhyme_strength(self, word_a, word_b):
        session = self.Session()
        word_a_object = session.query(Entry).filter(
            Entry.word == word_a
        ).first()
        word_b_object = session.query(Entry).filter(
            Entry.word == word_b
        ).first()
        max_rhyme_strength = 0
        if word_a_object and word_b_object:
            rhyme_classes = session.query(RhymeClass).filter(
                RhymeClass.word_matches.contains(word_a_object),
                RhymeClass.word_matches.contains(word_b_object)
            ).all()
            for rhyme_class in filter(
                    lambda c: len(c.pron.split()) >= self.trim,
                    sorted(rhyme_classes, key=lambda rhyme: len(rhyme.pron))):
                max_rhyme_strength = max(
                    max_rhyme_strength, len(rhyme_class.pron.split()))
        session.close()
        return max_rhyme_strength

    @staticmethod
    def last_vowel_index(pron):
        """
        Given pronuncation (separated into a list of phoneme strings), returns
        reverse index of last syllable
        """
        pron.sort(reverse=True)
        vowel_re = re.compile('.*[0-9].*')
        for index, phone in enumerate(pron):
            if vowel_re.search(phone):
                return index
        return None


if __name__ == "__main__":
    db_file = sys.argv[1]

    # If database doesn't exist, build it, otherwise connect
    if not os.path.isfile(db_file):
        Session = build_database(db_file)
    else:
        Session = connect_to_database(db_file)

    rhyme_dict = RhymeDictionary(Session, 0)

    # Testing loop
    while True:
        first = str(raw_input("Enter first word to test (or /quit to exit): "))
        if first == "/quit":
            break
        second = str(raw_input("Enter second word to test: "))
        int(rhyme_dict.rhyme_strength(first, second))

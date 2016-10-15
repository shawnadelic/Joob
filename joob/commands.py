from joob.rhyme_dictionary import build_database, RhymeDictionary

def build_dict():
    Session = build_database("test.db")
    rhyme_dict = RhymeDictionary(Session, 0)

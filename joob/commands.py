from joob.rhyme_dictionary import RhymeDictionary, build_database


def build_dict():
    Session = build_database("test.db")
    RhymeDictionary(Session, 0)

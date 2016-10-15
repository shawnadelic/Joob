import os
import unittest
from joob.rhyme_dictionary import connect_to_database, RhymeDictionary

class TestClass(object):
    def test_rhyme_strength(self):
        Session = connect_to_database("test.db")
        rhyme_dict = RhymeDictionary(Session, 0)
        assert rhyme_dict.rhyme_strength("test", "blessed") > 0

# Tests
# beige - Valid word with no rhymes
# comically - Valid word with multiple pronunciations
# Test word with no other rhymes (beige)
# Test word with numerous pronunciations (comically)
# Test that words don't return themselves (jew)

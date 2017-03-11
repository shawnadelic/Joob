import unittest

from joob.rhyme_dictionary import connect_to_database, RhymeDictionary


def get_rhyme_dict():
    Session = connect_to_database("test.db")
    return RhymeDictionary(Session, 0)


class RhymeDictionaryTests(unittest.TestCase):
    def test_rhyme_strength(self):
        rhyme_dict = get_rhyme_dict()
        assert rhyme_dict.rhyme_strength("test", "blessed") > 0

    def test_get_rhymes(self):
        rhyme_dict = get_rhyme_dict()
        assert not rhyme_dict.get_rhymes("fakeword")
        assert rhyme_dict.get_rhymes("blue")

    def test_multiple_pronunciations(self):
        rhyme_dict = get_rhyme_dict()
        all_rhymes = []
        for syllables, rhyme in rhyme_dict.get_rhymes("comically"):
            all_rhymes.extend(rhyme)

        assert "theologically" in all_rhymes

    def test_doesnt_return_self_rhymes(self):
        rhyme_dict = get_rhyme_dict()
        all_rhymes = []
        for syllables, rhyme in rhyme_dict.get_rhymes("jew"):
            all_rhymes.extend(rhyme)

        assert "jew" not in all_rhymes

# Needed Tests
# Test word with no other rhymes

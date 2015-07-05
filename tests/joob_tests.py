import os
import unittest
from joob.rhyme_dictionary import RhymeDictionary

class JoobClass(unittest.TestCase):
    def test_init(self):
        self.rhyme_dict = RhymeDictionary("test.db")
        self.assertEqual(self.rhyme_dict.a, "No")
    def test_one(self):
        self.assertEqual(self,self)

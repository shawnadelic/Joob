import unittest

from joob.song_generator import SongGenerator


class SongGeneratorTests(unittest.TestCase):
    def test_mock_generator(self):
        song_gen = SongGenerator()
        assert song_gen.generate(mock=True) == "TEST MOCK STRING"

    def test_train(self):
        song_gen = SongGenerator()
        song_gen.train("dummydata")

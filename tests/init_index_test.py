import unittest

from init_index import *

DIR = r'C:\Users\volod\PycharmProjects\Foogle\tests\qq'


class IndexTest(unittest.TestCase):
    def test_get_data_in_file(self):
        data = defaultdict(list)
        phrases = defaultdict(list)
        init = InitIndex(DIR, None, data, phrases)
        init.get_data_in_file(DIR)

        self.assertTrue(True)

    def test_generate_subphrases(self):
        text = 'this is a test phrase'
        expected = ['a', 'is', 'this', 'is a', 'test', 'a test', 'phrase', 'this is', 'this is a', 'is a test',
                    'test phrase', 'a test phrase', 'this is a test', 'is a test phrase', 'this is a test phrase']
        init = InitIndex(DIR, None, None, None)

        self.assertListEqual(expected, init.generate_subphrases(text))

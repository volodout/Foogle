import unittest
from init import count_files_in_directory

EMPTY_DIR = r'C:\Users\volod\PycharmProjects\Foogle\tests\empty_dir'
QQ_DIR = r'C:\Users\volod\PycharmProjects\Foogle\tests\qq'

class InitTest(unittest.TestCase):
    def test_count_files_in_empty_directory(self):
        self.assertEqual(0, count_files_in_directory(EMPTY_DIR))

    def test_count_files_in_directory(self):
        self.assertEqual(4, count_files_in_directory(QQ_DIR))
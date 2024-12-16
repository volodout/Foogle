import unittest
from init import count_files_and_checksum_in_directory

EMPTY_DIR = r'empty_dir'
QQ_DIR = r'qq'

class InitTest(unittest.TestCase):
    def test_count_files_in_empty_directory(self):
        self.assertEqual(0, count_files_and_checksum_in_directory(EMPTY_DIR)[0])

    def test_count_files_in_directory(self):
        self.assertEqual(4, count_files_and_checksum_in_directory(QQ_DIR)[0])
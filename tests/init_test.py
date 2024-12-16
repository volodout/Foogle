import os
import unittest
from init import count_files_and_checksum_in_directory


class InitTest(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.empty_dir = os.path.join(base_dir, 'empty_dir')
        self.qq_dir = os.path.join(base_dir, 'qq')

    def test_count_files_in_empty_directory(self):
        self.assertEqual(0, count_files_and_checksum_in_directory(self.empty_dir)[0])

    def test_count_files_in_directory(self):
        self.assertEqual(4, count_files_and_checksum_in_directory(self.qq_dir)[0])
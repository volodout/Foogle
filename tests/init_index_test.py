import os
import shutil
import unittest
import random

from index import Index
from init import count_files_and_checksum_in_directory

from init_index import InitIndex

class IndexTest(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.empty_dir = os.path.join(base_dir, 'empty_dir')
        self.qq_dir = os.path.join(base_dir, 'qq')

    def clear_directory(self, directory_path='saves'):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    def test_without_recovery(self):
        self.clear_directory()
        index = self.check_dir()
        request = "pick pop it lick kek"
        phrase = request.split()
        res = index.check_phrase(index.data[phrase[0]], len(phrase), request)
        self.assertEqual(1, len(res))
        self.assertTrue(res[0][1].endswith('2.txt'))
        self.clear_directory()

    def check_dir(self):
        data = count_files_and_checksum_in_directory(self.qq_dir)
        index = Index(self.qq_dir, data[1], data[0])
        return index

    def test_with_recovery(self):
        self.clear_directory()
        first_res = self.check_dir()
        path, folders, files = next(os.walk('saves'))
        self.assertEqual(1, len(files))
        second_res = self.check_dir()
        self.assertEqual(first_res.checksum, second_res.checksum)
        self.assertDictEqual(first_res.checksums, second_res.checksums)
        request = "pick pop it lick kek"
        phrase = request.split()
        res = second_res.check_phrase(second_res.data[phrase[0]], len(phrase), request)
        self.assertEqual(1, len(res))
        self.assertTrue(res[0][1].endswith('2.txt'))
        self.clear_directory()

    def test_recovery_after_changes_in_file(self):
        self.clear_directory()
        first_res = self.check_dir()
        request = 'lick kick pick hero'
        with open(self.qq_dir + r"\\1.txt", 'r+') as f:
            begin_str = f.readline()
            f.write(" hero")
        second_res = self.check_dir()
        self.assertEqual(first_res.checksum, second_res.checksum)
        res = []
        for key in first_res.checksums.keys():
            res.append(first_res.checksums[key] == second_res.checksums[key])
        self.assertTrue(not all(res))
        phrase = request.split()
        res = second_res.check_phrase(second_res.data[phrase[0]], len(phrase), request)
        self.assertEqual(1, len(res))
        self.assertTrue(res[0][1].endswith('1.txt'))
        with open(self.qq_dir + r"\\1.txt", 'w') as f:
            f.write(begin_str)
        self.clear_directory()

    def test_recovery_after_append_file(self):
        self.clear_directory()
        first_res = self.check_dir()
        request = "abobaaaaaaaaaa top"
        with open(self.qq_dir + r"\\52.txt", 'w') as f:
            f.write(request)
        second_res = self.check_dir()
        self.assertNotEqual(first_res.checksum, second_res.checksum)
        phrase = request.split()
        res = second_res.check_phrase(second_res.data[phrase[0]], len(phrase), request)
        self.assertEqual(1, len(res))
        self.assertTrue(res[0][1].endswith('52.txt'))
        os.remove(res[0][1])
        self.clear_directory()

    def test_recovery_after_delete_file(self):
        self.clear_directory()
        first_res = self.check_dir()
        with open(self.qq_dir + r"\\1.txt", 'r') as f:
            data = f.readline()
        os.remove(self.qq_dir + r"\\1.txt")
        second_res = self.check_dir()
        self.assertNotEqual(first_res.checksum, second_res.checksum)
        phrase = data.split()
        res = second_res.check_phrase(second_res.data[phrase[0]], len(phrase), data)
        self.assertEqual(0, len(res))
        with open(self.qq_dir + r"\\1.txt", 'w') as f:
            f.write(data)
        self.clear_directory()
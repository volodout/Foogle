import unittest
import os
import shutil
from pathlib import Path
from index import Index
from init import count_files_and_checksum_in_directory
import math


class TestAutocompleteAndTfIdf(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)

        with open(self.test_dir / "doc1.txt", "w", encoding="utf-8") as f:
            f.write("receive recycle record\nrecommend recipe\n")
        with open(self.test_dir / "doc2.txt", "w", encoding="utf-8") as f:
            f.write("recommend receive recovery\nrecreate rectangle\n")

        total_items, checksum_directory = count_files_and_checksum_in_directory(str(self.test_dir))
        self.index = Index(str(self.test_dir), checksum_directory, total_items)

    @classmethod
    def tearDownClass(self):
        if self.test_dir.exists():
            for item in self.test_dir.iterdir():
                item.unlink()
            self.test_dir.rmdir()

    def test_tf_idf_basic(self):
        score = self.index.get_tf_idf("receive", "doc2.txt")
        self.assertEqual(score, 0.0)

        score_recommend = self.index.get_tf_idf("recommend", "doc1.txt")
        self.assertEqual(score_recommend, 0.0)

    def test_tf_idf_no_occurrence(self):
        score = self.index.get_tf_idf("nonexistent", "doc1.txt")
        self.assertEqual(score, 0.0)

    def get_completions(self, prefix):
        matches = [w for w in self.index.all_full_words if w.startswith(prefix)]
        matches.sort(key=lambda w: self.index.best_tf_idf_for_word[w], reverse=True)
        return matches[:5]

    def test_autocomplete_basic(self):
        completions = self.get_completions("rec")

        self.assertTrue(len(completions) <= 5)
        for w in completions:
            self.assertTrue(w.startswith("rec"))

    def test_autocomplete_limit(self):
        completions = self.get_completions("rec")
        self.assertEqual(len(completions), 5)

    def test_autocomplete_no_matches(self):
        completions = self.get_completions("xyz")
        self.assertEqual(len(completions), 0)


if __name__ == '__main__':
    unittest.main()
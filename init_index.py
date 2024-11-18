import os
import re
from collections import defaultdict
from init import compute_tf_idf


class InitIndex:

    def __init__(self, directory, progress_bar, words=None, phrases=None):
        if words is None:
            words = defaultdict(list)
        if phrases is None:
            phrases = dict()
        self.path = directory
        self.words = words
        self.phrases = phrases
        self.progress_bar = progress_bar
        self.extensions = None
        path, folders, files = next(os.walk(directory))
        self.get_data_in_files(files)
        self.init_folders(folders)

    def get_data_in_files(self, files):
        for file in files:
            try:
                if self.progress_bar:
                    self.progress_bar.update(1)
                filepath = os.path.join(self.path, file)
                self.get_data_in_file(filepath)
            except PermissionError:
                continue

    def get_data_in_file(self, directory):
        if not directory.endswith('.txt'):
            return
        try:
            with open(directory, 'r', encoding='utf-8') as f:
                sentences = []
                for i, line in enumerate(f):
                    line = line.lower().strip()
                    words = line.split()
                    sentences.append(words)
                    for j, word in enumerate(words):
                        substrings = self.generate_substrings(word)
                        for substring in substrings:
                            self.words[substring].append((word, (i, j), directory))
            self.phrases[directory] = tuple(sentences)
        except UnicodeDecodeError:
            pass

    def generate_substrings(self, word):
        return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]

    def init_folders(self, folders):
        for folder in folders:
            try:
                init = InitIndex(self.path + '\\' + folder, self.progress_bar, self.words, self.phrases)
            except PermissionError:
                continue

    def get_data(self):
        return self.words

    def get_phrases(self):
        return self.phrases
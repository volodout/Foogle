import os
import re
from collections import defaultdict


class InitIndex:

    def __init__(self, directory, progress_bar, data=None, phrases=None):
        if data is None:
            data = defaultdict(list)
        if phrases is None:
            phrases = defaultdict(list)
        self.path = directory
        self.data = data
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
                for line in f:
                    line = line.lower().strip()
                    words = set(re.findall(r'\w+', line))

                    for word in words:
                        substrings = self.generate_substrings(word)
                        for substring in substrings:
                            self.data[substring].append((word, directory))

                    phrases_in_line = self.generate_subphrases(line)
                    for phrase in phrases_in_line:
                        substrings = self.generate_substrings(phrase)
                        for substring in substrings:
                            if ' ' not in substring.strip():
                                continue
                            if self.phrases[substring] and \
                                    self.phrases[substring][-1][0] in phrase and \
                                    directory == self.phrases[substring][-1][1]:
                                continue
                            self.phrases[substring].append((phrase.strip(), directory))
        except UnicodeDecodeError:
            print('Не получилось декодировать файл:', directory)

    def generate_subphrases(self, text):
        words = text.split()
        subphrases = []
        for start in range(len(words)):
            for end in range(start + 1, len(words) + 1):
                subphrases.append(" ".join(words[start:end]))
        return sorted(subphrases, key=len)

    def generate_substrings(self, word):
        return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]

    def init_folders(self, folders):
        for folder in folders:
            try:
                init = InitIndex(self.path + '\\' + folder, self.progress_bar, self.data, self.phrases)
            except PermissionError:
                continue

    def get_data(self):
        return self.data

    def get_phrases(self):
        return self.phrases
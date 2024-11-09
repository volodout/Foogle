import os
import re
from collections import defaultdict


class InitIndex:

    def __init__(self, directory, progress_bar, data=None):
        if data is None:
            data = defaultdict(list)
        self.path = directory
        self.data = data
        self.progress_bar = progress_bar
        self.extensions = None
        path, folders, files = next(os.walk(directory))
        self.__get_data_in_files(files)
        self.__init_folders(folders)

    def __get_data_in_files(self, files):
        for file in files:
            try:
                if self.progress_bar:
                    self.progress_bar.update(1)
                filepath = os.path.join(self.path, file)
                self.__get_data_in_file(filepath)
            except PermissionError:
                continue

    def __get_data_in_file(self, directory):
        with open(directory) as f:
            text = f.read().lower()
            words = set(re.findall(r'\w+', text))
            for word in words:
                substrings = self.__generate_substrings(word)
                for substring in substrings:
                    self.data[substring].append(directory)

    def __generate_substrings(self, word):
        return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]

    def __init_folders(self, folders):
        for folder in folders:
            try:
               init = InitIndex(self.path + '\\' + folder, self.progress_bar, self.data)
            except PermissionError:
                continue

    def get(self):
        return self.data

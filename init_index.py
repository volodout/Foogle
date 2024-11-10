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
        if not directory.endswith('.txt'):
            return
        try:
            with open(directory, 'r', encoding='utf-8') as f:
                text = f.read().lower()
                words = set(re.findall(r'\w+', text))

                # Добавляем слова и их подстроки в data
                for word in words:
                    substrings = self.__generate_substrings(word)
                    for substring in substrings:
                        self.data[substring].append((word, directory))

                # Разделяем текст на фразы для поиска многословных фраз
                phrases_in_file = self.__generate_subphrases(text)
                for phrase in phrases_in_file:
                    substrings = self.__generate_substrings(phrase)
                    for substring in substrings:
                        if str(substring).strip().count(' ') == 0:
                            continue
                        if len(self.phrases[substring]) > 0 and len(self.phrases[substring]) > 0:
                            sub = self.__generate_subphrases(substring)
                            a = [i == self.phrases[substring][-1] for i in sub]
                            if any(a):
                                continue
                            if self.phrases[substring][-1][0] in phrase and directory == self.phrases[substring][-1][1]:
                                continue
                        self.phrases[substring].append((phrase.strip(), directory))
        except UnicodeDecodeError:
            print('Не получилось декодировать файл: ', directory)

    def __generate_subphrases(self, text):
        words = text.split()
        subphrases = []
        for start in range(len(words)):
            for end in range(start + 1, len(words) + 1):
                subphrases.append(" ".join(words[start:end]))
        return sorted(subphrases, key=len)

    def __generate_substrings(self, word):
        return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]

    def __init_folders(self, folders):
        for folder in folders:
            try:
                init = InitIndex(self.path + '\\' + folder, self.progress_bar, self.data, self.phrases)
            except PermissionError:
                continue

    def get_data(self):
        return self.data

    def get_phrases(self):
        return self.phrases
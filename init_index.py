import os
from collections import defaultdict
import pickle
import hashlib

import init


def default_dict_of_int():
    return defaultdict(int)


def default_dict_of_default_dict_int():
    return defaultdict(default_dict_of_int)


class InitIndex:

    def __init__(self, directory, progress_bar, checksum_directory,
                 words=None, phrases=None, checksums=None,
                 is_recovery=False, del_directs=None, recalculate_directs=None):
        if is_recovery:
            if del_directs is None:
                del_directs = set(phrases.keys())
            if recalculate_directs is None:
                recalculate_directs = set()
        self.path = directory
        self.words = words or defaultdict(list)
        self.phrases = phrases or {}
        self.checksums = checksums or {}
        self.checksum_directory = checksum_directory
        self.is_recovery = is_recovery
        self.progress_bar = progress_bar
        self.del_directs = del_directs
        self.recalculate_directs = recalculate_directs
        self.process_directory()

    def process_directory(self):
        path, folders, files = next(os.walk(self.path))
        self.get_data_in_files(files)
        self.init_folders(folders)

        if not hasattr(self, 'document_word_counts'):
            InitIndex.init_document_word_counts(self)


    def get_data_in_files(self, files):
        for file in files:
            try:
                if self.progress_bar:
                    self.progress_bar.update(1)
                filepath = os.path.join(self.path, file)
                self.get_data_in_file(filepath)
            except PermissionError:
                continue

    def get_data_in_file(self, file_path):
        if not file_path.endswith('.txt'):
            return
        if self.is_recovery:
            self.del_directs.discard(file_path)
            if file_path in self.checksums.keys():
                hash = self.calculate_checksum(file_path)
                if self.checksums[file_path] != hash:
                    self.recalculate_directs.add(file_path)
                return
        try:
            self.read_file(file_path)
            self.calculate_checksum(file_path)
        except UnicodeDecodeError:
            pass

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            sentences = []
            for i, line in enumerate(f):
                line = line.lower().strip()
                words = line.split()
                sentences.append(words)
                for j, word in enumerate(words):
                    substrings = InitIndex.generate_substrings(word)
                    for substring in substrings:
                        self.words[substring].append((word, (i, j), file_path))
        self.phrases[file_path] = tuple(sentences)
        self.checksums[file_path] = InitIndex.calculate_checksum(file_path)

    @staticmethod
    def calculate_checksum(file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def generate_substrings(word):
        return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]

    def init_folders(self, folders):
        for folder in folders:
            try:
                init = InitIndex(self.path + '\\' + folder, self.progress_bar,
                                 self.checksum_directory, self.words,
                                 self.phrases, self.checksums, self.is_recovery, self.del_directs,
                                 self.recalculate_directs)
            except PermissionError:
                continue

    def get_data(self):
        return self.words

    def get_phrases(self):
        return self.phrases

    def get_checksums(self):
        return self.checksums

    def get_checksum_directory(self):
        return self.checksum_directory

    @staticmethod
    def init_document_word_counts(res):
        res.document_word_counts = default_dict_of_default_dict_int()
        res.word_document_counts = defaultdict(set)
        docs = list(res.phrases.keys())
        res.total_documents = len(docs)
        for doc in docs:
            for sentence in res.phrases[doc]:
                for w in sentence:
                    res.document_word_counts[doc][w] += 1
                    res.word_document_counts[w].add(doc)

    @staticmethod
    def recovery_index(name, checksum_directory):
        with open(f'saves/{name}.pkl', 'rb') as f:
            loaded_data = pickle.load(f)
        if loaded_data.get_checksum_directory() != checksum_directory:
            res = InitIndex.recovery_directory(loaded_data)
            res.checksum_directory = checksum_directory
            if not hasattr(res, 'document_word_counts'):
                InitIndex.init_document_word_counts(res)
            return res

        res = InitIndex.recover_files(loaded_data)
        res.checksum_directory = checksum_directory

        if not hasattr(res, 'document_word_counts'):
            InitIndex.init_document_word_counts(res)
        return res

    @staticmethod
    def recover_files(data):
        words_data = data.get_data()
        phrases = data.get_phrases()
        checksums = data.get_checksums()
        del_directs = set()
        for key in checksums.keys():
            if InitIndex.calculate_checksum(key) == checksums[key]:
                continue
            del_directs.add(key)
        InitIndex.delete_directory_from_data(del_directs, data, checksums)
        for path in del_directs:
            InitIndex.recover_file(path, words_data, phrases, checksums)
        return data

    @staticmethod
    def recovery_directory(data):
        path = data.path
        checksums = data.get_checksums()
        words = data.get_data()
        phrases = data.get_phrases()
        init = InitIndex(path, None, 0,
                         words, phrases, checksums, True)
        InitIndex.delete_directory_from_data({*init.del_directs, *init.recalculate_directs}, init, checksums)
        for file in init.recalculate_directs:
            InitIndex.recover_file(file, init.words, init.phrases, init.checksums)
        return init

    @staticmethod
    def delete_directory_from_data(del_directs, init, checksums):
        for key in set(init.phrases.keys()):
            if key in del_directs:
                init.phrases.pop(key)
                checksums.pop(key)
        for key in set(init.words.keys()):
            res = []
            for val in init.words[key]:
                if val[-1] in del_directs:
                    continue
                res.append(val)
            if len(res) == 0:
                init.words.pop(key)
                continue
            init.words[key] = res

    @staticmethod
    def recover_file(file_path, words_data, phrases, checksums):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sentences = []
                for i, line in enumerate(f):
                    line = line.lower().strip()
                    words = line.split()
                    sentences.append(words)
                    for j, word in enumerate(words):
                        substrings = InitIndex.generate_substrings(word)
                        for substring in substrings:
                            words_data[substring].append((word, (i, j), file_path))
            phrases[file_path] = tuple(sentences)
        except UnicodeDecodeError:
            pass
        checksums[file_path] = InitIndex.calculate_checksum(file_path)

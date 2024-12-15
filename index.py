import math
import os
import re
import pickle
from collections import defaultdict

from tqdm import tqdm

from init_index import InitIndex


class Index:
    def __init__(self, directory, checksum_directory, total_items):
        path, folders, files = next(os.walk('saves'))
        name = directory.replace(':', '')
        name = name.replace('\\', '_')
        if f'{name}.pkl' in files:
            print('Идёт выгрузка из памяти, пожалуйста, подождите...')
            init = InitIndex.recovery_index(name, checksum_directory)
            with open(f'saves/{name}.pkl', 'wb') as f:
                pickle.dump(init, f)
        else:
            progress_bar = tqdm(total=total_items)
            init = InitIndex(directory, progress_bar, checksum_directory)
            progress_bar.close()
            init.progress_bar = None
            with open(f'saves/{name}.pkl', 'wb') as f:
                pickle.dump(init, f)
        self.data = init.get_data()
        self.phrases = init.get_phrases()
        self.checksum = checksum_directory
        self.checksums = init.get_checksums()

        self.document_word_counts = init.document_word_counts
        self.word_document_counts = init.word_document_counts
        self.total_documents = init.total_documents

    def start(self):
        while True:
            print('Введите интересующее слово или фразу: ')
            request = input().lower()
            words_in_request = request.split()
            count_words = len(words_in_request)

            if count_words > 1:
                base = self.data.get(words_in_request[0], [])
                if not base:
                    print('Данное предложение не найдено')
                    continue

                results = []
                for word, coord, directory in base:
                    i, j = coord
                    if j + count_words - 1 >= len(self.phrases[directory][i]):
                        continue
                    sentence = ' '.join(self.phrases[directory][i][j: j + count_words]).lower()
                    if re.search(re.escape(request), sentence):
                        score = sum(self.get_tf_idf(w, directory) for w in words_in_request)
                        results.append((sentence, directory, score))

                results.sort(key=lambda x: x[2], reverse=True)

                for sentence, directory, score in results:
                    print(f'"{sentence}" in {directory} (tf-idf: {score:.4f})')
            else:
                base = self.data.get(request, [])
                if not base:
                    print('Данное слово не найдено')
                    continue

                print('Найдены следующие совпадения:')
                results = []
                for word, coord, directory in base:
                    score = self.get_tf_idf(word, directory)
                    results.append((word, directory, score))

                results.sort(key=lambda x: x[2], reverse=True)

                for word, directory, score in results:
                    print(f'"{word}" in {directory} (tf-idf: {score:.4f})')

    def get_tf_idf(self, word, doc):
        doc_words = self.document_word_counts[doc]
        term_freq = doc_words.get(word, 0)
        total_terms_in_doc = sum(doc_words.values())
        if total_terms_in_doc == 0:
            return 0.0
        tf = term_freq / total_terms_in_doc
        df = len(self.word_document_counts.get(word, set()))
        if df == 0:
            return 0.0
        idf = math.log((self.total_documents + 1) / (df + 1))
        return tf * idf

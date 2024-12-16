import math
import os
import re
import pickle
import readline
from collections import defaultdict

from tqdm import tqdm

from init_index import InitIndex
import re

def completer_function_factory(options):
    def completer(text, state):
        matches = [x for x in options if x.startswith(text)]
        if state < len(matches):
            return matches[state]
        return None
    return completer

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

        self.all_full_words = set()
        for doc, sentences in self.phrases.items():
            for sentence in sentences:
                for w in sentence:
                    self.all_full_words.add(w)

        self.best_tf_idf_for_word = {}
        for w in self.all_full_words:
            max_score = 0.0
            for doc, doc_words in self.document_word_counts.items():
                if w in doc_words:
                    score = self.get_tf_idf(w, doc)
                    if score > max_score:
                        max_score = score
            self.best_tf_idf_for_word[w] = max_score

    def start(self):
        def completer(text, state):
            matches = [w for w in self.all_full_words if w.startswith(text)]
            matches.sort(key=lambda w: self.best_tf_idf_for_word[w], reverse=True)
            top_5 = matches[:5]
            if state < len(top_5):
                return top_5[state]
            return None

        readline.set_completer(completer)
        readline.parse_and_bind('tab: complete')

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
                for sentence, directory, score in self.check_phrase(base, count_words, request):
                    print(f'"{sentence}" in {directory} (tf-idf: {score:.4f})')

            else:
                base = self.data.get(request, [])
                if not base:
                    print('Данное слово не найдено')
                    continue

                for word, directory, score in self.check_word(request):
                    print(f'"{word}" in {directory} (tf-idf: {score:.4f})')

    def check_word(self, request):
        print('Найдены следующие совпадения:')
        results = []
        for word, coord, directory in self.data[request]:
            score = self.get_tf_idf(word, directory)
            results.append((word, directory, score))
        return results


    def check_phrase(self, base, count_words, request):
        results = []
        for word, coord, directory in base:
            i, j = coord
            if j + count_words - 1 >= len(self.phrases[directory][i]):
                continue
            sentence = ' '.join(self.phrases[directory][i][j: j + count_words]).lower()
            if re.search(re.escape(request), sentence):
                score = sum(self.get_tf_idf(w, directory) for w in request.split())
                results.append((sentence, directory, score))

        results.sort(key=lambda x: x[2], reverse=True)

        return results

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





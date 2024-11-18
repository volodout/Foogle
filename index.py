from init import compute_tf_idf
from init_index import InitIndex
import re


class Index:
    def __init__(self, directory, progress_bar):
        init = InitIndex(directory, progress_bar)
        self.data = init.get_data()
        self.phrases = init.get_phrases()
        self.tf_idf = compute_tf_idf(self.data, len(self.phrases))

    def start(self):
        while True:
            print('Введите интересующее слово или фразу: ')
            request = input().lower()
            words_in_request = request.split()
            count_words = len(words_in_request)

            if count_words > 1:
                base = self.data[words_in_request[0]]
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
                        tf_idf_score = sum(self.get_tf_idf(word, directory) for word in words_in_request)
                        results.append((sentence, directory, tf_idf_score))

                results.sort(key=lambda x: x[2], reverse=True)
                for sentence, directory, score in results:
                    print(f'"{sentence}" in {directory} (TF-IDF: {score:.4f})')
            else:
                if not self.data[request]:
                    print('Данное слово не найдено')
                    continue

                print('Найдены следующие совпадения:')
                results = []
                for word, coord, directory in self.data[request]:
                    tf_idf_score = self.get_tf_idf(word, directory)
                    results.append((word, directory, tf_idf_score))

                results.sort(key=lambda x: x[2], reverse=True)
                for word, directory, score in results:
                    print(f'"{word}" in {directory} (TF-IDF: {score:.4f})')

    def get_tf_idf(self, word, doc):
        for w, d, score in self.tf_idf.get(word, []):
            if d == doc:
                return score
        return 0

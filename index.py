from init_index import InitIndex
import re


class Index:
    def __init__(self, directory, progress_bar):
        init = InitIndex(directory, progress_bar)
        self.data = init.get_data()
        self.phrases = init.get_phrases()
        self.tf_idf_data = init.tf_idf_data

    def start(self):
        while True:
            print('Введите интересующее слово или фразу: ')
            request = input().lower()
            words_in_request = request.split()
            count_words = len(words_in_request)
            if count_words > 1:
                base = self.data[words_in_request[0]]
                if len(base) == 0:
                    print('Данное предложение не найдено')
                for word, coord, directory in base:
                    i, j = coord
                    if j + count_words - 1 >= len(self.phrases[directory][i]):
                        continue
                    sentence = ' '.join(self.phrases[directory][i][j: j + count_words]).lower()
                    if re.search(re.escape(request), sentence):
                        print(f'"{sentence}" in {directory}')
            else:
                if len(self.data[request]) == 0:
                    print('Данное слово не найдено')
                    continue
                print('Найдены следующие совпадения:')
                for word, i, directory in self.data[request]:
                    print(f'"{word}" in {directory}')


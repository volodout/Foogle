from init_index import InitIndex


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

            if len(words_in_request) > 1:
                if request not in self.phrases:
                    print('Данная фраза не найдена')
                    continue
                print('Найдены следующие совпадения:')
                results = sorted(self.phrases[request], key=lambda x: x[1], reverse=True)
                for phrase, directory in results:
                    print(f'"{phrase}" in {directory}')
            else:
                if len(self.tf_idf_data[request]) == 0:
                    print('Данное слово не найдено')
                    continue
                print('Найдены следующие совпадения:')
                results = sorted(self.tf_idf_data[request], key=lambda x: x[2], reverse=True)
                for word, directory, score in results:
                    print(f'"{word}" in {directory} (TF-IDF: {score:.4f})')
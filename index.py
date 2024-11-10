from init_index import InitIndex


class Index:

    def __init__(self, directory, progress_bar):
        init = InitIndex(directory, progress_bar)
        self.data = init.get_data()
        self.phrases = init.get_phrases()

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
                for phrase, directory in self.phrases[request]:
                    print(f'"{phrase}" in {directory}')
            else:
                if len(self.data[request]) == 0:
                    print('Данное слово не найдено')
                    continue
                print('Найдены следующие совпадения:')
                for word, directory in self.data[request]:
                    print(f'"{word}" in {directory}')

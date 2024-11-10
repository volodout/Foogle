from init_index import InitIndex


class Index:

    def __init__(self, directory, progress_bar):
        init = InitIndex(directory, progress_bar)
        self.data = init.get()

    def start(self):
        while True:
            print('Введите интересующее слово: ')
            request = input().lower()
            if len(self.data[request]) == 0:
                print('Данное слово не найдено')
                continue
            print('Встретилось в следующих директориях:')
            for directory in self.data[request]:
                print(directory)

from index import Index
from init import count_files_in_directory
from tqdm import tqdm

if __name__ == '__main__':
    directory = input("Введите путь к директории: ")
    print('Инициализация, пожалуйста, подождите')
    total_items = count_files_in_directory(directory)
    progress_bar = tqdm(total=total_items)
    index = Index(directory, progress_bar)
    progress_bar.close()
    index.start()


from index import Index
from init import count_files_and_checksum_in_directory
from tqdm import tqdm

if __name__ == '__main__':
    directory = input("Введите путь к директории: ")
    print('Инициализация, пожалуйста, подождите...')
    total_items, checksum_directory = count_files_and_checksum_in_directory(directory)
    index = Index(directory, checksum_directory, total_items)
    index.start()

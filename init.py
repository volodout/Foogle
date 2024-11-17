import math
import os
from collections import defaultdict


def count_files_in_directory(directory):
    file_count = 0
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path):
                    file_count += 1
                elif os.path.isdir(item_path):
                    file_count += count_files_in_directory(item_path)
            except PermissionError:
                continue
    except PermissionError:
        return 0
    return file_count

def compute_tf_idf(data, total_documents):
    tf_idf = defaultdict(list)
    document_word_counts = defaultdict(lambda: defaultdict(int))
    word_document_counts = defaultdict(int)

    # Подсчет TF и количества документов, содержащих слово
    for substring, occurrences in data.items():
        word_document_counts[substring] = len(occurrences)
        for word, doc in occurrences:
            document_word_counts[doc][word] += 1

    # Вычисление TF-IDF
    for substring, occurrences in data.items():
        # Обновленная формула IDF
        idf = math.log(1 + (total_documents / (1 + word_document_counts[substring])))
        for word, doc in occurrences:
            tf = document_word_counts[doc][word] / sum(document_word_counts[doc].values())
            tf_idf[substring].append((word, doc, tf * idf))

    return tf_idf
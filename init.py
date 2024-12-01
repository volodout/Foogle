import math
import os
from collections import defaultdict
import hashlib


def count_files_and_checksum_in_directory(directory):
    file_count = 0
    hasher = hashlib.md5()

    try:
        items = sorted(os.listdir(directory))
        for item in items:
            item_path = os.path.join(directory, item)
            try:
                if os.path.isfile(item_path):
                    file_count += 1
                    if item.endswith('.txt'):
                        hasher.update(item_path.encode('utf-8'))
                elif os.path.isdir(item_path):
                    subdir_file_count, subdir_hash = count_files_and_checksum_in_directory(item_path)
                    file_count += subdir_file_count
                    hasher.update(subdir_hash.encode('utf-8'))
            except PermissionError:
                continue
    except PermissionError:
        return file_count, ""
    return file_count, hasher.hexdigest()


def compute_tf_idf(data, total_documents):
    tf_idf = defaultdict(list)
    document_word_counts = defaultdict(lambda: defaultdict(int))
    word_document_counts = defaultdict(int)

    for substring, occurrences in data.items():
        unique_documents = set()
        for word, coord, doc in occurrences:
            document_word_counts[doc][word] += 1
            unique_documents.add(doc)
        word_document_counts[substring] = len(unique_documents)

    for substring, occurrences in data.items():
        idf = math.log(1 + (total_documents / (1 + word_document_counts[substring])))
        for word, coord, doc in occurrences:
            tf = document_word_counts[doc][word] / sum(document_word_counts[doc].values())
            tf_idf[substring].append((word, doc, tf * idf))

    return tf_idf

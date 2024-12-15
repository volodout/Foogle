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

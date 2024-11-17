import os


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

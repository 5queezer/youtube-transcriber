import os


def change_file_extension(filename, new_extension):
    if filename is None:
        return None
    base = os.path.splitext(filename)[0]
    return base + new_extension

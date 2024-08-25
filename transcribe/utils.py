import os


def change_file_extension(filename, new_extension):
    if filename is None:
        return None
    base, _extension = os.path.splitext(filename)
    return base + new_extension

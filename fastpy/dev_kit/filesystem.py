import os
import shutil


def read_file(filepath: str) -> str:
    with open(filepath, 'r') as f:
        return f.read()


def write_file(filepath: str, content: str):
    with open(filepath, 'w') as f:
        f.write(content)


def normalize_path(path: str) -> str:
    if os.path.exists(path):
        return os.path.abspath(path)
    else:
        raise FileNotFoundError(f'The path "{path}" does not exist.')


def replace_ext(path: str, new_ext: str):
    path, current_ext = os.path.splitext(path)
    return path + new_ext


def copy_files(src_folder: str, dest_folder: str):
    for file in os.listdir(src_folder):
        shutil.copyfile(os.path.join(src_folder, file), os.path.join(dest_folder, file))

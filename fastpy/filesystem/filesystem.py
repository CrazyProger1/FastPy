import os
import shutil


class FileSystem:
    @staticmethod
    def read_file(filepath: str) -> str:
        with open(filepath, 'r') as f:
            return f.read()

    @staticmethod
    def write_file(filepath: str, content: str):
        with open(filepath, 'w') as f:
            f.write(content)

    @staticmethod
    def remove_quotes(path: str):
        for symbol in ['"', "'"]:
            path = path.replace(symbol, '')
        return path

    @staticmethod
    def normalize_path(path: str) -> str:
        path = FileSystem.remove_quotes(path)
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            raise FileNotFoundError(f'The path "{path}" does not exist.')

    @staticmethod
    def replace_ext(path: str, new_ext: str) -> str:
        path, current_ext = os.path.splitext(path)
        return path + new_ext

    @staticmethod
    def copy_files(src_folder: str, dest_folder: str):
        for file in os.listdir(src_folder):
            shutil.copyfile(os.path.join(src_folder, file), os.path.join(dest_folder, file))

    @staticmethod
    def get_filename_without_ext(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    @staticmethod
    def get_filename(path: str):
        return os.path.basename(path)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

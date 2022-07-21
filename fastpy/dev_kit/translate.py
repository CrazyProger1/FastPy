from fastpy.filesystem import FileSystem as Fs


def translate(source: str, **kwargs) -> str:
    source = Fs.normalize_path(source)
    source_code = Fs.read_file(source)

    return ''

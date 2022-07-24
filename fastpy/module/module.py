from ..filesystem import FileSystem as Fs


class Module:
    def __init__(self,
                 filepath: str,
                 name: str = None,
                 authoload: bool = True
                 ):

        self.filepath = filepath
        self.filename = Fs.get_filename_without_ext(self.filepath)
        self.name = name or self.filename
        self.source_code = ''

        if authoload:
            self.load_source()

    def load_source(self):
        if Fs.exists(self.filepath):
            with open(self.filepath, 'r') as sf:
                self.source_code = sf.read()

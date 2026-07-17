import pathlib
import os

class Importer:
    path = None
    absolutePath = ""
    relativePath = ""

    pathDir = None
    fileName = ""
    extension = ""
    
    def __init__(self, path: str):
        self.path = pathlib.Path(path)
        self.absolutePath = self.path.absolute()
        # self.relativePath = self.path.relative_to(os.getcwd())
        self.pathDir = self.path.parent

        if not self.path.is_dir():
            self.fileName = self.path.stem
            self.extension = self.path.suffix

    def getPath(self) -> pathlib.PurePath:
        return self.path
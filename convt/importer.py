"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

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
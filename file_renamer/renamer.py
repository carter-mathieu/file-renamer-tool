# -*- coding: utf-8 -*-
# file_rename/renamer.py

"""This module provides the enamer class to rename multiple files."""

import time
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

class Renamer(QObject):
    # define custom signals
    # return int of number of currently renamed file to update progress bar
    progressed = pyqtSignal(int)
    # return path of renamed file to update renamed files list in GUI
    renamedFile = pyqtSignal(Path)
    # signal process is done
    finished = pyqtSignal()

    def __init__(self, files, prefix, schar):
        super().__init__()
        # list of user selected files
        self._files = files
        # rename format to use to rename the files based on manhole or pipe selection
        self._prefix = prefix
        # get the character the user declared to split the file name on
        self._schar = schar

    def renameFiles(self):
        if self._prefix == None:
            pass

        if self._prefix == "manhole":
            index = 1
            for fileNumber, file in enumerate(self._files, 1):
                # skip the pipe segement folders
                if str(file).count(self._schar) > 1:
                    newFile = file.parent.joinpath(
                        f"Skipped: {str(file)}"
                    )
                else:
                    temp = str(file).split(self._schar)
                    new = self._schar.join(temp[:index])
                    newFile = file.parent.joinpath(
                        f"{new}"
                    )
                    file.rename(newFile)
                time.sleep(0.1)  # comment this line to rename files faster.
                self.progressed.emit(fileNumber)
                self.renamedFile.emit(newFile)
            self.progressed.emit(0)  # reset the progress
            self.finished.emit()
        
        if self._prefix == "pipe":
            index = 2
            for fileNumber, file in enumerate(self._files, 1):
                # skip the manhole folders
                if str(file).count(self._schar) > 2:
                    newFile = file.parent.joinpath(
                        f"Skipped: {str(file)}"
                    )
                else:
                    temp = str(file).split(self._schar)
                    new = self._schar.join(temp[:index])
                    newFile = file.parent.joinpath(
                        f"{new}"
                    )
                    file.rename(newFile)
                time.sleep(0.1)  # comment this line to rename files faster.
                self.progressed.emit(fileNumber)
                self.renamedFile.emit(newFile)
            self.progressed.emit(0)  # reset the progress
            self.finished.emit()
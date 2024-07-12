# -*- coding: utf-8 -*-
# file_renamer/views.py

"""This module provides the File Renamer Tool main window."""

from collections import deque
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QWidget

from .ui.window import Ui_Window

FILTERS = ";;".join(
    (
        "PNG Files (*.png)",
        "JPEG Files (*.jpeg)",
        "JPG Files (*.jpg)",
        "GIF Files (*.gif)",
        "Text Files (*.txt)",
        "SVG Files (*.svg)",
        "All Files (*)"
    )
)

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        # create ._files as a deque object. This attribute will store the paths to files to rename
        self._files = deque()
        # store the number of files to be renamed
        self._filesCount = len(self._files)
        self._setupUI()
        self._connectSignalsSlots()

    def _setupUI(self):
        self.setupUi(self)

    # collect several signal and slot connections in one place. Makes possible to trigger loadFiles on button click
    def _connectSignalsSlots(self):
        self.loadFilesButton.clicked.connect(self.loadFiles)
    
    def loadFiles(self):
        # clear the list widget on Load Files button click
        self.dstFileList.clear()
        # check if Last Source Directory element is populated
        # if true set the initial directory, initDir, to hold that path
        if self.dirEdit.text():
            initDir = self.dirEdit.text()
        # else initial directory is set to Path.home()
        else:
            initDir = str(Path.home())
        
        # allow the user to select one or more files and return a list of string-based paths to the selected files
        # files, filter = QFileDialog.getOpenFileNames(
        #     self, "Choose Files to Rename", initDir, filter=FILTERS
        # )

        # if there is a selection get to work renaming
        # if len(files) > 0:
        #     fileExtension = filter[filter.index("*") : -1]
        #     self.extensionLabel.setText(fileExtension)
        #     srcDirName = str(Path(files[0]).parent)
        #     self.dirEdit.setText(srcDirName)

        #     for file in files:
        #         self._files.append(Path(file))
        #         self.srcFileList.addItem(file)

        #     self._filesCount = len(self._files)

        # allow the user to select one or more folders and return a list of string-based paths to the selected files
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Rename Contents", initDir)

        if len(folder) > 0:
            srcDirName = str(Path(folder))
            print(srcDirName)
            self.dirEdit.setText(srcDirName)

            for subfolder in Path(folder).iterdir():
                if subfolder.is_dir():
                    print(str(Path(subfolder)))
                    self._files.append(Path(subfolder))
                    self.srcFileList.addItem(str(subfolder))

            self._filesCount = len(self._files)
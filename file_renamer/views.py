# -*- coding: utf-8 -*-
# file_renamer/views.py

"""This module provides the File Renamer Tool main window."""

from collections import deque
from pathlib import Path

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QWidget

from .renamer import Renamer
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
        self.renameFilesButton.clicked.connect(self.renameFiles)
    
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
    
    def renameFiles(self):
        self._runRenamerThread()
    
    def _runRenamerThread(self):
        # check if user is renaming manhole folders or pipes
        if self.manholeEdit.isChecked() == False and self.pipeSegmentEdit.isChecked == False:
            prefix = None
        if self.manholeEdit.isChecked():
            prefix = "manhole"
        if self.pipeSegmentEdit.isChecked():
            prefix = 'pipe'

        # get the split character user put into the field
        schar = self.splitChar.text()

        self._thread = QThread()
        self._renamer = Renamer(
            files=tuple(self._files),
            prefix=prefix,
            schar=schar,
        )
        self._renamer.moveToThread(self._thread)
        # Rename
        self._thread.started.connect(self._renamer.renameFiles)
        # Update state
        self._renamer.renamedFile.connect(self._updateStateWhenFileRenamed)
        # Clean up
        self._renamer.finished.connect(self._thread.quit)
        self._renamer.finished.connect(self._renamer.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()
    
    def _updateStateWhenFileRenamed(self, newFile):
        self._files.popleft()
        self.srcFileList.takeItem(0)
        self.dstFileList.addItem(str(newFile))
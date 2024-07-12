# -*- coding: utf-8 -*-
# file_renamer/views.py

"""This module provides the File Renamer Tool main window."""

from PyQt5.QtWidgets import QWidget

from .ui.window import Ui_Window

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self._setupUI()

    def _setupUI(self):
        self.setupUi(self)
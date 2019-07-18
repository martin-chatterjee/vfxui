# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level file browser widget.

import os
import time

from .pyside import QtCore, QtGui, QtWidgets

# =============================================================================
class FileBrowser(QtWidgets.QWidget):
    """
    """

    clicked = QtCore.Signal()

    # -------------------------------------------------------------------------
    def __init__(self,
                 label='',
                 dialog_caption='',
                 show_text=True,
                 button_label='...',
                 mode='open',
                 filters=[],
                 initialdir='',
                 selected_file=''):
        """
        """
        super(FileBrowser, self).__init__()

        # store settings
        self.mode = mode

        self.test_mode = None
        self.test_delay = 1 # seconds

        self.initialdir = initialdir
        if os.path.exists(self.initialdir) == False:
            self.initialdir = 'C:/Temp'

        self.selected_file = selected_file

        self.label = label
        self.dialog_caption = dialog_caption
        if self.dialog_caption == '':
            self.dialog_caption = self.label

        self.filters = filters
        default_filter = 'All Files (*.*)'
        if default_filter not in self.filters:
            self.filters.append(default_filter)

        self.filebrowser = QtWidgets.QFileDialog(
                                        self,
                                        caption=self.dialog_caption,
                                        directory=self.initialdir)
        self.filebrowser.setNameFilters(self.filters)
        if self.selected_file != '':
            self.filebrowser.selectFile(self.selected_file)

        self.__targetfolder = ''
        self.__targetfile = ''

        # deal with layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        activeLayout = self.layout

        if label != '':
            self.group = QtWidgets.QGroupBox(label)
            self.groupLayout = QtWidgets.QHBoxLayout()

            self.group.setLayout(self.groupLayout)

            activeLayout.addWidget(self.group)

            activeLayout = self.groupLayout

        self.text = QtWidgets.QLineEdit()
        self.text.setEnabled(False)
        self.text.setToolTip(self.dialog_caption)

        self.button = QtWidgets.QPushButton(button_label)
        # self.button.setFixedWidth(50)
        self.button.setToolTip(self.dialog_caption)

        if show_text == True:
            activeLayout.addWidget(self.text)
        activeLayout.addWidget(self.button)

        self.setLayout(self.layout)

        # connect button to slot
        self.button.clicked.connect(self.slot_released)

    # -------------------------------------------------------------------------
    @property
    def targetfolder(self):
        """
        """
        return self.__targetfolder

    # -------------------------------------------------------------------------
    @property
    def targetfile(self):
        """
        """
        return self.__targetfile

    # -------------------------------------------------------------------------
    @property
    def targetfilepath(self):
        """
        """
        return '%s/%s' % (self.targetfolder, self.targetfile)

    # -------------------------------------------------------------------------
    def showDialog(self, test_mode=None):
        """
        """
        path = ''

        if not test_mode is None:
            self.test_mode = test_mode

        # if not self.test_mode is None:
        #     t = QtCore.QTimer(None)
        #     if self.test_mode == 'reject':
        #         t.timeout.connect(self.filebrowser.reject)
        #     elif self.test_mode == 'accept':
        #         t.timeout.connect(self.filebrowser.accept)
        #     t.start(2000)

        if self.targetfolder != '':
            self.filebrowser.setDirectory(self.targetfolder)
        if self.targetfile != '':
            self.filebrowser.selectFile(self.targetfile)

        if self.mode == 'open':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        elif self.mode == 'save':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        elif self.mode == 'folder':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            self.filebrowser.setFileMode(QtWidgets.QFileDialog.Directory)

        status = False

        if self.test_mode is None: # pragma no cover
            status = self.filebrowser.exec_()
        else:
            self.filebrowser.show()
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.test_delay)
            if self.test_mode == 'accept':
                self.filebrowser.accept()
            else:
                self.filebrowser.reject()
            status = self.filebrowser.result()
        if status:
            path = self.filebrowser.selectedFiles()[0]

            # conform and process path
            path = path.replace('\\', '/').strip()

            if self.mode == 'folder':
                self.__targetfolder = path
                self.__targetfile = ''
            else:
                self.__targetfolder = os.path.dirname(path)
                self.__targetfile = os.path.basename(path)
        else:
            self.__targetfolder = ''
            self.__targetfile = ''

        self._updateText()

    # -------------------------------------------------------------------------
    def _updateText(self):
        """
        """
        content = self.targetfolder
        if self.targetfile != '':
            content += '/' + self.targetfile

        self.text.setText(content)

    # -------------------------------------------------------------------------
    def slot_released(self, **kwargs):
        """
        """
        self.showDialog(**kwargs)
        self.clicked.emit()


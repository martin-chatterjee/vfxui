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
                 direct_edit=False,
                 button_label='...',
                 mode='open',
                 filters=[],
                 initialdir='',
                 selected_file=''):
        """
        """

        super(FileBrowser, self).__init__()

        self.__targetfolder = ''
        self.__targetfile = ''

        # store settings
        self.mode = mode

        self.test_mode = None
        self.test_delay = 1 # seconds

        self.initialdir = initialdir
        if os.path.exists(self.initialdir) == False:
            self.initialdir = 'C:/Temp'
        if mode == 'folder':
            self.__targetfolder = self.initialdir

        self.selected_file = selected_file

        self.label = label
        self.dialog_caption = dialog_caption
        if self.dialog_caption == '':
            self.dialog_caption = self.label

        self.filters = filters
        default_filter = 'All Files (*.*)'
        if default_filter not in self.filters:
            self.filters.append(default_filter)

        self.__filebrowser = None

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
        if direct_edit is False:
            self.text.setEnabled(False)
        self.text.setToolTip(self.dialog_caption)
        self.text.setText(self.targetfilepath)
        self.text.editingFinished.connect(self.slot_text_editingFinished)

        self.button = QtWidgets.QPushButton(button_label)
        self.button.setFixedWidth(100)
        self.button.setToolTip(self.dialog_caption)

        if show_text == True:
            activeLayout.addWidget(self.text)
            activeLayout.addSpacing(5)
        activeLayout.addWidget(self.button)

        self.setLayout(self.layout)

        # connect button to slot
        self.button.clicked.connect(self.slot_released)

    # -------------------------------------------------------------------------
    @property
    def filebrowser(self):
        if self.__filebrowser is None:
            self.__filebrowser = QtWidgets.QFileDialog(
                                            self,
                                            caption=self.dialog_caption,
                                            directory=self.initialdir)
            self.__filebrowser.setNameFilters(self.filters)
            if self.selected_file != '':
                self.__filebrowser.selectFile(self.selected_file)

        return self.__filebrowser

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
        tfp = '%s/%s' % (self.targetfolder, self.targetfile)
        if tfp.endswith('/'):
            tfp = tfp[:-1]
        return tfp

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

    # -------------------------------------------------------------------------
    def slot_text_editingFinished(self, **kwargs):
        """
        """
        value = self.text.text()
        value = value.strip().replace(' ', '/').replace('\\', '/')
        if value.endswith('/'):
            value = value[:-1]
        while len(value) > 0 and not os.path.exists(value):
            tokens = value.split('/')
            value = '/'.join(tokens[:-1])

        self.text.setText(value)
        self.__targetfolder = value
        self.button.setFocus(QtCore.Qt.TabFocusReason)


    # -------------------------------------------------------------------------
    def setFixedHeight(self, height):
        self.text.setFixedHeight(height)
        self.button.setFixedHeight(height)

    # -------------------------------------------------------------------------
    def font(self):
        return self.text.font()

    # -------------------------------------------------------------------------
    def setFont(self, font):
        self.text.setFont(font)

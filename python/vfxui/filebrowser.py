# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level file browser widget.

import os
import time

from .pyside import QtCore, QtGui, QtWidgets

# -----------------------------------------------------------------------------
class FileBrowser(QtWidgets.QWidget):
    """
    """

    clicked = QtCore.Signal()
    updated = QtCore.Signal()

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
                 selected_file='',
                 multiselect=False):
        """
        """

        super(FileBrowser, self).__init__()

        self.__targetfolder = ''
        self.__targetfiles = ['']

        # store settings
        self.mode = mode
        self.__multiselect = False
        self.multiselect = multiselect
        self.__direct_edit = False

        self.test_mode = None
        self.test_delay = 1 # seconds

        self.initialdir = self._sanitizePath(initialdir)
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
        self.text.setEnabled(False)
        self.direct_edit = direct_edit
        self.text.setToolTip(self.dialog_caption)
        self.text.setText(self.targetfilepath)
        self.text.last_value = self.targetfilepath
        self.text.editingFinished.connect(self.slot_text_editingFinished)
        self.text.returnPressed.connect(self.slot_text_returnPressed)
        self.text.suppress_callback = False

        self.button = QtWidgets.QPushButton(button_label)
        self.button.setMinimumWidth(100)
        self.button.setToolTip(self.dialog_caption)

        if show_text == True:
            activeLayout.addWidget(self.text)
            activeLayout.addSpacing(5)
        activeLayout.addWidget(self.button)

        self.setLayout(self.layout)

        # connect button to slot
        self.button.released.connect(self.slot_released)


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
    def direct_edit(self):
        """
        """
        return self.__direct_edit

    @direct_edit.setter
    def direct_edit(self, value):
        self.__direct_edit = False
        if value is True and not self.multiselect:
            self.__direct_edit = True
        self.text.setEnabled(self.direct_edit)

    # -------------------------------------------------------------------------
    @property
    def multiselect(self):
        """
        """
        return self.__multiselect

    @multiselect.setter
    def multiselect(self, value):
        if value is True:
            self.__multiselect = True
        else:
            self.__multiselect = False

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
        if len(self.__targetfiles):
            return self.__targetfiles[0]
        return ''

    # -------------------------------------------------------------------------
    @property
    def targetfiles(self):
        """
        """
        return self.__targetfiles

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
    @property
    def targetfilepaths(self):
        """
        """
        filepaths = []
        for file in self.targetfiles:
            tfp = '%s/%s' % (self.targetfolder, file)
            if tfp.endswith('/'):
                tfp = tfp[:-1]
            filepaths.append(tfp)
        return filepaths

    # -------------------------------------------------------------------------
    def showDialog(self, test_mode=None):
        """
        """
        path = ''

        if test_mode:
            self.test_mode = test_mode

        if self.targetfolder != '':
            self.filebrowser.setDirectory(self.targetfolder)
        if self.targetfile != '':
            self.filebrowser.selectFile(self.targetfile)

        if self.mode == 'open':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            if self.multiselect:
                self.filebrowser.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            else:
                self.filebrowser.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        elif self.mode == 'save':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        elif self.mode == 'folder':
            self.filebrowser.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            self.filebrowser.setFileMode(QtWidgets.QFileDialog.Directory)

        status = False

        if not self.test_mode: # pragma no cover
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
            paths = self.filebrowser.selectedFiles()
            self.setPaths(paths)


    # -------------------------------------------------------------------------
    def setPath(self, path, emit_signal=True):
        """
        """
        self.setPaths([path, ], emit_signal=emit_signal)

    # -------------------------------------------------------------------------
    def setPaths(self, paths, emit_signal=True):
        """
        """
        conformed_paths = []
        file_names = []
        for path in paths:
            path = path.replace('\\', '/').strip()
            conformed_paths.append(path)
            file_names.append(os.path.basename(path))

        if self.mode == 'folder':
            self.__targetfolder = conformed_paths[0]
            self.__targetfiles = ['',]
        else:
            if os.path.isdir(conformed_paths[0]):
                self.__targetfolder = conformed_paths[0]
                self.__targetfiles = ['',]
            else:
                self.__targetfolder = os.path.dirname(conformed_paths[0])
                self.__targetfiles = file_names

        self._updateText()
        if emit_signal:
            self.updated.emit()

    # -------------------------------------------------------------------------
    def _updateText(self):
        """
        """
        content = self.targetfolder
        if self.targetfile != '':
            if len(self.targetfiles) > 1:
                files = list(self.targetfiles)[:3]
                if len(self.targetfiles) > 3:
                    files.append('...')
                content = '{}/[ {} ]'.format(content, ', '.join(files))
            else:
                content = self.targetfilepath

        self.text.suppress_callback = True
        self.text.setText(content)
        self.text.suppress_callback = False

    # -------------------------------------------------------------------------
    def slot_released(self, **kwargs):
        """
        """
        self.showDialog(**kwargs)
        self.clicked.emit()

    # -------------------------------------------------------------------------
    def slot_text_returnPressed(self, **kwargs):
        # pass
        self.button.setFocus(QtCore.Qt.TabFocusReason)

    # -------------------------------------------------------------------------
    def slot_text_editingFinished(self, **kwargs):
        """
        """
        if self.text.last_value == self.text.text():
            return
        if self.text.suppress_callback:
            return
        path = self._sanitizePath(self.text.text())
        self.setPath(path)
        self.text.last_value = path
        # self.text.setText(path)
        # self.__targetfolder = path
        # self.button.setFocus(QtCore.Qt.TabFocusReason)

    # -------------------------------------------------------------------------
    def _sanitizePath(self, path):
        """
        """
        path = path.strip().replace(' ', '/').replace('\\', '/')
        if path.endswith('/'):
            path = path[:-1]
        while len(path) > 0 and not os.path.exists(path):
            tokens = path.split('/')
            path = '/'.join(tokens[:-1])
        return path

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

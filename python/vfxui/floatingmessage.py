# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief

from .pyside import QtCore, QtGui, QtWidgets

# -----------------------------------------------------------------------------
class FloatingMessage(QtWidgets.QWidget):
    """
    """

    # -------------------------------------------------------------------------
    def __init__(self, parent=None, **kwargs):
        """
        """
        super(FloatingMessage, self).__init__(parent=parent)
        self._message = ''
        self.top = None

        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(text='', parent=self)
        self.label.setProperty('labelClass', 'FloatingMessage')

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()
        self.hide()

    # -------------------------------------------------------------------------
    def show(self, message='', duration=3.0):
        """
        """
        if self.isVisible():
            self.hide()
        self.label.setFixedWidth(1)
        self.label.setText(message)
        new_width = self.label.sizeHint().width()
        self.label.setFixedWidth(new_width)
        self.label.setStyle(self.label.style())
        self.updatePosition()
        super(FloatingMessage, self).show()
        QtCore.QCoreApplication.processEvents()

        if duration:
            QtCore.QTimer.singleShot(duration * 1000.0, self.hide)


    # -------------------------------------------------------------------------
    def updatePosition(self):
        """
        """
        window = self.parent().geometry()
        window_x = window.x()
        window_width = window.width()
        label_width = self.label.width()
        progress_x = window_x + (window_width * 0.5) - (label_width * 0.5)

        window_y = window.y()
        window_height = window.height()
        offset_y = (window_height / 1.618)
        if self.top:
            offset_y = self.top
        progress_y = window_y + offset_y

        self.move(progress_x, progress_y)

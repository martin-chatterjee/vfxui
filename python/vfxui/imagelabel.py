# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level clickable image label widget.

import os

from .pyside import QtCore, QtGui, QtWidgets


# =============================================================================
class ImageLabel(QtWidgets.QLabel):
    """
    """

    clicked = QtCore.Signal()

    # -------------------------------------------------------------------------
    def __init__(self, image, image_hi=None, working_dir=None, parent=None):
        """
        """
        QtWidgets.QLabel.__init__(self, parent)

        self.image = image
        self.image_hi = image_hi

        self.setPixmap(self.image)

        self.working_dir = working_dir

    # -------------------------------------------------------------------------
    def enterEvent(self, event):
        """
        """
        if self.image_hi is not None:
            self.setPixmap(self.image_hi)

    # -------------------------------------------------------------------------
    def swapImage(self, image_path):

        image_path = self.conformPath(image_path)
        self.image = QtGui.QPixmap(image_path)
        self.setPixmap(self.image)
        QtCore.QCoreApplication.processEvents()

    # -------------------------------------------------------------------------
    def conformPath(self, path):
        """
        """
        if not self.working_dir is None:
            if os.path.exists(self.working_dir):
                wd = os.getcwd()
                os.chdir(self.working_dir)
                path = os.path.abspath(path)
                os.chdir(wd)

        path = os.path.expandvars(path)
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[:-1]

        return path

    # -------------------------------------------------------------------------
    def leaveEvent(self, event):
        """
        """
        if self.image_hi is not None:
            self.setPixmap(self.image)

    # -------------------------------------------------------------------------
    def mousePressEvent(self, event):
        """
        """
        self.setPixmap(self.image)
        self.clicked.emit()

    # -------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        """
        """
        if self.image_hi is not None:
            self.setPixmap(self.image_hi)



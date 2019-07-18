# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level clickable image label widget.

from .pyside import QtCore, QtGui, QtWidgets


# =============================================================================
class ListBox(QtWidgets.QListWidget):
    """
    """
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        """
        self.__ignore_keypress = False

        super(ListBox, self).__init__(*args, **kwargs)

    # -------------------------------------------------------------------------
    @property
    def ignore_keypress(self):
        """
        """
        return self.__ignore_keypress

    # -------------------------------------------------------------------------
    @ignore_keypress.setter
    def ignore_keypress(self, value):
        """
        """
        if value == True:
            self.__ignore_keypress = True
        else:
            self.__ignore_keypress = False


    # -------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """
        """
        result = self.keyPressed.emit(event)

        if not self.ignore_keypress:
            super(ListBox, self).keyPressEvent(event)


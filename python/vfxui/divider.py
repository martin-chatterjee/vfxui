# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level clickable image label widget.

from .pyside import QtCore, QtGui, QtWidgets

# -----------------------------------------------------------------------------
class Divider(QtWidgets.QWidget):
    """
    """

    # -------------------------------------------------------------------------
    def __init__(self, horizontal=True, thickness=1, align='center', **kwargs):
        """
        """
        super(Divider, self).__init__()

        self.line = QtWidgets.QFrame()
        self.line.setLineWidth(thickness)
        if horizontal:
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFixedHeight(thickness)
        else:
            self.line.setFrameShape(QtWidgets.QFrame.VLine)
            self.line.setFixedWidth(thickness)

        explicit_width_height = 'width' in kwargs or 'height' in kwargs

        # build and fill layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        if align == 'right' and explicit_width_height:
            self.layout.addStretch()
        if not horizontal:
            self.layout.addSpacing(10)

        self.layout.addWidget(self.line)

        if not horizontal:
            self.layout.addSpacing(10)

        if align == 'left' and explicit_width_height:
            self.layout.addStretch()

        self.setLayout(self.layout)

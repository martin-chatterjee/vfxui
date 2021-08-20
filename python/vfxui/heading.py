# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief High level clickable image label widget.

import os
import logging

from .pyside import QtCore, QtGui, QtWidgets


logger = logging.getLogger('vfxui')


# -----------------------------------------------------------------------------
class Heading(QtWidgets.QWidget):
    """
    """

    # -------------------------------------------------------------------------
    def __init__(self,
                 label,
                 size='h1',
                 indent=0,
                 parent=None):
        """
        """
        QtWidgets.QWidget.__init__(self, parent)

        if not size in ['h1', 'h2', 'h3']:
            logger.warning("Not supported: '{}' Defaulting to 'h2'.")
            size = 'h2'

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.indent = QtWidgets.QLabel()
        self.indent.setFixedWidth(indent)
        self.indent.setProperty('labelClass', '{}_indent'.format(size))
        self.layout.addWidget(self.indent)

        self.label = QtWidgets.QLabel(label)
        self.label.setProperty('labelClass', '{}_label'.format(size))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)

        self.layout.addWidget(self.label)

        self.line = QtWidgets.QLabel()
        self.line.setProperty('labelClass', '{}_line'.format(size))
        self.layout.addWidget(self.line)


        self.setLayout(self.layout)



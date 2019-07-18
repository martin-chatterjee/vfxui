# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

# try to import PySide2, fall back to PySide
QtCore = None
QtGui = None
QtWidgets = None
QtTest = None

try:
    import PySide2.QtCore as PS2_QtCore
    QtCore = PS2_QtCore
    import PySide2.QtGui as PS2_QtGui
    QtGui = PS2_QtGui
    import PySide2.QtWidgets as PS2_QtWidgets
    QtWidgets = PS2_QtWidgets
    import PySide2.QtTest as PS2_QtTest
    QtTest = PS2_QtTest

except ImportError:
    import PySide.QtCore as PS_QtCore
    QtCore = PS_QtCore
    import PySide.QtGui as PS_QtGui
    QtGui = PS_QtGui
    QtWidgets = PS_QtGui
    import PySide.QtTest as PS_QtTest
    QtTest = PS_QtTest


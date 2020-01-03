# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

# try to import PySide2, fall back to PySide
QtCore = None
QtGui = None
QtWidgets = None
QtTest = None
is_pyside2 = True
shiboken = None
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
    is_pyside2 = False
    import PySide.QtCore as PS_QtCore
    QtCore = PS_QtCore
    import PySide.QtGui as PS_QtGui
    QtGui = PS_QtGui
    QtWidgets = PS_QtGui
    import PySide.QtTest as PS_QtTest
    QtTest = PS_QtTest

try:
    import shiboken2 as PS2_shiboken
    shiboken = PS2_shiboken
except ImportError:
    try:
        import shiboken as PS_shiboken
        shiboken = PS_shiboken # pragma: no cover
    except ImportError:
        pass

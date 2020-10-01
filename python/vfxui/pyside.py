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
shiboken = None

uses_sgtk_imports = False
is_pyside2 = False

# prefer sgtk PySide2/Qt5
try:
    uses_sgtk_imports = True
    is_pyside2 = True
    from sgtk.platform.qt5 import QtCore as sg_qt5_QtCore
    QtCore = sg_qt5_QtCore
    from sgtk.platform.qt5 import QtGui as sg_qt5_QtGui
    QtGui = sg_qt5_QtGui
    from sgtk.platform.qt5 import QtWidgets as sg_qt5_QtWidgets
    QtWidgets = sg_qt5_QtWidgets
    # catch issue with Maya + Houdini Engine where QtTest is not importable
    try:
        from sgtk.platform.qt5 import QtTest as sg_qt5_QtTest
        QtTest = sg_qt5_QtTest
    except ImportError: # pragma: no cover
        pass

except ImportError:
    # fall back to sgtk PySide/Qt4
    try:
        uses_sgtk_imports = True
        is_pyside2 = False
        from sgtk.platform.qt import QtCore as sg_qt_QtCore
        QtCore = sg_qt_QtCore
        from sgtk.platform.qt import QtGui as sg_qt_QtGui
        QtGui = sg_qt_QtGui
        QtWidgets = sg_qt_QtGui
        # catch issue with Maya + Houdini Engine where QtTest is not importable
        try:
            from sgtk.platform.qt import QtTest as sg_qt_QtTest
            QtTest = sg_qt_QtTest
        except ImportError: # pragma: no cover
            pass

    except ImportError:
        # then prefer PySide2
        try:
            uses_sgtk_imports = False
            is_pyside2 = True
            import PySide2.QtCore as PS2_QtCore
            QtCore = PS2_QtCore
            import PySide2.QtGui as PS2_QtGui
            QtGui = PS2_QtGui
            import PySide2.QtWidgets as PS2_QtWidgets
            QtWidgets = PS2_QtWidgets
            # catch issue with Maya + Houdini Engine where QtTest is not importable
            try:
                import PySide2.QtTest as PS2_QtTest
                QtTest = PS2_QtTest
            except ImportError: # pragma: no cover
                pass

        except ImportError:
            # fall back to PySide
            try:
                uses_sgtk_imports = False
                is_pyside2 = False
                import PySide.QtCore as PS_QtCore
                QtCore = PS_QtCore
                import PySide.QtGui as PS_QtGui
                QtGui = PS_QtGui
                QtWidgets = PS_QtGui
                try:
                    import PySide.QtTest as PS_QtTest
                    QtTest = PS_QtTest
                except ImportError: # pragma: no cover
                    pass

            except ImportError:
                # giving up...
                pass

try:
    import shiboken2 as PS2_shiboken
    shiboken = PS2_shiboken
except ImportError:
    try:
        import shiboken as PS_shiboken
        shiboken = PS_shiboken # pragma: no cover
    except ImportError:
        pass

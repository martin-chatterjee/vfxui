# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# -----------------------------------------------------------------------------

import os
import sys
import time
import importlib
import imp

import vfxui.dialog as dlg

from vfxui.pyside import QtCore, QtGui, QtWidgets, QtTest
QTest = QtTest.QTest

from vfxui.dialog import Dialog, createDialog, ListRow
from complexDialog import ComplexDialog

from vfxtest import TestCase, mock

# -----------------------------------------------------------------------------
class FloatingMessage_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        cls.display_length = 100
        cls.time_between_emits = 0.2
        cls.delay = 20

    # -------------------------------------------------------------------------
    @classmethod
    def tearDownOnce(cls):
        pass
    # -------------------------------------------------------------------------
    def setUp(self):
        pass

    # -------------------------------------------------------------------------
    def tearDown(self):
        pass

    # -------------------------------------------------------------------------
    def test01_dialog_with_floating_message(self):

        dlg = createDialog(width=400,
                           height=800,
                           # test_mode='ok',
                           test_display_length=self.display_length)

        fm = dlg.createFloatingMessage()
        dlg.show()
        dlg.redraw()
        time.sleep(self.time_between_emits)
        fm.show('Foo')
        dlg.redraw()
        time.sleep(self.time_between_emits)
        dlg.move(dlg.geometry().x() + 100, dlg.geometry().y())
        fm.show('Bar')
        dlg.redraw()
        time.sleep(self.time_between_emits)
        dlg.resize(600, 200)
        fm.show('Really long text')
        dlg.redraw()
        time.sleep(self.time_between_emits)
        fm.show('x')
        dlg.redraw()
        time.sleep(self.time_between_emits)
        fm.hide()

        dlg.close()
        dlg = None

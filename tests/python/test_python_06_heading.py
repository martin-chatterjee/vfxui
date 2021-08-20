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
class Heading_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        cls.test_display_length = 1000
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
    def test01_heading(self):

        dlg = createDialog(width=400,
                           height=800,
                           test_mode='ok',
                           test_display_length=self.test_display_length)

        h1 = dlg.addHeading(label='My Heading')
        h3 = dlg.addHeading(label='subhead', size='h3', indent=50)
        defaults_to_h2 = dlg.addHeading(label='defaults_to_h2', size='crap')

        dlg.showModal()


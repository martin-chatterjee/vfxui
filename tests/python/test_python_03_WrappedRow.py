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

from vfxui.dialog import Dialog, createDialog, WrappedRowLayout

from vfxtest import TestCase, mock

# -----------------------------------------------------------------------------
class WrappedRow_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        cls.display_length = 100
        cls.time_between_emits = .1
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
    def test01_openWrappedRow(self):

        # with mock.patch('vfxui.dialog.WrappedRowLayout.smartSpacing', return_value=0):
        dlg = createDialog(width=200,
                           test_mode='ok',
                           test_display_length=self.display_length)

        wr_a = dlg.openWrappedRow(hspacing=3, vspacing=4, margin=5)
        for i in range(30):
            dlg.addLabel(label=str(i), width=30)
            dlg.addSpacer(10)
        dlg.closeWrappedRow()
        wr_b = dlg.openWrappedRow()
        for i in range(30):
            dlg.addLabel(label='{}-{}'.format(i, i), width=50)
        dlg.closeWrappedRow()
        wr_c = dlg.openWrappedRow()
        for i in range(30):
            dlg.addLabel(label='{}|{}'.format(i, i), width=50)
        dlg.closeWrappedRow()
        wr_c.layout().takeAt(0)
        dlg.showModal()

        self.assertEqual(wr_a.layout().horizontalSpacing(), 3)
        self.assertEqual(wr_a.layout().verticalSpacing(), 4)
        self.assertEqual(wr_a.layout().direction(), QtWidgets.QBoxLayout.LeftToRight)
        self.assertNotEqual(wr_b.layout().horizontalSpacing(), 3)
        self.assertNotEqual(wr_b.layout().verticalSpacing(), 4)
        self.assertEqual(len(wr_c.layout()._items), 29)

    # -------------------------------------------------------------------------
    def test02_doLayout_Coverage(self):

        with mock.patch('vfxui.dialog.WrappedRowLayout.horizontalSpacing', return_value=-1):
            with mock.patch('vfxui.dialog.WrappedRowLayout.verticalSpacing', return_value=-1):
                dlg = createDialog(width=200,
                                   test_mode='ok',
                                   test_display_length=self.display_length)

                wr_a = dlg.openWrappedRow(hspacing=3, vspacing=4, margin=5)
                for i in range(30):
                    dlg.addLabel(label=str(i), width=30)
                    dlg.addSpacer(10)
                dlg.closeWrappedRow()
                dlg.showModal()


    # -------------------------------------------------------------------------
    def test02_smartSpacing_Coverage(self):

        with mock.patch('vfxui.dialog.WrappedRowLayout.parent', return_value=None):
            dlg = createDialog(width=200,
                               test_mode='ok',
                               test_display_length=self.display_length)

            wr_a = dlg.openWrappedRow(hspacing=3, vspacing=4, margin=5)
            for i in range(30):
                dlg.addLabel(label=str(i), width=30)
                dlg.addSpacer(10)
            dlg.closeWrappedRow()
            dlg.showModal()

            self.assertEqual(wr_a.layout().smartSpacing(None), -1)

        with mock.patch('vfxui.dialog.WrappedRowLayout.parent',
                         return_value=mock.Mock(
                                isWidgetType=mock.Mock(return_value=False))):
            dlg = createDialog(width=200,
                               test_mode='ok',
                               test_display_length=self.display_length)

            wr_a = dlg.openWrappedRow(hspacing=3, vspacing=4, margin=5)
            for i in range(30):
                dlg.addLabel(label=str(i), width=30)
                dlg.addSpacer(10)
            dlg.closeWrappedRow()
            dlg.showModal()

            self.assertNotEqual(wr_a.layout().smartSpacing(None), -1)

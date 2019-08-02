# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
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

# =============================================================================
class ListBox_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        cls.display_length = 1000
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
    def test01_listbox_with_filter(self):

        dlg = createDialog(width=400,
                           height=800,
                           # test_mode='ok',
                           test_display_length=self.display_length)

        lb = dlg.addListBox(filtering=True,
                            multiselect=True,
                            selection_controls=True,
                            selection_control_position='invalid',
                            placeholder='Search here')
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        self.assertEqual(lb.count(), 3)
        self.assertEqual(len(lb.visibleItems()), 3)
        self.assertEqual(len(lb.selectedItems()), 0)
        time.sleep(self.time_between_emits)


        QTest.keyClicks(lb.filter.filter_line, 'zz', delay=self.delay)
        QTest.keyPress(lb.filter.filter_line, QtCore.Qt.Key_Tab, delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)

        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.visibleItems()), 2)
        self.assertEqual(len(lb.selectedItems()), 1)
        self.assertEqual(lb.selectedItems()[0].text(), 'fizz')
        self.assertEqual(lb.getFilterTokens(), ['zz',])

        QTest.mouseClick(lb.btn_invert,
                         QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(5,5),
                         delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.selectedItems()), 1)
        self.assertEqual(lb.selectedItems()[0].text(), 'buzz')

        QTest.mouseClick(lb.btn_all,
                         QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(5,5),
                         delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.selectedItems()), 2)

        QTest.mouseClick(lb.btn_none,
                         QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(5,5),
                         delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.selectedItems()), 0)

        self.assertEqual(len(lb.visibleItems()), 2)
        QTest.mouseClick(lb.filter.clear_icon,
                         QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(3,3),
                         delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.visibleItems()), 3)

        QTest.keyPress(lb.list, QtCore.Qt.Key_Down, delay=self.display_length)
        QTest.keyPress(lb.list, QtCore.Qt.Key_Return, delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)

        lb.filter.setText('foo bar')
        self.assertEqual(lb.getFilterTokens(), ['foo', 'bar'])
        lb.filter.clear()

        dlg.redraw()
        time.sleep(self.time_between_emits)

        # we should probably test those properly in the future...
        lb.list.itemClicked.emit(lb.item(0))
        lb.list.itemDoubleClicked.emit(lb.item(1))
        lb.list.itemPressed.emit(lb.item(1))
        lb.list.itemEntered.emit(lb.item(1))
        lb.list.itemChanged.emit(lb.item(1))


        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test02_listbox_inline_controls(self):

        dlg = createDialog(width=400,
                           height=800,
                           # test_mode='ok',
                           test_display_length=self.display_length)

        lb = dlg.addListBox(filtering=True,
                            multiselect=True,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='inline',
                            placeholder='Search here')
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)


        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test03_listbox_center_controls(self):

        dlg = createDialog(width=400,
                           height=800,
                           # test_mode='ok',
                           test_display_length=self.display_length)

        lb = dlg.addListBox(filtering=True,
                            multiselect=True,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='center',
                            placeholder='Search here')
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)


        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test04_listbox_right_controls(self):

        dlg = createDialog(width=400,
                           height=800,
                           # test_mode='ok',
                           test_display_length=self.display_length)

        lb = dlg.addListBox(filtering=True,
                            multiselect=True,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='right',
                            placeholder='Search here')
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)

        QTest.keyClicks(lb.filter.filter_line, 'lorem ipsum', delay=self.delay)
        QTest.keyPress(lb.filter.filter_line, QtCore.Qt.Key_Return, delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)

        self.assertEqual(len(lb.visibleItems()), 0)
        dlg.close()
        dlg = None



    # -------------------------------------------------------------------------
    def test05_listbox_removeSelection(self):

        dlg = createDialog(width=400,
                           height=800,
                           test_display_length=self.display_length)


        lb = dlg.addListBox(filtering=True,
                            multiselect=True,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='inline')
        lb.ignore_keypress = True
        self.assertTrue(lb.ignore_keypress)
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)

        QTest.mouseClick(lb.btn_all,
                         QtCore.Qt.LeftButton,
                         pos=QtCore.QPoint(5,5),
                         delay=self.display_length)
        dlg.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(len(lb.selectedItems()), 3)
        lb.removeSelection()
        self.assertEqual(len(lb.selectedItems()), 0)

        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test06_listbox_removeItem(self):

        dlg = createDialog(width=400,
                           height=800,
                           test_display_length=self.display_length)


        lb = dlg.addListBox(filtering=True,
                            multiselect=False,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='inline')
        lb.ignore_keypress = True
        self.assertTrue(lb.ignore_keypress)
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)

        lb.removeItem('fizz')
        self.assertEqual(lb.count(), 2)
        self.assertEqual(lb.item(1).text(),'buzz')
        self.assertEqual(lb.item(1).index, 1)
        dlg.redraw()
        time.sleep(1)

        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test07_listbox_addItem_text_or_widget_or_listrow(self):

        dlg = createDialog(width=400,
                           height=800,
                           test_display_length=self.display_length)


        lb = dlg.addListBox(filtering=False,
                            multiselect=False,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='inline',
                            min_height=200,
                            font='Arial',
                            font_size=20,
                            font_weight='light',
                            font_spacing=0.1,
                            )
        lb.ignore_keypress = True
        self.assertTrue(lb.ignore_keypress)
        lb.addItems(['foo', 'fizz', 'buzz'])

        dlg.show()
        dlg.redraw()
        time.sleep(1)

        lb.addItem('yeah')
        self.assertEqual(lb.count(), 4)

        lb.addItem(QtWidgets.QLabel('fff'))
        self.assertEqual(lb.count(), 5)

        custom_row = ListRow(value='Boooooo', tooltip='Awesome Tip')
        lb.addItem(custom_row)
        self.assertEqual(lb.count(), 6)
        self.assertEqual(lb.item(5).text(), 'Boooooo')
        lb.item(5).setText('Aaaargh')
        self.assertEqual(lb.item(5).text(), 'Aaaargh')
        dlg.redraw()
        time.sleep(1)

        dlg.close()
        dlg = None

    # -------------------------------------------------------------------------
    def test08_listbox_listrows(self):

        dlg = createDialog(width=400,
                           height=800,
                           test_display_length=self.display_length)


        lb = dlg.addListBox(filtering=True,
                            multiselect=False,
                            filter_row_height=20,
                            selection_controls=True,
                            selection_control_position='inline',
                            min_height=200,
                            font='Arial',
                            font_size=20,
                            font_weight='light',
                            font_spacing=0.1,
                            )

        custom_row = ListRow(value='Boooooo', tooltip='Awesome Tip', keywords='foobar')
        lb.addItem(custom_row)
        dlg.show()
        self.assertEqual(lb.count(), 1)
        self.assertEqual(len(lb.visibleItems()), 1)

        lb.filter.setText('foo')
        dlg.redraw()
        time.sleep(1)
        self.assertEqual(len(lb.visibleItems()), 1)

        self.assertEqual(custom_row.listbox, lb)
        self.assertEqual(str(custom_row.listrow), str(lb.item(0)))

        dlg.close()
        dlg = None

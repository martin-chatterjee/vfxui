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
from vfxui.dialog import Dialog, createDialog, deleteDialog, ListRow
from complexDialog import ComplexDialog

from vfxtest import TestCase, mock

QTest = QtTest.QTest


# -----------------------------------------------------------------------------
class UI_Dialog_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        dlg.initLogging(format='')

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
    def test01_context(self):

        self.assertEqual(Dialog._context, None)
        foo = dlg.createDialog()
        Dialog._context = None
        self.assertEqual(foo.context, 'python')
        self.assertEqual(Dialog._context, 'python')

        Dialog._context = None
        with mock.patch('sys.executable', 'C:/foo/bar/mayabatch.exe'):
            bar = dlg.createDialog()
            self.assertEqual(bar.context, 'maya')
        Dialog._context = None

        Dialog._context = None

        with mock.patch('sys.executable', 'C:/foo/bar/nuke11.3.exe'):
            with mock.patch.dict('sys.modules',
                {'nuke' : mock.Mock(
                            env=mock.Mock(
                                __getitem__=mock.Mock(
                                    return_value='studio')))
                }
            ):
                bar = dlg.createDialog()
                self.assertEqual(bar.context, 'nukestudio')

        Dialog._context = None


    # -------------------------------------------------------------------------
    def test02_divider(self):

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        dialog.addLabel(label='above')
        dialog.addDivider() # <-- default thickness = 1
        dialog.addLabel(label='below')
        dialog.addDivider(width=150, thickness=2, align='left')
        dialog.addDivider(width=150, thickness=2, align='right')
        dialog.addDivider(width=150, thickness=2, align='center')
        dialog.addSpacer(30)
        dialog.openRow()
        dialog.addLabel(label='left')
        dialog.addDivider(horizontal=False, thickness=30, height=50)
        dialog.addLabel(label='right')
        dialog.addStretch()
        dialog.closeRow()
        dialog.addStretch()

        ret_val = dialog.showModal()
        self.assertFalse(ret_val)

        deleteDialog(dialog)
        dialog = None

    # -------------------------------------------------------------------------
    def test03_imagelabel(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True)
        # dialog.setWorkingDir(__file__)
        dialog.addSpacer(30)
        img = dialog.addImage(image_path='%s/green.png' % basepath,
                        image_path_hi='%s/red.png' % basepath,
                        width=200,
                        height=50)
        img_id = dialog.getWidgetId(img)
        dialog.addSpacer(30)
        img2 = dialog.addImage(image_path=None)
        img_id2 = dialog.getWidgetId(img2)

        dialog.addSpacer(30)

        image = dialog.getWidget(img_id)

        dialog.show()
        QtTest.QTest.mouseMove(image,
                               pos=QtCore.QPoint(10,10),
                               delay=self.display_length)
        QtTest.QTest.mouseMove(image,
                               pos=QtCore.QPoint(10,400),
                               delay=self.display_length)
        QtTest.QTest.mouseClick(image,
                                QtCore.Qt.LeftButton,
                                pos=QtCore.QPoint(10,10),
                                delay=self.display_length)

        img.swapImage(image_path='%s/red.png' % basepath)

        time.sleep(self.time_between_emits)
        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test07_createSimpleDialog(self):

        dialog = dlg.createDialog(title='Awesome Dialog', width=400,
                                  height=100, fixed_size=False,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        # on the fly layout
        headline = dialog.addHeadline('Headline')
        group = dialog.openGroup('FOO')
        widget_a = dialog.addTextBox(widget_id='awesome_A',
                                        value='Hello Pyside!!',
                                        label='foo',
                                        label_width=100,
                                        width=300)
        dialog.addSpacer(30)
        row = dialog.openRow()
        widget_b = dialog.addTextBox(widget_id='awesome_A',
                                        label='BOOYA',
                                        labelclass='css_class',
                                        width=100)
        widget_b.setText('AA')
        widget_c = dialog.addTextBox(widget_id='awesome_A',
                                        value = 'XXX')

        self.assertEqual(dialog.getWidgetId(widget_a), 'awesome_a')
        self.assertEqual(dialog.getWidgetId(widget_b), 'awesome_a_1')
        self.assertEqual(dialog.getWidgetId(widget_c), 'awesome_a_2')
        ret_val = dialog.showModal()

        self.assertEqual(ret_val, True)
        self.assertEqual(dialog.title, 'Awesome Dialog')
        self.assertEqual(dialog.width, 400)
        self.assertEqual(dialog.height, 100)
        self.assertEqual(dialog.fixed_size, False)

        self.assertEqual(dlg.Dialog._context, dialog.context)

        dialog = None

    # -------------------------------------------------------------------------
    def test07_printWidgetDetails(self):

        dialog = dlg.createDialog(title='Awesome Dialog', width=400,
                                  height=100, fixed_size=False,
                                  test_mode=False,
                                  test_display_length=self.display_length)

        widget_b = dialog.addTextBox(widget_id='myTextBox',
                                        label='BOOYA',
                                        labelclass='css_class',
                                        width=100)

        details = dialog.getWidgetDetails(widget_b)
        self.assertEqual(details['id'], 'mytextbox')
        self.assertEqual(details['type'], 'QLineEdit')
        self.assertTrue('signals' in details)
        self.assertTrue('returnPressed' in details['signals'])

    # -------------------------------------------------------------------------
    def test08_createDialog_disable_return_escape(self):


        dialog = dlg.createDialog(title='Awesome Dialog')
        self.assertFalse(dialog.disable_return_escape)
        dialog = dlg.createDialog(title='Awesome Dialog', no_return_escape=True)
        self.assertTrue(dialog.disable_return_escape)

        dialog.disable_return_escape = False
        self.assertFalse(dialog.disable_return_escape)
        self.assertFalse(dialog.disable_return)
        self.assertFalse(dialog.disable_escape)

        dialog.disable_return_escape = True
        self.assertTrue(dialog.disable_return_escape)
        self.assertTrue(dialog.disable_return)
        self.assertTrue(dialog.disable_escape)

        dialog.disable_return = False
        self.assertFalse(dialog.disable_return_escape)
        self.assertFalse(dialog.disable_return)
        self.assertTrue(dialog.disable_escape)

        dialog.disable_escape = False
        self.assertFalse(dialog.disable_return_escape)
        self.assertFalse(dialog.disable_return)
        self.assertFalse(dialog.disable_escape)

        dialog = None

    # -------------------------------------------------------------------------
    def test09_createDialogUnknownContextUsesOwnQApplication(self):

        Dialog._context = 'unknown'
        try:
            dialog = dlg.createDialog(title='Awesome Dialog',
                                      width=400,
                                      height=100,
                                      test_mode=False,
                                      test_display_length=self.display_length)

            self.assertTrue(isinstance(dialog, dlg.Dialog))
        finally:
            Dialog._context = None

    # -------------------------------------------------------------------------
    def test10_createDialog_invalidTestDisplayLength(self):


        dialog = dlg.createDialog(title='Awesome Dialog',
                                  width=400,
                                  height=100,
                                  test_mode=False,
                                  test_display_length='invalid')

        self.assertEqual(dialog.test_display_length, None)

        dialog = None

    # -------------------------------------------------------------------------
    def test11_createDialog_close_lastViewModal(self):

        dialog = dlg.createDialog(title='Awesome Dialog 11',
                                  width=400,
                                  height=100,
                                  test_mode='Cancel',
                                  test_display_length=self.display_length)


        status = dialog.showModal()
        self.assertTrue(status)
        self.assertEqual(dialog.last_view_modal, True)

        dialog.test_display_length = None
        dialog.show()
        time.sleep(self.time_between_emits)
        dialog.redraw()
        dialog.close()
        self.assertEqual(dialog.last_view_modal, False)

        dialog = None

    # -------------------------------------------------------------------------
    def test12_createDialog_close_lastViewModal(self):


        dialog = dlg.createDialog(title='Awesome Dialog 12',
                                  width=400,
                                  height=100,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        label = dialog.addLabel(label='foo', width=100)
        self.assertNotEqual(label, None)
        label_id = dialog.getWidgetId(label)
        dialog.clear()
        label = dialog.getWidget(label_id)
        self.assertEqual(label, None)
        dialog.showModal()

        dialog = None

    # -------------------------------------------------------------------------
    def test13_createDialog_sizeFlags(self):

        dialog = dlg.createDialog(title='Awesome Dialog',
                                  width='crap',
                                  height='crap',
                                  fixed_size=True,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        dialog.setWidthHeight(300, 600)
        self.assertEqual(dialog.width, 300)
        self.assertEqual(dialog.height, 600)

        ret_val = dialog.showModal()
        self.assertTrue(ret_val)

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test14_DialogBase_createUniqueWidgetId(self):

        dialog = dlg.createDialog()

        result = dialog._createUniqueWidgetId(widget_id='')
        self.assertEqual(result, 'unnamed_widget')
        result = dialog._createUniqueWidgetId(widget_id=None)
        self.assertEqual(result, 'unnamed_widget')

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test15_DialogBase_storeWidget(self):


        dialog = dlg.createDialog(test_mode='ok',
                                  test_display_length=self.display_length)

        widget = QtWidgets.QLabel('foo')
        widget_id = dialog._storeWidget(widget, widget_id='')
        self.assertEqual(widget_id, 'unnamed_widget')
        ret_val = dialog.showModal()
        self.assertTrue(ret_val)

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test16_create_called_multiple_times(self):

        dialog = dlg.createDialog(test_mode='ok',
                                  test_display_length=self.display_length)

        ret_val = dialog.showModal()
        dialog.test_display_length = None
        dialog.show()
        time.sleep(self.time_between_emits)
        dialog.show()
        time.sleep(self.time_between_emits)
        dialog.close()
        self.assertTrue(ret_val)

        dialog = None

    # -------------------------------------------------------------------------
    def test17_activateWindow_fails_without_exception(self):

        def throwsError(self):
            raise Exception

        try:
            patch = mock.patch('PySide2.QtWidgets.QWidget.activateWindow',
                                side_effect=Exception())
            patch.start()
        except Exception:
            patch = mock.patch('PySide.QtGui.QDialog.activateWindow',
                                side_effect=Exception())
            patch.start()

        try:
            dialog = dlg.createDialog(test_mode='ok',
                                      test_display_length=self.display_length)

            ret_val = dialog.showModal()
            self.assertTrue(ret_val)

            dialog.close()
            dialog = None

        finally:
            patch.stop()

    # -------------------------------------------------------------------------
    def test18_DialogBase_keyPressedEvent(self):

        dialog = dlg.createDialog(test_mode=True)
        dialog.disable_return_escape = True

        dialog.show()
        dialog.redraw()
        time.sleep(self.time_between_emits)

        try:
            event = QtWidgets.QKeyEvent(QtCore.QEvent.KeyPress, 13, QtCore.Qt.ShiftModifier)
        except AttributeError:
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 13, QtCore.Qt.ShiftModifier)
        QtCore.QCoreApplication.sendEvent(dialog, event)
        dialog.redraw()
        time.sleep(self.time_between_emits)

        keys = [QtCore.Qt.Key_Escape, QtCore.Qt.Key_Return, QtCore.Qt.Key_X]

        for key in keys:
            try:
                event = QtWidgets.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier)
            except AttributeError:
                event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier)
            QtCore.QCoreApplication.sendEvent(dialog, event)
            dialog.redraw()
            time.sleep(self.time_between_emits)


        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test19_createComplexDialog(self):
        dialog = dlg.createDialog(targetclass=ComplexDialog,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        ret_val = dialog.showModal()
        self.assertTrue(ret_val)

        dialog.test_display_length = None
        dialog.show()

        time.sleep(self.time_between_emits)
        cba = dialog.getWidget('cba')
        cba.setCheckState(QtCore.Qt.Unchecked)
        dialog.redraw()
        time.sleep(self.time_between_emits)
        cba.setCheckState(QtCore.Qt.Checked)
        dialog.redraw()
        time.sleep(self.time_between_emits)

        cbA = dialog.getWidget('cbA')
        self.assertTrue(isinstance(cbA, QtWidgets.QCheckBox))
        foo = dialog.getWidget('doesNotExist')
        self.assertEqual(foo, None)

        val = dialog.getWidgetValue('cbA')
        self.assertTrue(val)

        val = dialog.getWidgetValue('comboBox')
        self.assertEqual(val, (2, 'C'))

        val = dialog.getWidgetValue('text')
        self.assertEqual(val, 'Fritz Lakritz')

        val = dialog.getWidgetValue('multiline_text')
        self.assertEqual(val, 'Foo man Choo')

        mlt = dialog.getWidget('multiline_text')
        self.assertEqual(mlt.placeholderText(), 'Enter Name')
        mlt.setPlaceholderText('')
        self.assertEqual(mlt.placeholderText(), '')

        val = dialog.getWidgetValue('spinBox')
        self.assertEqual(val, 13)

        val = dialog.getWidgetValue('doesNotExistaosiais')
        self.assertEqual(val, None)

        lb = dialog.getWidget('listBox')
        lb.ignore_keypress = True
        self.assertTrue(lb.ignore_keypress)
        lb.ignore_keypress = False
        self.assertFalse(lb.ignore_keypress)

        try:
            event = QtWidgets.QKeyEvent(QtCore.QEvent.KeyPress, 13, QtCore.Qt.NoModifier)
        except AttributeError:
            event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 13, QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.sendEvent(lb, event)


        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test20_createDialog_ownModalButtons(self):
        class OwnModalButtonsDialog(dlg.Dialog):

            def initialize(self, **kwargs):
                self.title = 'OwnModalButtons Dialog'
                self.setWidthHeight(300, 600)

            def defineLayout(self):
                self.own_ok = self.addButton(widget_id='own_ok', label='My Own Ok')
                self.setModalOk(self.own_ok)
                self.own_cancel = self.addButton(widget_id='own_cancel', label='My Own Cancel')
                self.setModalCancel(self.own_cancel)

            def slot_own_ok_released(self):
                self.modal_return_value = True
                self.accept()

            def slot_own_cancel_released(self):
                self.reject()


        dialog = dlg.createDialog(targetclass=OwnModalButtonsDialog,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        ret_val = dialog.showModal()
        self.assertTrue(ret_val)
        dialog.close()
        dialog = None


        dialog = dlg.createDialog(targetclass=OwnModalButtonsDialog,
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        ret_val = dialog.showModal()
        self.assertFalse(ret_val)
        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test21_createDialog_scrollable_width_height(self):
        dialog = dlg.createDialog(scrollable=True,
                                   width=200,
                                   height=300,
                                   test_mode='ok',
                                   test_display_length=self.display_length)

        self.assertTrue(dialog.scrollable)
        dialog.scrollable = False
        self.assertFalse(dialog.scrollable)
        dialog.scrollable = True
        self.assertTrue(dialog.scrollable)

        status = dialog.showModal()
        self.assertTrue(status)
        self.assertTrue(dialog.scrollable)
        self.assertEqual(dialog.width, 200)
        self.assertEqual(dialog.height, 300)

    # -------------------------------------------------------------------------
    def test22_msgBox_ok_cancel(self):

        message = 'awesome and very informative multi\nline\nmessage...'
        result = dlg.msgBox(test_mode='ok',
                             title='Oh no...',
                             mode='warning',
                             message=message,
                             test_display_length=self.display_length)

        self.assertTrue(result)

        result = dlg.msgBox(test_mode='cancel',
                            test_display_length=self.display_length)


        self.assertFalse(result)

    # -------------------------------------------------------------------------
    def test23_msgBox_ok(self):

        result = dlg.msgBox(cancel_label=None,
                            test_mode='ok',
                            test_display_length=self.display_length)

        self.assertTrue(result)

        result = dlg.msgBox(cancel_label=None,
                            test_mode='cancel',
                            test_display_length=self.display_length)

        self.assertTrue(result)

    # -------------------------------------------------------------------------
    def test24_createDialog_openScrollable(self):
        dialog = dlg.createDialog(
                                   width=200,
                                   height=600,
                                   test_mode='ok',
                                   test_display_length=self.display_length)

        dialog.openScrollable(height=600, width=200)
        for i in range(40):
            dialog.addLabel(label=str(i))
        dialog.closeScrollable()
        status = dialog.showModal()
        self.assertTrue(status)

    # -------------------------------------------------------------------------
    def test25_createDialog_openGroup_width_height(self):
        dialog = dlg.createDialog(
                                   width=200,
                                   height=600,
                                   test_mode='ok',
                                   test_display_length=self.display_length)

        dialog.openGroup(widget_id='foo',
                         label='group',
                         prominent=False,
                         height=600,
                         width=200)

        dialog.addLabel(label='content')

        dialog.closeGroup()
        status = dialog.showModal()
        self.assertTrue(status)

    # -------------------------------------------------------------------------
    def test25_source_dir(self):

        dialog = dlg.createDialog(targetclass=ComplexDialog)

        self.assertEqual(dialog.source_dir,
                         os.path.dirname(__file__).replace('\\', '/'))

    # -------------------------------------------------------------------------
    def test26_source_filename(self):

        dialog = dlg.createDialog(targetclass=ComplexDialog)
        self.assertEqual(dialog.source_filename, 'complexDialog')


    # -------------------------------------------------------------------------
    def test27_addLabel_align(self):


        dialog = dlg.createDialog(title='Awesome Dialog',
                                  width=400,
                                  height=100,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        label_a = dialog.addLabel(label='left', align='left')
        label_b = dialog.addLabel(label='center', align='center')
        label_c = dialog.addLabel(label='right', align='right')
        label_d = dialog.addLabel(label='unsupported', align='nope')
        label_e = dialog.addLabel(label='top', valign='top')
        label_f = dialog.addLabel(label='bottom', valign='bottom')

        dialog.showModal()

        self.assertEqual(int(label_a.alignment()), 129)
        self.assertEqual(int(label_b.alignment()), 132)
        self.assertEqual(int(label_c.alignment()), 130)
        self.assertEqual(int(label_d.alignment()), 129)
        self.assertEqual(int(label_e.alignment()), 33)
        self.assertEqual(int(label_f.alignment()), 65)

        dialog = None

    # -------------------------------------------------------------------------
    def test28_addComboBox(self):

        dialog = dlg.createDialog(title='Awesome Dialog',
                                  width=400,
                                  height=100,
                                  test_mode='ok',
                                  test_display_length=self.display_length)

        combo = dialog.addComboBox(label='combo',
                                   label_width=50,
                                   content=['A', 'B'],
                                   value='B')
        dialog.showModal()

        self.assertEqual(combo.currentText(), 'B')

        dialog = None

    # -------------------------------------------------------------------------
    def test29_processEvents_works_as_expected(self):
        a = time.time()

        dialog = dlg.createDialog(title='Awesome Dialog',
                                   width=400,
                                   height=100,
                                   test_mode='cancel',
                                   test_display_length=1000)
        dialog.show()
        dlg.Dialog.processEvents()
        b = time.time()

        self.assertTrue((b-a) > 1.0)
        self.assertTrue((b-a) < 1.3)

    # -------------------------------------------------------------------------
    def test30_add_last_stretch_can_only_be_set_to_True_or_False(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        dialog.add_last_stretch = False
        self.assertEqual(dialog.add_last_stretch, False)

        dialog.add_last_stretch = True
        self.assertEqual(dialog.add_last_stretch, True)

        dialog.add_last_stretch = 'other value'
        self.assertEqual(dialog.add_last_stretch, False)

        dialog = None

    # -------------------------------------------------------------------------
    def test31_ui_built_signals_whether_the_ui_has_been_built(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        self.assertFalse(dialog.ui_built)

        dialog.show()
        self.assertTrue(dialog.ui_built)
        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test32_focussed_widget_returns_focussed_widget(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        btn = dialog.addButton(widget_id='btn_proof')

        self.assertEqual(dialog.focussed_widget, None)
        dialog.show()
        dialog.setFocus(btn)
        self.assertEqual(dialog.focussed_widget, btn)
        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test33_addWidget_adds_empty_widget(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='cancel',
                                  test_display_length=self.display_length)
        wdg = dialog.addWidget(widget_id='proof')

        self.assertEqual(dialog.getWidget('proof'), wdg)

        dialog.showModal()
        dialog = None

    # -------------------------------------------------------------------------
    def test34_addButton_works_as_expected(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='cancel',
                                  test_display_length=self.display_length)

        btn = dialog.addButton(widget_id='proof',
                               icon_path='ressources/search.png',
                               color='#ff00ff')

        self.assertEqual(dialog.getWidget('proof'), btn)

        dialog.showModal()
        dialog = None

    # -------------------------------------------------------------------------
    def test35_msgBox_from_dialog_ok_cancel(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='ok',
                                  test_display_length=self.display_length)
        # dialog.show()

        message = 'awesome and very informative multi\nline\nmessage...'
        result = dialog.msgBox(test_mode='ok',
                               title='Oh no...',
                               mode='warning',
                               message=message,
                               test_display_length=self.display_length)

        self.assertTrue(result)

        result = dialog.msgBox(test_mode='cancel',
                               test_display_length=self.display_length)

        self.assertFalse(result)

        # dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test36_insertWidget_lets_us_insert_functioning_Dialog_object(self):

        class MyRow(dlg.Dialog):
            def initialize(self, **kwargs):
                self.content = 'Label content'

            def defineLayout(self):
                self.addSpacer(10)
                self.label = self.addLabel(label=self.content)
                self.addButton(widget_id='btn_proof', label='click me')

            def slot_btn_proof_released(self):
                self.label.setText('I clicked da button!')


        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='ok',
                                  test_display_length=self.display_length)
        row = MyRow()
        wdg = dialog.insertWidget(widget_id='proof', widget=row)

        self.assertEqual(dialog.getWidget('proof'), row)
        self.assertTrue(isinstance(dialog.getWidget('proof'), MyRow))
        self.assertTrue(dialog.getWidget('proof').is_child_widget)

        result = dialog.showModal()
        self.assertTrue(result)
        dialog = None

    # -------------------------------------------------------------------------
    def test37_insertWidget_only_accepts_QWidgets_raises_AttributeError_if_otherwise(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='ok',
                                  test_display_length=self.display_length)
        with self.assertRaises(AttributeError):
            dialog.insertWidget('foo bar')

    # -------------------------------------------------------------------------
    def test38_Dialog_as_child_widget_showModal_raises_AttributeError(self):

        dialog = dlg.createDialog(title='dialog title',
                                  test_mode='ok',
                                  test_display_length=self.display_length)
        dialog.is_child_widget = True

        with self.assertRaises(AttributeError):
            dialog.showModal()

    # -------------------------------------------------------------------------
    def test39_nestedDialogs(self):

        class Child(Dialog):
            def defineLayout(self):
                self.openRow()
                self.btn = self.addButton(widget_id='btn', label='Booh')
                self.label = self.addLabel(label='Aaaah!')
                self.closeRow()

        class Main(Dialog):
            def defineLayout(self):
                a = Child()
                self.a = self.insertWidget(a, widget_id='a')
                self.addSpacer(20)
                b = Child()
                self.b = self.insertWidget(b, widget_id='b')

        dialog = createDialog(targetclass=Main,
                              test_mode='ok',
                              test_display_length=self.display_length)
        dialog.showModal()

        dialog.a.clear()
        dialog.a.rebuild()
        # dialog.redraw()
        # time.sleep(self.display_length)

        # dialog.rebuild()

        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test40_multiline_TextBox_placeholder(self):

        dialog = createDialog(width=400, height=300, test_mode=True)
        mltb = dialog.addTextBox(multiline=True, placeholder='placeholder')
        tb = dialog.addTextBox(multiline=False)
        dialog.setFocus(tb)
        dialog.show()

        self.assertEqual(mltb.placeholderText(), 'placeholder')
        time.sleep(1)
        dialog.redraw()
        mltb.setPlaceholderText('New Text')
        self.assertEqual(mltb.placeholderText(), 'New Text')
        time.sleep(1)
        dialog.redraw()

        dialog.close()
        dialog = None


    # -------------------------------------------------------------------------
    def test41_clickable_Label(self):

        class TestDialog(Dialog):
            def initialize(self):
                self.test_mode = True
            def defineLayout(self):
                self.text = self.addTextBox(multiline=False)
                self.addSpacer(50)
                self.label = self.addLabel(widget_id='label', label='ClickMe')
                self.addSpacer(50)
            def slot_label_labelClicked(self):
                self.text.setText('clicked')


        dialog = createDialog(targetclass=TestDialog)

        dialog.show()
        dialog.redraw()
        time.sleep(self.time_between_emits)

        self.assertEqual(dialog.text.text(), '')

        QtTest.QTest.mouseClick(dialog.label,
                                QtCore.Qt.LeftButton,
                                pos=QtCore.QPoint(5,5),
                                delay=self.display_length)
        dialog.redraw()
        time.sleep(self.time_between_emits)
        dialog.close()

        self.assertEqual(dialog.text.text(), 'clicked')
        dialog = None

    # -------------------------------------------------------------------------
    def test42_dialog_delete_late_can_be_get_and_set(self):

        dialog = createDialog()
        self.assertTrue(dialog.delete_later)
        dialog.delete_later = False
        self.assertFalse(dialog.delete_later)
        dialog.delete_later = True
        self.assertTrue(dialog.delete_later)
        dialog.delete_later = 'Nonsense'
        self.assertFalse(dialog.delete_later)

    # -------------------------------------------------------------------------
    def test43_multiline_TextBox_leave_on_tab(self):

        dialog = createDialog(width=400, height=300, test_mode=True)
        mltb = dialog.addTextBox(multiline=True, leave_on_tab=True)
        dialog.setFocus(mltb)
        dialog.show()

        QTest.keyClicks(mltb, 'abc\t', delay=self.delay)
        self.assertFalse(mltb.hasFocus())

        dialog.close()
        dialog = None

        dialog = createDialog(width=400, height=300, test_mode=True)
        mltb = dialog.addTextBox(multiline=True, leave_on_tab=False)
        dialog.setFocus(mltb)
        dialog.show()

        QTest.keyClicks(mltb, 'abc\t', delay=self.delay)
        self.assertTrue(mltb.hasFocus())

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test44_multiline_TextBox_leave_on_ctrl_enter(self):

        dialog = createDialog(width=400, height=300, test_mode=True)
        mltb = dialog.addTextBox(multiline=True, leave_on_ctrl_enter=True)
        dialog.setFocus(mltb)
        dialog.show()

        QTest.keyPress(mltb, QtCore.Qt.Key_Return, modifier=QtCore.Qt.ControlModifier, delay=self.delay)
        self.assertFalse(mltb.hasFocus())

        dialog.close()
        dialog = None

        dialog = createDialog(width=400, height=300, test_mode=True)
        mltb = dialog.addTextBox(multiline=True, leave_on_ctrl_enter=False)
        dialog.setFocus(mltb)
        dialog.show()

        QTest.keyPress(mltb, QtCore.Qt.Key_Return, modifier=QtCore.Qt.ControlModifier, delay=self.delay)
        self.assertTrue(mltb.hasFocus())

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test92_contextNuke(self):

        def import_module(foo):
            return os

        with mock.patch('importlib.import_module', return_value=os):

            try:
                QtWidgets.QApplication(sys.argv)
            except RuntimeError:
                pass

            Dialog._context = None
            try:
                with mock.patch('sys.executable', 'c:/foo/nuke11.1.exe'):
                    dialog = dlg.createDialog(title='dialog title',
                                              width=400,
                                              height=100,
                                              fixed_size=False,
                                              test_mode='ok',
                                              test_display_length=self.display_length)


                    ret_val = dialog.showModal()
                    self.assertTrue(ret_val)

                    self.assertEqual(dialog.context, 'nuke')

                    dialog.close()
                    dialog = None

            finally:
                Dialog._context = None

# -------------------------------------------------------------------------
    def test93_contextHoudini(self):

        hou = mock.Mock(
                  qt=mock.Mock(
                      mainWindow=mock.Mock(
                          return_value=QtWidgets.QApplication.activeWindow()
                      )
                  )
              )

        sys.modules['hou'] = hou

        if dlg.Dialog.app is None:
            dlg.Dialog.app = QtWidgets.QApplication(sys.argv)


        Dialog._context = None
        try:
            with mock.patch('sys.executable', 'c:/foo/houdini.exe'):

                dialog = dlg.createDialog(title='dialog title',
                                          width=400,
                                          height=100,
                                          fixed_size=False,
                                          test_mode='ok',
                                          test_display_length=self.display_length)


                ret_val = dialog.showModal()
                self.assertTrue(ret_val)

                self.assertEqual(dialog.context, 'houdini')

                dialog.close()
                dialog = None

        finally:
            sys.modules.pop('hou')
            Dialog._context = None

    # -------------------------------------------------------------------------
    def test94_DialogBase_redraw_maya(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')
        filename = os.path.basename(__file__).replace('.pyc', '.py')

        import mocked_cmds

        def import_module(foo):
            return mocked_cmds

        with mock.patch('importlib.import_module', return_value=os):

            try:
                QtWidgets.QApplication(sys.argv)
            except RuntimeError:
                pass

            mocked_maya_window = QtWidgets.QDialog()
            mocked_maya_window.setObjectName('MayaWindow')

            Dialog._context = None

            try:
                with mock.patch('sys.executable', 'c:/foo/maya.exe'):

                    dialog = dlg.createDialog(title='dialog title',
                                              width=400,
                                              height=100,
                                              fixed_size=False,
                                              test_mode=True,
                                              test_display_length=None)

                    dialog.addSpacer(30)
                    widget = dialog.addFileBrowser(
                                        mode='open',
                                        width=300,
                                        label='awesome open Browser',
                                        initialdir=basepath,
                                        selected_file=filename,
                                        filters=['Python (*.py)'])

                    dialog.addSpacer(30)


                    ret_val = dialog.show()
                    time.sleep(self.time_between_emits)
                    button = widget.button
                    widget.test_mode = 'accept'
                    widget.test_delay = self.time_between_emits
                    button.click()
                    dialog.redraw()
                    time.sleep(self.time_between_emits)
                    self.assertEqual(widget.targetfile, filename)
                    self.assertEqual(widget.targetfolder.lower(),
                                     basepath.lower())

                    self.assertEqual(dialog.context, 'maya')

                    dialog.close()
                    dialog = None

                    mocked_maya_window.close()
                    mocked_maya_window = None

            finally:
                Dialog._context = None

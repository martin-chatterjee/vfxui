# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# -----------------------------------------------------------------------------

import os
import sys
import time
import importlib
import imp

import sehsucht

import vfxui.dialog as dlg

from vfxui.pyside import QtCore, QtGui, QtWidgets, QtTest
from vfxui.dialog import Dialog
from complexDialog import ComplexDialog

from vfxtest import TestCase, mock

# =============================================================================
class UI_Dialog_Test(TestCase):
    """
    """

    # -------------------------------------------------------------------------
    @classmethod
    def setUpOnce(cls):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        cls.display_length = 100
        cls.time_between_emits = .1

        # cls.display_length = 0
        # cls.time_between_emits = 0


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

        dialog = None

    # -------------------------------------------------------------------------
    def test03_imagelabel(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=False,
                                  test_display_length=self.display_length)
        # dialog.setWorkingDir(__file__)
        dialog.addSpacer(30)
        img = dialog.addImage(image_path='%s/ActionsSubHead.png' % basepath,
                        image_path_hi='%s/ActionsSubHead_HI.png' % basepath,
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

        img.swapImage(image_path='%s/ActionsSubHead_HI.png' % basepath)

        time.sleep(self.time_between_emits)
        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test04_filebrowser_open(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=False,
                                  test_display_length=self.display_length)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='open',
                            width=300,
                            label='awesome open Browser',
                            initialdir=basepath,
                            selected_file='run_all_tests.py',
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)



        ret_val = dialog.show()
        time.sleep(self.time_between_emits)
        button = browser.button
        browser.test_mode = 'accept'
        browser.test_delay = self.time_between_emits
        button.click()
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfile, u'run_all_tests.py')
        self.assertEqual(browser.targetfolder.lower(),
                         basepath.lower())
        expected_filepath = u'%s/run_all_tests.py' % (browser.targetfolder)
        self.assertEqual(browser.targetfilepath, expected_filepath)

        browser.test_mode = 'reject'

        button.click()
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfile, u'')
        self.assertEqual(browser.targetfolder, u'')

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test05_filebrowser_save(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=False,
                                  test_display_length=self.display_length)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            widget_id='saveBrowser',
                            mode='save',
                            label='awesome save Browser',
                            initialdir=basepath,
                            selected_file='savename.py',
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)

        ret_val = dialog.show()
        time.sleep(self.time_between_emits)
        browser.test_delay = self.time_between_emits
        browser.showDialog(test_mode='accept')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfile, u'savename.py')
        self.assertEqual(browser.targetfolder.lower(),
                         basepath.lower())

        browser.showDialog(test_mode='reject')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfile, u'')
        self.assertEqual(browser.targetfolder, u'')

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test06_filebrowser_folder(self):


        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            widget_id='folderBrowser',
                            mode='folder',
                            label='awesome folder Browser')

        dialog.addSpacer(30)

        ret_val = dialog.show()
        time.sleep(self.time_between_emits)
        browser.test_delay = self.time_between_emits
        browser.showDialog(test_mode='accept')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfolder, u'C:/TEMP')
        self.assertEqual(browser.targetfile, u'')

        browser.showDialog(test_mode='reject')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfolder, u'')
        self.assertEqual(browser.targetfile, u'')

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

        self.assertEqual(dlg.Dialog._resolveContext(), dialog.context)

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
        dialog.disable_return_escape = True
        self.assertTrue(dialog.disable_return_escape)

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

        self.assertEqual(dialog.test_display_length, 1000)

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

        dialog.test_mode = False
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
        dialog.test_mode = False
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

        dialog = dlg.createDialog()
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

        dialog.test_mode = False
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

        dialog.showModal()

        self.assertEqual(int(label_a.alignment()), 1)
        self.assertEqual(int(label_b.alignment()), 132)
        self.assertEqual(int(label_c.alignment()), 2)
        self.assertEqual(int(label_d.alignment()), 1)

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
    def test92_contextNuke(self):

        def import_module(foo):
            return os

        with mock.patch('importlib.import_module', return_value=os):

            try:
                QtWidgets.QApplication(sys.argv)
            except RuntimeError:
                pass

            Dialog._context = 'nuke'
            try:
                dialog = dlg.createDialog(title='dialog title',
                                          width=400,
                                          height=100,
                                          fixed_size=False,
                                          test_mode='ok',
                                          test_display_length=self.display_length)


                ret_val = dialog.showModal()
                self.assertTrue(ret_val)

                self.assertEqual(dialog.context, 'nuke')
                # self.assertEqual(len(dialog.apis), 2)
                # self.assertTrue('nuke' in dialog.apis)
                # self.assertEqual(dialog.apis['nuke'], os)
                # self.assertTrue('nukescripts' in dialog.apis)
                # self.assertEqual(dialog.apis['nukescripts'], os)

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


        Dialog._context = 'houdini'
        try:
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

            Dialog._context = 'maya'

            try:
                dialog = dlg.createDialog(title='dialog title',
                                          width=400,
                                          height=100,
                                          fixed_size=False,
                                          test_mode=False,
                                          test_display_length=self.display_length)

                dialog.addSpacer(30)
                widget = dialog.addFileBrowser(
                                    mode='open',
                                    width=300,
                                    label='awesome open Browser',
                                    initialdir=basepath,
                                    selected_file='run_all_tests.py',
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
                self.assertEqual(widget.targetfile, u'run_all_tests.py')
                self.assertEqual(widget.targetfolder.lower(),
                                 basepath.lower())

                self.assertEqual(dialog.context, 'maya')
                # self.assertEqual(len(dialog.apis), 3)
                # self.assertTrue('maya.cmds' in dialog.apis)
                # self.assertTrue('pymel.core' in dialog.apis)
                # self.assertTrue('maya.mel' in dialog.apis)
                # self.assertEqual(dialog.apis['maya.cmds'], mocked_cmds)
                # self.assertEqual(dialog.apis['pymel.core'], mocked_cmds)
                # self.assertEqual(dialog.apis['maya.mel'], mocked_cmds)

                dialog.close()
                dialog = None

                mocked_maya_window.close()
                mocked_maya_window = None

            finally:
                Dialog._context = None

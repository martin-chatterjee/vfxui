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
class UI_FileBrowser_Test(TestCase):
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
    def test01_filebrowser_open(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')
        filename = os.path.basename(__file__).replace('.pyc', '.py')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='open',
                            width=300,
                            label='awesome open Browser',
                            initialdir=basepath,
                            selected_file=filename,
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
        self.assertEqual(browser.targetfile, filename)
        self.assertEqual(browser.targetfolder.lower(),
                         basepath.lower())
        expected_filepath = u'%s/%s' % (browser.targetfolder, filename)
        self.assertEqual(browser.targetfilepath, expected_filepath)
        self.assertEqual(browser.targetfilepaths, [expected_filepath,])

        browser.test_mode = 'reject'

        button.click()
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfile, u'')
        self.assertEqual(browser.targetfiles, ['',])
        self.assertEqual(browser.targetfolder, u'')

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test02_filebrowser_save(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=400,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

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
    def test03_filebrowser_folder(self):


        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=500,
                                  height=100,
                                  test_mode=True,
                                  fixed_size=False)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            widget_id='folderBrowser',
                            width=400,
                            mode='folder',
                            label='awesome folder Browser')

        dialog.addSpacer(30)

        ret_val = dialog.show()
        time.sleep(self.time_between_emits)
        browser.test_delay = self.time_between_emits
        browser.showDialog(test_mode='accept')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfolder, u'{}'.format(basepath))
        self.assertEqual(browser.targetfile, u'')

        browser.showDialog(test_mode='reject')
        dialog.redraw()
        time.sleep(self.time_between_emits)
        self.assertEqual(browser.targetfolder, u'')
        self.assertEqual(browser.targetfile, u'')

        dialog.close()
        dialog = None

    # -------------------------------------------------------------------------
    def test04_filebrowser_font(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=800,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='open',
                            label='awesome open Browser',
                            initialdir=basepath,
                            selected_file='run_all_tests.py',
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)

        browser.setFont('Helvetica')
        self.assertEqual(browser.font().family(), 'Helvetica')

    # -------------------------------------------------------------------------
    def test05_direct_editing(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=800,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='open',
                            direct_edit=True,
                            label='awesome open Browser',
                            initialdir=basepath,
                            selected_file='run_all_tests.py',
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)

        dialog.show()
        dialog.redraw()

        time.sleep(self.time_between_emits)

        invalid_subfolder = '{}/does-not-exist/'.format(basepath)
        QTest.keyClicks(browser.text, invalid_subfolder, delay=self.delay)
        QTest.keyPress(browser.text, QtCore.Qt.Key_Tab, delay=self.display_length)
        dialog.redraw()
        time.sleep(self.time_between_emits)

        dialog.close()
        dialog = None

        self.assertEqual(browser.targetfolder, basepath)
        self.assertEqual(browser.targetfile, '')

    # -------------------------------------------------------------------------
    def test06_invalid_initialdir(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')

        dialog = dlg.createDialog(title='dialog title',
                                  width=800,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='folder',
                            direct_edit=True,
                            label='awesome open Browser',
                            initialdir='{}/does/not/exist'.format(basepath),
                            selected_file='run_all_tests.py',
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)

        dialog.show()
        dialog.redraw()

        dialog.close()
        dialog = None
        self.assertEqual(browser.targetfolder, basepath)
        self.assertEqual(browser.targetfile, '')


    # -------------------------------------------------------------------------
    def test07_multi_select(self):

        basepath = os.path.dirname(__file__).replace('\\', '/')
        files = []
        for item in sorted(os.listdir(basepath)):
            if item.endswith('.py'):
                files.append(item)
                if len(files) >= 4:
                    break
        escaped = ['"{}"'.format(item) for item in files]
        files_string = ' '.join(escaped)

        shown_files = list(files)[:3]
        if len(files) > 3:
            shown_files.append('...')
        expected_text = '{}/[ {} ]'.format(basepath, ', '.join(shown_files))

        selected_files = '"complexDialog.py" "mocked_cmds.py"'
        dialog = dlg.createDialog(title='dialog title',
                                  width=800,
                                  height=100,
                                  fixed_size=False,
                                  test_mode=True,
                                  test_display_length=None)

        dialog.addSpacer(30)
        browser = dialog.addFileBrowser(
                            mode='open',
                            multiselect=True,
                            selected_file = files_string,
                            label='awesome open Browser',
                            initialdir=basepath,
                            filters=['Python (*.py)'])

        dialog.addSpacer(30)

        dialog.show()
        dialog.redraw()
        time.sleep(self.time_between_emits)

        button = browser.button
        browser.test_mode = 'accept'
        browser.test_delay = self.time_between_emits
        button.click()


        dialog.redraw()
        time.sleep(self.time_between_emits)

        dialog.close()
        dialog = None

        self.assertEqual(browser.targetfolder, basepath)
        self.assertEqual(browser.targetfile, files[0])
        self.assertEqual(browser.targetfiles, files)
        self.assertEqual(browser.text.text(), expected_text)

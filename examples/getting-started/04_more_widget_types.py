# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

import os
import vfxui
from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_04_more_widget_types():
    """Introduces more widget types.
    """

    # Let's have a look at some supported widget types.
    # Please don't hesitate to glance over the implementation of
    # vfxui.dialog to discover even more goodies! ;)

    from vfxui.dialog import Dialog

    class MoreWidgetsDialog(Dialog):

        # implement initialize() to deal with all the prep work
        def initialize(self, **kwargs):
            self.title = 'More Widgets...'
            self.width = 400
            # prepare other things here
            self.initialdir = os.path.dirname(vfxui.__file__)


        # now implement defineLayout() to build up your layout
        def defineLayout(self):

            # a head line (really just a label...)
            self.headline = self.addHeadline(label='Widgets Galore...')
            self.addSpacer(10)

            # one-line textbox
            self.textbox = self.addTextBox(value='one line of disabled text',
                                           enabled=False)
            self.addSpacer(10)

            # multi-line textbox
            self.multiline_textbox = self.addTextBox(value='Lorem\nIpsum\n...',
                                                     multiline=True)
            self.addSpacer(10)

            # a label...
            self.addLabel(label='Just a Label', font_size=13, font_weight='italic')
            self.addSpacer(10)

            # a spinbox for Integers...
            self.int_spinbox = self.addSpinBox(label='Integer SpinBox',
                                               value=13,
                                               label_width=100,
                                               width=100)
            self.addSpacer(10)
            # and a spinbox for Floats...
            self.float_spinbox = self.addSpinBox(label='Float SpinBox',
                                                 value=13.0,
                                                 label_width=100,
                                                 width=100)
            self.addSpacer(10)

            # three checkboxes without label
            self.openGroup(label='some checkboxes...')
            self.openRow()
            self.check_a = self.addCheckBox(value=True)
            self.addSpacer(5)
            self.check_b = self.addCheckBox(value=False)
            self.addSpacer(5)
            self.check_c = self.addCheckBox(value=True)
            self.addStretch()
            self.closeRow()
            self.closeGroup()

            self.addSpacer(10)

            # a line-centered image (you can use paths relative to the current file!)
            self.openRow()
            self.addStretch()
            self.img = self.addImage(image_path='images/logo.png')
            self.addStretch()
            self.closeRow()

            self.addSpacer(10)

            # a combo box
            self.combo = self.addComboBox(content = ['Lorem', 'Ipsum', 'Foo', 'Bar'],
                                          value = 'Foo',
                                          height=30,
                                          font_size=20)
            self.addSpacer(10)

            # a Button
            self.button = self.addButton(label='Click Me!!!',
                                         width=200,
                                         height=100,
                                         color='#883333')

            self.addSpacer(10)

            # a file browser (supported modes are 'open', 'save', 'folder')
            self.browser = self.addFileBrowser(mode='open',
                                               initialdir = self.initialdir,
                                               button_label='Open File...',
                                               dialog_caption='Please select a Script File!',
                                               filters=['Python Files (*.py)'],
                                               label='awesome file browser')


            self.addSpacer(10)
            # and finally a list box
            self.listbox = self.addListBox(multiselect=True,
                                           content=['Fizz', 'Buzz', 'Baz'],
                                           height=90)



    # let's create and display our dialog
    dialog = createDialog(targetclass=MoreWidgetsDialog)
    status = dialog.showModal()

    print('return status:         %s' % status)
    print('')

    print('Int Spinbox class:     %s' % dialog.int_spinbox.__class__.__name__)
    print('Int Spinbox value:     %s' % dialog.int_spinbox.value())
    print('')
    print('Checkboxes:            %s - %s - %s' % (dialog.check_a.isChecked(),
                                                   dialog.check_b.isChecked(),
                                                   dialog.check_c.isChecked()))
    print('')
    print('FileBrowser file:      %s' % dialog.browser.targetfile)
    print('FileBrowser folder:    %s' % dialog.browser.targetfolder)

    print('')
    print('')
    raw_input('Press Enter to finish...')



example_04_more_widget_types()

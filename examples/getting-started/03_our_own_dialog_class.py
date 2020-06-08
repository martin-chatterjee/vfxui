# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_03_our_own_dialog_class():
    """Implement your own Dialog class for more serious UI's.
    """

    # For proper Dialogs it's good practice to implement your own class for it.
    # Let's reimplement example_02 UI as a class.

    from vfxui.dialog import Dialog

    # You need to inherit from class Dialog
    class ExampleDialog(Dialog):

        # implement initialize() to deal with all the prep work
        def initialize(self, **kwargs):
            self.title = 'My awesome dialog'
            self.width = 400
            self.height = 300
            # you can also control, if the dialog should be resizable
            self.fixed_size = False

        # now implement defineLayout() to build up your layout
        def defineLayout(self):
            self.addSpacer(10)
            self.addLabel(label='My Awesome Label', font_size=20)
            self.addSpacer(10)

            self.openGroup(label='some controls')

            self.openRow()
            self.addStretch()
            self.textbox = self.addTextBox(value='Awesome Content', width=200)
            self.addStretch()
            self.closeRow()

            self.addSpacer(10)

            self.openRow()
            self.check_a = self.addCheckBox(label='A')
            self.addSpacer(20)
            self.check_b = self.addCheckBox(label='B', value=False)
            self.addStretch()
            self.closeRow()

            self.closeGroup()


    # all right, now we can get our Dialog object.
    # !!! It is important to NOT just instantiate your class !!!
    # Rather again use createDialog(), and pass in your class

    dialog = createDialog(targetclass=ExampleDialog)
    print('We now have an object of type %s!' % dialog.__class__.__name__)

    # The rest should behave just like example_02, except now you can interact
    # with the widgets through your dialog object by accessing 'dialog.textbox',
    # for example.

    status = dialog.showModal()

    print('return status: %s' % status)
    print('')

    print('textbox class:  %s' % dialog.textbox.__class__.__name__)
    print('textbox value:  %s' % dialog.textbox.text())
    print('')
    print('check_a class:  %s' % dialog.check_a.__class__.__name__)
    print('check_a value:  %s' % dialog.check_a.isChecked())
    print('')
    print('check_b class:  %s' % dialog.check_b.__class__.__name__)
    print('check_b value:  %s' % dialog.check_b.isChecked())

    print('')
    print('')
    raw_input('Press Enter to finish...')



example_03_our_own_dialog_class()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_07_textbox_expression():
    """Example for Textbox expression.

    """

    # create the dialog object
    dialog = createDialog(title='Achtung Baby!', width=200, height=50)

    # add a spacer of 10 pixels
    dialog.addSpacer(10)
    # add a Label
    dialog.addLabel(label='this Textbox is limited....')
    dialog.addLabel(label='no space and weird characters allowed ;-)')
    # and another spacer
    dialog.addSpacer(10)
    # and TextBox with reg expression
    dialog.addTextBox(  label = 'Name',
                        label_width = 50,
                        width = 150,
                        value = '',
                        expression='^[_a-zA-Z0-9]*$')
    dialog.addSpacer(10)

    # now let's show our dialog modally.
    # This will automatically add 'OK' and 'Cancel' buttons to the dialog.
    status = dialog.showModal()

    # the return value is True for an 'OK' button press and False
    # for everything else
    print('return status: %s' % status)

    print('')
    print('')
    raw_input('Press Enter to finish...')



example_07_textbox_expression()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_02_control_layout():
    """Build up your layout bit by bit.

    """
    # I personally find building UI Layouts with vanilla PySide a bit of a burden.
    # Oftentimes you need to sort of think a bit 'backwards':
    #   - create a layout for a row
    #   - fill it with content
    #   - create a widget and attach this prepared layout to the widget
    #   - only now can I add that widget (and therefore the row) to the main layout.

    # 'vfxui' attempts to hide all this complexity from you and
    # lets you build up your layout bit by bit in a linear fashion.


    # create the dialog object
    dialog = createDialog(title='my awesome dialog', width=400, height=300)
    # every empty dialog starts with a column layout.
    # add a spacer of 10 pixels
    dialog.addSpacer(10)
    # add a Label
    dialog.addLabel(label='My Awesome Label', font_size=20)
    # and another spacer
    dialog.addSpacer(10)
    # open a Group
    dialog.openGroup(label='some controls')
    #now open a row
    dialog.openRow()
    # center a textBox in this row by sandwiching it between two stretches
    dialog.addStretch()
    textbox = dialog.addTextBox(value='Awesome Content', width=200)
    dialog.addStretch()
    dialog.closeRow()
    # one more spacer between rows
    dialog.addSpacer(10)
    # add another row and show two checkboxes
    dialog.openRow()
    check_a = dialog.addCheckBox(label='A')
    dialog.addSpacer(20)
    check_b = dialog.addCheckBox(label='B', value=False)
    # finish this row with a stretch
    dialog.addStretch()

    # It's good practice to close all your rows, columns and groups explicitely.
    # However if you don't do it at the end of your layout creation,
    # sehsucht.ui would just close them for you automatically.
    dialog.closeRow()
    dialog.closeGroup()

    # Show the dialog modally.
    # Try to resize the dialog to see what effect the Stretches and Spacers have!
    status = dialog.showModal()
    print('return status: %s' % status)
    print('')

    # the return values of the add*() method are the actual PySide widgets.
    # you can interact with them an read their values after the dialog has been
    # closed.
    #
    # For more information on the PySide Widget methods simply google :
    #       'PySide <ClassName>'
    #  e.g. 'PySide QCheckBox'

    print('textbox class:  %s' % textbox.__class__.__name__)
    print('textbox value:  %s' % textbox.text())
    print('')
    print('check_a class:  %s' % check_a.__class__.__name__)
    print('check_a value:  %s' % check_a.isChecked())
    print('')
    print('check_b class:  %s' % check_b.__class__.__name__)
    print('check_b value:  %s' % check_b.isChecked())

    print('')
    print('')
    raw_input('Press Enter to finish...')



example_02_control_layout()

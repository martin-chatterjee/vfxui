# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_01_hello_world():
    """Create your first on-the-fly dialog.

    """

    # reateDialog() allows you to create a Dialog that will automatically
    # be a child of the current parent application (Maya, Python, Houdini, ...)
    # These dialogs will work within PySide2 environments (such as modern Mayas)
    # as well as within PySide environments.

    # More complex dialogs will be implemented in their own classes, but for
    # super simple Dialogs you can just create them on the fly -- just like
    # in this 'hello World' example.

    # create the dialog object
    dialog = createDialog(title='my awesome dialog', width=200, height=50)

    # add a spacer of 10 pixels
    dialog.addSpacer(10)
    # add a Label
    dialog.addLabel(label='Hello World!')
    # and another spacer
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



example_01_hello_world()

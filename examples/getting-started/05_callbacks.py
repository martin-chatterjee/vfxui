# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

import os
from vfxui.dialog import createDialog

# -----------------------------------------------------------------------------
def example_05_callbacks():
    """Implement your own callbacks.
    """

    # All right, it's time for some callbacks!
    from vfxui.dialog import Dialog

    class CallbacksDialog(Dialog):

        def initialize(self, **kwargs):
            self.title = 'Time for some callbacks...'
            self.width = 800
            self.width = 400

        def defineLayout(self):
            # a head line (really just a label...)
            self.headline = self.addHeadline(label='Time for Callbacks...')
            self.addSpacer(30)

            # in order to build callbacks for a widget we need to create it
            # with a known unique lower-case widget_id -- in this example 'my_button'.
            self.openRow()
            self.addStretch()
            self.button = self.addButton(widget_id='my_button',
                                         label='Click me!!!',
                                         width=300, height=170)
            self.addStretch()
            self.closeRow()
            self.addSpacer(30)

            # ---------------------------------------------
            # Pyside has the concept of 'Signals' and 'Slots':
            #   - a widget emits 'Signals'
            #   - implemented 'Slots' get triggered by these emitted signals
            # ---------------------------------------------

            # this is the fastest way to get a list of supported signals
            # for a widget:
            self.getWidgetDetails(self.button)
            # this will print the Class name, the widget_id and a list of
            # supported signals.


        # -------------------------------------------------
        # All right, now let's implement a slot!
        # You need to know the 'widget_id' and the 'signal' name.
        #
        # Then just implement 'slot_<widget_id>_<signal>()'
        #
        # In our case we have the widget_id 'my_button' and we choose
        # the signal 'released'.
        # -------------------------------------------------
        def slot_my_button_released(self):
            print('You did it!!!')


        # -------------------------------------------------
        # You can also implement context-specific slots:
        #
        # Just implement 'slot<Context>_<widget_id>_<signal>()'
        # -------------------------------------------------
        def slotPython_my_button_released(self):
            print('I got clicked in the Python context...')

        def slotMaya_my_button_released(self):
            print('I got clicked in the Maya context...')


        # -------------------------------------------------
        # Finally there's the possibility to implement a global slot
        # for a signal:
        #
        # Just implement 'slotGlobal_<signal>()'
        # -------------------------------------------------
        def slotGlobal_released(self):
            print("I get called for every 'release' signal")

        # -------------------------------------------------
        # The evaluation order is:
        #   - context-specific
        #   - regular
        #   - global




    # let's create and display our dialog
    dialog = createDialog(targetclass=CallbacksDialog)
    status = dialog.showModal()

    print('')
    print('')
    raw_input('Press Enter to finish...')



example_05_callbacks()

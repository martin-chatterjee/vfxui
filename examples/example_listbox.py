# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

from vfxui.dialog import Dialog, createDialog


# -----------------------------------------------------------------------------
class ListBoxExample(Dialog):

    # -------------------------------------------------------------------------
    def initialize(self):
        self.width = 400
        self.height = 400
        self.title = 'ListBox Demo'

    # -------------------------------------------------------------------------
    def defineLayout(self):

        self.listbox = self.addListBox(
                            widget_id='listbox',
                            filtering=True,
                            multiselect=True,
                            selection_controls=True,
                            selection_control_position='left',
                            content=['foo', 'bar', 'fizz', 'buzz'],
                        )

        self.getWidgetDetails(self.listbox)

    # -------------------------------------------------------------------------
    def slot_listbox_itemSelectionChanged(self):
        print('itemSelectionChanged!')

    # -------------------------------------------------------------------------
    def slot_listbox_currentItemChanged(self, current, previous):
        prev = None
        if previous is not None:
            prev = previous.text()
        print('currentItemChanged from {} to {}'.format(prev,
                                                        current.text()))





if __name__ == '__main__':
    dlg = createDialog(targetclass=ListBoxExample)
    dlg.showModal()

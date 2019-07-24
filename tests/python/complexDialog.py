# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2018, Martin Chatterjee. All rights reserved.
# ------------------------------------------------------------------------------

import os

from vfxui.dialog import Dialog

# =============================================================================
class ComplexDialog(Dialog):

    # -------------------------------------------------------------------------
    def initialize(self, **kwargs):
        """
        """
        self.title = 'ComplexDialog'
        self.width = 500
        self.height = 800
        self.setAsSplashScreen()


    # -------------------------------------------------------------------------
    def defineLayout(self):

        tabsgroup = self.addTabsGroup()

        tab_a = self.openTab(tabsgroup, 'tab_a', 'first Tab')
        self.addSpacer(10)
        self.addDivider()
        self.addSpacer(10)
        self.addListBox(content=['foo',
                                 'bar',
                                 'fizz',
                                 'buzz'],
                                 min_width=300,
                                 min_height=300,
                                 multiselect=True,
                                 font='Arial',
                                 font_weight='bold',
                                 height=300,
                                 width=300)
        self.addStretch()
        self.closeTab()




        tab_b = self.openTab(tabsgroup, label='second Tab')
        self.addSpacer(10)
        self.addDivider()
        self.addLabel(label='awesome Label')
        self.addDivider()
        self.addSpacer(10)
        self.addComboBox(label='choose:',
                         width=200,
                         height=50,
                         content=['A', 'B', 'C'],
                         value='C')
        self.addSpacer(20)
        self.openRow()
        self.addSpinBox(label='spinBox:',
                       width=50,
                       label_width=100,
                       min=0,
                       max=100,
                       value=13)
        self.addSpinBox(widget_id='float_spin',
                        label='float spinBox:',
                        width=50,
                        label_width=100,
                        min=0.0,
                        max=100.0,
                        value=13.0)
        self.addSpacer(20)
        self.addLabel(label='some infos....')
        self.addStretch()
        self.closeRow()
        self.addSpacer(30)
        self.openGroup()
        self.openRow()
        self.addCheckBox(widget_id='cbA', label='this one', value=True)
        self.addSpacer(20)
        self.addCheckBox(value=False)
        self.addSpacer(100)
        self.addButton(label='confirm', width=300, height=100)
        self.addStretch()
        self.closeRow()
        self.closeGroup()
        textbox = self.addTextBox(label='enter Name:',
                                value='Fritz Lakritz',
                                min_height=50,
                                width=300,
                                placeholder='placeholder',
                                expression='^[_a-zA-Z0-9]*$')
        multilinetextbox = self.addTextBox(
                                widget_id='multiline_text',
                                multiline=True,
                                label='enter Name:',
                                placeholder='Enter Name',
                                value='Foo man Choo',
                                min_height=50,
                                width=300)
        self.addStretch()
        self.closeTab()


        self.addStretch()

        self.showTab(tabsgroup, tab_b)
        self.setFocus(textbox)

        self.add_last_stretch = True


    # -------------------------------------------------------------------------
    def slot_cba_stateChanged(self):
        print('changed State!!')
    # -------------------------------------------------------------------------
    def slotPython_cba_stateChanged(self):
        print('changed State!! (python only)')

    # -------------------------------------------------------------------------
    def slotGlobal_stateChanged(self):
        print('changed State!! (Global)')


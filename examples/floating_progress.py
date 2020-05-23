from vfxui.dialog import Dialog, createDialog
from vfxui.pyside import QtCore, QtWidgets


def doIt():

    class FloatingProgress(Dialog):

        def initialize(self, **kwargs):
            self.title = 'Floating Progress'
        def defineLayout(self):
            self.addButton(widget_id='btn_show', label='show')
            self.addButton(widget_id='btn_change', label='change')
            self.addButton(widget_id='btn_hide', label='hide')

            self.msg = self.createFloatingMessage()

        def slot_btn_show_released(self):
            self.msg.show('Hey There')

        def slot_btn_change_released(self):
            self.msg.show('This is my awesome message')

        def slot_btn_hide_released(self):
            self.msg.hide()


    dlg = createDialog(targetclass=FloatingProgress)
    dlg.showModal()
    print('Done...')


if __name__ == '__main__':
    doIt()

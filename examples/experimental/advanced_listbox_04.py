
from vfxui.dialog import Dialog, createDialog, ListRow
from vfxui.pyside import QtWidgets, QtCore

class MyListRow(ListRow):
    def defineLeftLayout(self):
        btn = self.addButton(widget_id='btn_in_row', label='>>', width=80, height=15)
        btn.setToolTip('<img src="C:/DATA/JOBS/ALMARAI_Obesity_CIF_18_001/almarai.png">')


    def defineRightLayout(self):
        self.addStretch()

        # img = self.addImage(image_path='C:/DATA/JOBS/ALMARAI_Obesity_CIF_18_001/almarai.png', height=50)
        # img.setToolTip('<img src="C:/DATA/JOBS/ALMARAI_Obesity_CIF_18_001/almarai.png">')

        self.addLabel(label='XXX')

    def slot_btn_in_row_released(self):
        print('YESSSS {} {} {}'.format(self.value, self.index, self.listrow.index))



class TestDialog(Dialog):
    def initialize(self, **kwargs):
        self.height = 500
        self.width = 800

    def defineLayout(self):
        self.box = self.addListBox(widget_id='listbox',
                                   filtering=True,
                                   multiselect=True,
                                   selection_controls = True,
                                   selection_control_position='inline')
                                   # filter_row_height=50)
                                   # row_height=100)

        print(self.getWidgetDetails(self.box))
        content = []
        labels = ['foo', 'bar', 'fizz', 'buzz']
        for index, label in enumerate(labels):
            row = MyListRow(value=label, index=index)

            content.append(row)

        self.box.addItems(content)

        self.addButton(widget_id='btn_change',
                       label='Interact...')
        self.addButton(widget_id='btn_add',
                       label='Add...')
        self.addButton(widget_id='btn_clear',
                       label='clear')
        self.addButton(widget_id='btn_selected',
                       label='print selected')
        self.addButton(widget_id='btn_delete',
                       label='delete selected')
        self.addButton(widget_id='btn_hide',
                       label='Hide selected')
        self.addButton(widget_id='btn_show',
                       label='Show all')


    def slot_listbox_itemClicked(self):
        print('clicked!!')
    def slot_listbox_itemActivated(self):
        print('activated!!')
    def slot_listbox_selectAll(self):
        print('ALLLLLLL!!!!')

    def slot_btn_show_released(self):

        for i in range(self.box.count()):
            item = self.box.item(i)
            item.setHidden(False)

    def slot_btn_hide_released(self):
        for item in self.box.selectedItems():
            item.setSelected(False)
            item.setHidden(True)

        print(len(self.box.selectedItems()))

    def slot_btn_delete_released(self):
        for item in self.box.selectedItems():
            self.box.removeItem(item)
            self.box.takeItem(self.box.row(item))

        print('xxx {}'.format(item.text()))

    def slot_btn_selected_released(self):
        for item in self.box.selectedItems():
            print('{}: {} --> {}'.format(item.index,
                                         item.text(),
                                         item.value.index))


    def slot_btn_change_released(self):
        print(self.box.count())
        for i in range(self.box.count()):
            item = self.box.item(i)
            print(item.__class__)
            print(item.text())

        if self.box.count() > 2:
            self.box.item(1).setSelected(True)
            self.box.item(2).setText('Haha!!!')

    def slot_btn_add_released(self):
        self.box.addItem('fkfkfkfkf')
        new_row = ListRow(value='new ListRow', index=99)
        self.box.addItem(new_row)

    def slot_btn_clear_released(self):
        self.box.clear()

def doIt():
    dlg = createDialog(targetclass=TestDialog)

    dlg.showModal()

if __name__ == '__main__':
    doIt()

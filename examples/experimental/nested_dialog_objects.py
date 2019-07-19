import sys
import time

from vfxui.dialog import Dialog, createDialog


class MyRow(Dialog):

    def initialize(self, row_id, content_string, **kwargs):
        self.content = content_string
        self.row_id = row_id

    def defineLayout(self):
        self.openRow()
        self.addButton(widget_id='btn_right', label='>>')
        self.addStretch()
        self.addSpacer(40)
        self.label = self.addLabel(label=self.content)
        self.addSpacer(40)
        self.addStretch()
        self.addButton(widget_id='btn_left', label='<<')

    def reset(self):
        self.label.setText(self.content)

    def slot_btn_right_released(self):
        self.label.setText('{}{}'.format(self.row_id, self.label.text()))

    def slot_btn_left_released(self):
        self.label.setText('{}{}'.format(self.label.text(), self.row_id))


class MyDialog(Dialog):

    def initialize(self, **kwargs):
        self.width=900
        self.title = 'Booyah!'
        self.contents = ['first line',
                    "I'm pretty stoked",
                    'this is fucking awesome']
        self.rows = []


    def defineLayout(self):
        self.addLabel(label='Hell Yeah!!!')

        for index, content in enumerate(self.contents):
            row = MyRow(row_id=index, content_string=content)
            self.insertWidget(row)
            self.rows.append(row)

        self.addSpacer(50)
        self.addButton(widget_id='proof_btn', label='Reset...')

    def slot_proof_btn_released(self):
        for row in self.rows:
            value = row.label.text()
            print('YAY! {}'.format(value))
            row.reset()



def doIt():
    foo = createDialog(targetclass=MyDialog)
    print(foo.showModal())


if __name__ == '__main__':
    doIt()

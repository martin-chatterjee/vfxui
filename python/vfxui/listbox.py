# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2020, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
##\brief
import os
import sys
import re

from .pyside import QtCore, QtGui, QtWidgets
from .imagelabel import ImageLabel

from .guard import Guard


# -----------------------------------------------------------------------------
class FilterLine(QtWidgets.QWidget):
    """
    """

    filterTabPressed = QtCore.Signal()

    # -------------------------------------------------------------------------
    def conformPath(self, path):
        """
        """
        filename = sys.modules[self.__class__.__module__].__file__
        source_dir = os.path.abspath(os.path.dirname(filename))

        cwd = os.getcwd()
        try:
            os.chdir(source_dir)
            path = os.path.abspath(path).replace('\\', '/')
        finally:
            os.chdir(cwd)
        return path

    # -------------------------------------------------------------------------
    def __init__(self,
                 row_height,
                 placeholder='Filter...',
                 less_prominent=False,
                 parent=None,
                 **kwargs):
        """
        """
        super(FilterLine, self).__init__(parent=parent)

        self.less_prominent = less_prominent

        image_search = QtGui.QPixmap(self.conformPath('ressources/search.png'))
        image_clear = QtGui.QPixmap(self.conformPath('ressources/clear.png'))

        self.search_icon = ImageLabel(image=image_search)
        self.search_icon.setFixedHeight(row_height)
        if self.less_prominent is True:
            self.search_icon.setProperty('labelClass', 'searchIcon_lessProminent')
        else:
            self.search_icon.setProperty('labelClass', 'searchIcon')

        self.filter_line = QtWidgets.QLineEdit()
        self.filter_line.setPlaceholderText(placeholder)
        self.filter_line.setFixedHeight(row_height)
        if self.less_prominent is True:
            self.filter_line.setProperty('labelClass', 'lessProminent')

        self._dealWithCustomFont(self.filter_line, kwargs)

        shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key_Tab),
            self.filter_line,
            context= QtCore.Qt.WidgetWithChildrenShortcut,
            activated=self.slot_filter_line_filterTabPressed)

        self.clear_icon = ImageLabel(image=image_clear)
        self.clear_icon.setProperty('labelClass', 'clearIcon')
        if self.less_prominent is True:
            self.clear_icon.setProperty('labelClass', 'clearIcon_lessProminent')
        self.clear_icon.setFixedHeight(row_height)

        self.clear_icon.clicked.connect(self.slot_clear_clicked)
        self.clear_icon.setCursor(QtCore.Qt.PointingHandCursor)
        self.clear_icon.setToolTip('Clear Filter')
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.search_icon)
        self.layout.addWidget(self.filter_line)
        self.layout.addWidget(self.clear_icon)
        self.setLayout(self.layout)

    # -------------------------------------------------------------------------
    def _dealWithCustomFont(self, widget, kwargs):
        """
        """
        if 'font' in kwargs:
            with Guard():
                font = kwargs['font']
                font_size = 10
                if 'font_size' in kwargs:
                    font_size = int(kwargs['font_size'])
                font_spacing = 0.0
                if 'font_spacing' in kwargs:
                    font_spacing = float(kwargs['font_spacing'])

                font_weight = QtGui.QFont.Normal
                if 'font_weight' in kwargs:
                    value = kwargs['font_weight'].lower()
                    font_weight_values = {
                                            'normal' : QtGui.QFont.Normal,
                                            'light' : QtGui.QFont.Light,
                                            'demibold' : QtGui.QFont.DemiBold,
                                            'bold' : QtGui.QFont.Bold,
                                            'black' : QtGui.QFont.Black
                                         }
                    if value in font_weight_values:
                        font_weight = font_weight_values[value]
                custom_font = QtGui.QFont(font, font_size)
                custom_font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, font_spacing)
                custom_font.setWordSpacing(font_spacing)
                custom_font.setWeight(font_weight)
                widget.setFont(custom_font)

        if 'font_size' in kwargs:
            with Guard():
                font_size = int(kwargs['font_size'])
                font = widget.font()
                font.setPointSize(font_size)
                widget.setFont(font)

    # -------------------------------------------------------------------------
    def slot_filter_line_filterTabPressed(self):
        """
        """
        self.filterTabPressed.emit()


    # -------------------------------------------------------------------------
    def getFilterTokens(self):
        """
        """
        filter_line = self.filter_line.text().strip().lower()
        tokens = re.split(r'[,; ]', filter_line)
        result = [x for x in tokens if x != '']
        return result

    # -------------------------------------------------------------------------
    def slot_clear_clicked(self):
        self.filter_line.setText('')

    # -------------------------------------------------------------------------
    def __getattr__(self, attr):
        """
        """
        if hasattr(self.filter_line, attr):
            return getattr(self.filter_line, attr)



# -----------------------------------------------------------------------------
class ListBox(QtWidgets.QWidget):
    """
    """
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    itemActivated = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemClicked = QtCore.Signal(QtWidgets.QListWidgetItem)
    currentItemChanged = QtCore.Signal(QtWidgets.QListWidgetItem, QtWidgets.QListWidgetItem)
    currentRowChanged = QtCore.Signal(int)
    currentTextChanged = QtCore.Signal(str)
    itemChanged = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemDoubleClicked = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemEntered = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemPressed = QtCore.Signal(QtWidgets.QListWidgetItem)
    itemSelectionChanged = QtCore.Signal()

    filterChanged = QtCore.Signal()
    filterTabPressed = QtCore.Signal()
    filterCleared = QtCore.Signal()
    filterReturnPressed = QtCore.Signal()

    selectAll = QtCore.Signal()
    selectNone = QtCore.Signal()
    selectInvert = QtCore.Signal()

    # -------------------------------------------------------------------------
    def __init__(self,
                 row_height=25,
                 filter_row_height=35,
                 multiselect=False,
                 filtering=False,
                 selection_controls=False,
                 selection_control_position='left',
                 placeholder='Search',
                 select_first_filtered=False,
                 filter_less_prominent=False,
                 parent=None,
                 **kwargs):
        """
        """
        super(ListBox, self).__init__(parent=parent)

        self._kwargs = kwargs
        self.__ignore_keypress = False

        self.row_height = row_height
        self.filter_row_height = filter_row_height
        self.multiselect = multiselect
        self.filtering = filtering
        self.selection_controls = selection_controls
        self.selection_control_position = selection_control_position
        self.placeholder = placeholder
        self.select_first_filtered = select_first_filtered
        self.filter_less_prominent = filter_less_prominent
        if self.filter_row_height < 35:
            self.filter_row_height = 35
        if not self.multiselect:
            self.selection_controls = False
        if not self.selection_control_position in ['left', 'center', 'right', 'inline']:
            self.selection_control_position = 'left'
        if self.filtering is False and self.selection_control_position == 'inline':
            self.selection_control_position = 'left'

        self.defineLayout(**kwargs)

    # -------------------------------------------------------------------------
    def defineLayout(self, **kwargs):
        """
        """
        # prepare filter line
        if self.filtering is True:
            self.filter = FilterLine(placeholder=self.placeholder,
                                     row_height=self.filter_row_height,
                                     less_prominent=self.filter_less_prominent,
                                     parent=self,
                                     **kwargs)
            self.filter.filter_line.textChanged.connect(
                                            self.slot_filter_line_textChanged)
            self.filter.clear_icon.clicked.connect(
                                            self.slot_filter_line_clear_clicked)
            self.filter.filter_line.returnPressed.connect(
                                            self.slot_filter_line_returnPressed)

            self.filter.filterTabPressed.connect(
                                            self.slot_filter_line_filterTabPressed)

        # prepare selection controls
        if self.selection_controls is True:
            self.label_select = QtWidgets.QLabel('Select:')
            self.label_select.setProperty('labelClass', 'labelSelect')
            self.btn_all = QtWidgets.QPushButton('All')
            self.btn_all.setFixedWidth(45)
            self.btn_all.setProperty('labelClass', 'selectionControl')
            self.btn_all.released.connect(self.slot_btn_all_released)
            self.btn_none = QtWidgets.QPushButton('None')
            self.btn_none.setFixedWidth(45)
            self.btn_none.setProperty('labelClass', 'selectionControl')
            self.btn_none.released.connect(self.slot_btn_none_released)
            self.btn_invert = QtWidgets.QPushButton('Invert')
            self.btn_invert.setFixedWidth(45)
            self.btn_invert.setProperty('labelClass', 'selectionControl')
            self.btn_invert.released.connect(self.slot_btn_invert_released)
            if self.selection_control_position == 'inline':
                self.btn_all.setFixedHeight(self.filter_row_height - 4)
                self.btn_none.setFixedHeight(self.filter_row_height - 4)
                self.btn_invert.setFixedHeight(self.filter_row_height - 4)

        # prepare list widget
        self.list = QtWidgets.QListWidget() #**kwargs)
        if self.multiselect is True:
            self.list.setSelectionMode(
                        QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list.itemActivated.connect(self.slot_list_itemActivated)
        self.list.itemClicked.connect(self.slot_list_itemClicked)
        self.list.currentItemChanged.connect(self.slot_list_currentItemChanged)
        self.list.currentRowChanged.connect(self.slot_list_currentRowChanged)
        self.list.currentTextChanged.connect(self.slot_list_currentTextChanged)
        self.list.itemChanged.connect(self.slot_list_itemChanged)
        self.list.itemDoubleClicked.connect(self.slot_list_itemDoubleClicked)
        self.list.itemEntered.connect(self.slot_list_itemEntered)
        self.list.itemPressed.connect(self.slot_list_itemPressed)
        self.list.itemSelectionChanged.connect(self.slot_list_itemSelectionChanged)





        # prepare layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # add filter row
        if self.filtering is True:
            self.wdg_filterline = QtWidgets.QWidget()
            layout_filterline = QtWidgets.QHBoxLayout()
            layout_filterline.setContentsMargins(0, 0, 0, 0)
            layout_filterline.setSpacing(0)
            self.wdg_filterline.setLayout(layout_filterline)
            self.layout.addWidget(self.wdg_filterline)
            self.layout.addSpacing(5)

            layout_filterline.addWidget(self.filter)

            if self.selection_controls is True:
                if self.selection_control_position == 'inline':
                    self._addControlsToLayout(layout_filterline)

        # add row for selection controls
        if self.selection_controls is True:
            if self.selection_control_position in ['left', 'center', 'right']:
                self.wdg_controls = QtWidgets.QWidget()
                layout_controls = QtWidgets.QHBoxLayout()
                layout_controls.setContentsMargins(0, 0, 0, 0)
                layout_controls.setSpacing(0)
                self.wdg_controls.setLayout(layout_controls)
                self.layout.addWidget(self.wdg_controls)
                self.layout.addSpacing(5)

                self._addControlsToLayout(layout_controls)

        # add the actual listbox
        self.layout.addWidget(self.list)



    # -------------------------------------------------------------------------
    def hideRow(self, row_index):
        """
        """
        item = self.list.item(row_index)
        item.setHidden(True)
        item.visible = False

    # -------------------------------------------------------------------------
    def showRow(self, row_index):
        """
        """
        item = self.list.item(row_index)
        item.setHidden(False)
        item.visible = True

    # -------------------------------------------------------------------------
    def _addControlsToLayout(self, layout):
        """
        """
        if self.selection_control_position == 'left':
            layout.addSpacing(12)
        if self.selection_control_position in ['center', 'right']:
            layout.addStretch()
        if self.selection_control_position == 'inline':
            layout.addSpacing(10)

        layout.addWidget(self.label_select)
        layout.addSpacing(10)
        layout.addWidget(self.btn_all)
        layout.addSpacing(5)
        layout.addWidget(self.btn_none)
        layout.addSpacing(5)
        layout.addWidget(self.btn_invert)

        if self.selection_control_position in ['left', 'center']:
            layout.addStretch()
        if self.selection_control_position == 'right':
            layout.addSpacing(2)

    # -------------------------------------------------------------------------
    def slot_btn_all_released(self):

        for i in range(self.list.count()):
            item = self.list.item(i)
            item.setSelected(False)

            if item.isHidden() is False:
                item.setSelected(True)
        self.selectAll.emit()

    # -------------------------------------------------------------------------
    def slot_btn_none_released(self):

        for i in range(self.list.count()):
            item = self.list.item(i)
            item.setSelected(False)
        self.selectNone.emit()

    # -------------------------------------------------------------------------
    def slot_btn_invert_released(self):

        for i in range(self.list.count()):
            item = self.list.item(i)

            if item.isHidden() is False:
                item.setSelected(not item.isSelected())
            else:
                item.setSelected(False)
        self.selectInvert.emit()

    # -------------------------------------------------------------------------
    def slot_list_itemActivated(self, item):
        self.itemActivated.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemClicked(self, item):
        self.itemClicked.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_currentItemChanged(self, current, previous):
        self.currentItemChanged.emit(current, previous)

    # -------------------------------------------------------------------------
    def slot_list_currentRowChanged(self, currentRow):
        self.currentRowChanged.emit(currentRow)

    # -------------------------------------------------------------------------
    def slot_list_currentTextChanged(self, item):
        self.currentTextChanged.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemChanged(self, item):
        self.itemChanged.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemDoubleClicked(self, item):
        self.itemDoubleClicked.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemEntered(self, item):
        self.itemEntered.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemPressed(self, item):
        self.itemPressed.emit(item)

    # -------------------------------------------------------------------------
    def slot_list_itemSelectionChanged(self):
        self.itemSelectionChanged.emit()

    # -------------------------------------------------------------------------
    def slot_filter_line_textChanged(self):
        # update filtering
        self.filterChanged.emit()
        self.filterRows()

    # -------------------------------------------------------------------------
    def slot_filter_line_clear_clicked(self):
        self.filterCleared.emit()
        self.filterRows()

    # -------------------------------------------------------------------------
    def slot_filter_line_returnPressed(self):
        self.filterReturnPressed.emit()

    # -------------------------------------------------------------------------
    def slot_filter_line_filterTabPressed(self):
        self.filterTabPressed.emit()

    # -------------------------------------------------------------------------
    def removeSelection(self):
        for i in range(self.list.count()):
            row = self.list.item(i)
            row.setSelected(False)

    # -------------------------------------------------------------------------
    def filterRows(self):
        filter_tokens = self.filter.getFilterTokens()
        for i in range(self.list.count()):
            row = self.list.item(i)
            if row.visible is False:
                continue
            row.setHidden(False)
            row.setSelected(False)

            exclude_row = False
            if len(filter_tokens) > 0:
                exclude_row = True
                try:
                    filter_keywords = row.value.filter_keywords
                except AttributeError as e:
                    filter_keywords = str(row.value).lower()
                for token in filter_tokens:
                    if token in filter_keywords:
                        exclude_row = False
                        break

            if exclude_row:
                row.setHidden(True)

        if self.select_first_filtered:
            if len(filter_tokens) > 0:
                # auto-select first entry
                for i in range(self.list.count()):
                    row = self.list.item(i)
                    if row.isHidden() is False:
                        row.setSelected(True)
                        break

    # -------------------------------------------------------------------------
    @property
    def ignore_keypress(self):
        """
        """
        return self.__ignore_keypress

    # -------------------------------------------------------------------------
    @ignore_keypress.setter
    def ignore_keypress(self, value):
        """
        """
        self.__ignore_keypress = False
        if value == True:
            self.__ignore_keypress = True


    # -------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """
        """
        result = self.keyPressed.emit(event)

        if not self.ignore_keypress:
            self.list.keyPressEvent(event)

        super(ListBox, self).keyPressEvent(event)

    # -------------------------------------------------------------------------
    def visibleItems(self):
        """
        """
        items = []
        for i in range(self.list.count()):
            item = self.list.item(i)
            if item.isHidden() == False:
                items.append(item)
        return items

    # -------------------------------------------------------------------------
    def allItems(self):
        """
        """
        items = []
        for i in range(self.list.count()):
            item = self.list.item(i)
            items.append(item)
        return items

    # -------------------------------------------------------------------------
    def removeItem(self, item):
        """
        """
        for i in range(self.list.count()):
            row = self.list.item(i)
            if row.text() == item:
                self.takeItem(i)
                self._refreshIndices()
                break

    # -------------------------------------------------------------------------
    def _refreshIndices(self):
        """
        """
        for index in range(self.count()):
            item = self.item(index)
            item.index = index

    # -------------------------------------------------------------------------
    def addItem(self, item):
        """
        """
        if hasattr(item, 'is_list_row'):
            item._listbox = self

        item = ListWidgetItem(value=item,
                              index=self.count(),
                              **self._kwargs)
        item.visible = True
        size_hint = QtCore.QSize(0, self.row_height)
        item.setSizeHint(size_hint)

        self.list.addItem(item)
        if item.value_type > 0:
            self.setItemWidget(item, item.content)

    # -------------------------------------------------------------------------
    def addItems(self, rows):
        """
        """
        for index, item in enumerate(rows):
            self.addItem(item)

    # -------------------------------------------------------------------------
    def getFilterTokens(self):
        """
        """
        return self.filter.getFilterTokens()

    # -------------------------------------------------------------------------
    def __getattr__(self, attr):
        """
        """
        if hasattr(self.list, attr):
            return getattr(self.list, attr)





# -----------------------------------------------------------------------------
class ListWidgetItem(QtWidgets.QListWidgetItem):
    """
    """

    # -------------------------------------------------------------------------
    def __init__(self,
                 value,
                 index,
                 *args,
                 **kwargs):
        """
        """
        # super(ListWidgetItem, self).__init__()
        super(ListWidgetItem, self).__init__()

        self.value = value
        self.index = index

        self._dealWithCustomFont(kwargs)

        self.value_type = 0 # string


        if isinstance(self.value, QtWidgets.QWidget):
            self.value_type = 1 # QWidget
            if hasattr(self.value, 'is_list_row'):
                self.value.build()
                self.value_type = 2 # ListRow

        # deal with plain string value
        if self.value_type == 0:
            self.setText('{}'.format(self.value))
            return

        # vertically center value
        self.content = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch()
        layout.addWidget(self.value)
        layout.addStretch()

        self.content.setLayout(layout)


    # -------------------------------------------------------------------------
    def _dealWithCustomFont(self, kwargs):
        """
        """
        if 'font' in kwargs:
            with Guard():
                font = kwargs['font']
                font_size = 10
                if 'font_size' in kwargs:
                    font_size = int(kwargs['font_size'])
                font_spacing = 0.0
                if 'font_spacing' in kwargs:
                    font_spacing = float(kwargs['font_spacing'])

                font_weight = QtGui.QFont.Normal
                if 'font_weight' in kwargs:
                    value = kwargs['font_weight'].lower()
                    font_weight_values = {
                                            'normal' : QtGui.QFont.Normal,
                                            'light' : QtGui.QFont.Light,
                                            'demibold' : QtGui.QFont.DemiBold,
                                            'bold' : QtGui.QFont.Bold,
                                            'black' : QtGui.QFont.Black
                                         }
                    if value in font_weight_values:
                        font_weight = font_weight_values[value]
                custom_font = QtGui.QFont(font, font_size)
                custom_font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, font_spacing)
                custom_font.setWordSpacing(font_spacing)
                custom_font.setWeight(font_weight)
                self.setFont(custom_font)


        if 'font_size' in kwargs:
            with Guard():
                font_size = int(kwargs['font_size'])
                font = self.font()
                font.setPointSize(font_size)
                self.setFont(font)

    # -------------------------------------------------------------------------
    def text(self):
        """
        """
        if self.value_type == 2:
            return self.value.value
        else:
            return super(ListWidgetItem, self).text()


    # -------------------------------------------------------------------------
    def setText(self, value):
        """
        """
        if self.value_type == 2:
            self.value.value = value
            self.value.update()
        else:
            super(ListWidgetItem, self).setText(value)





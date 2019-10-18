# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------

##\file
"""
Build and use Dialogs independent of DCC and context.

"""

import os
import sys
import time
import importlib
import logging

from .pyside import QtCore, QtGui, QtWidgets

from .filebrowser import FileBrowser
from .imagelabel import ImageLabel
from .listbox import ListBox
from .divider import Divider
from .guard import Guard

maya_main_window = None
try: # pragma: no cover
    import maya.OpenMayaUI as omui
    from .pyside import shiboken
    ptr = omui.MQtUtil.mainWindow()
    maya_main_window = shiboken.wrapInstance(long(ptr), QtWidgets.QWidget)
except:
    pass

logger = logging.getLogger('vfxui')
"""vfxtest logger"""

# -----------------------------------------------------------------------------
def initLogging(level=logging.INFO,
                format='%(message)s'):
    """Initializes the vfxui logger.

    Args:
        level            : log level
                           Optional, defaults to logging.INFO
        format (string)  : tokenized string describing the log format
                           Optional, defaults to plain message logging:
                           '%(message)s'

    """
    logger = logging.getLogger('vfxui')
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    console = logging.StreamHandler()
    formatter = logging.Formatter(format)
    console.setFormatter(formatter)
    console.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(console)


initLogging()


# -----------------------------------------------------------------------------
class Dialog(QtWidgets.QDialog):
    """Allows to create and use Dialogs independent of DCC and context.

    Users can create Dialog objects directly for smallish UI's,
    or will build a class inheriting from `Dialog` for bigger UI's.

    Implements all core level functionality for Dialogs.
    Also takes care of preventing issues with Maya's outliner.

    For a good starting point please have a look at the examples in
        examples/sehsucht.ui/.

    """

    ## handle of the current QApplication handle
    app = None

    dialogOpen = QtCore.Signal()
    _font_db = None
    _loaded_fonts = []
    _core_css = None

    _context = None

    # -------------------------------------------------------------------------
    def __init__(self, parent=None, **kwargs):
        """Initializer.

        Args:
            parent (optional):     parent window handle. Defaults to None.
            kwargs (optional):     keyword arguments passing property values.

        """
        super(Dialog, self).__init__()

        ## if True the size can not be changed by user.
        self.__fixed_size = False
        ## dialog width.
        self.__width = 200
        ## dialog height.
        self.__height = 200
        ## dialog title.
        self.__title = 'Dialog'

        self.__is_child_widget = False

        ## full path to the file of the current class implementation
        self.__source_filename = None
        ## full path to the folder of the current class implementation
        self.__source_dir = None

        self._storeWorkingDirAndFile()

        self._btn_modal_ok = None
        self._btn_modal_cancel = None

        self.__scrollable = False
        if 'scrollable' in kwargs:
            if kwargs['scrollable'] is True:
                self.__scrollable = True

        self.__disable_return_escape = False
        if 'no_return_escape' in kwargs:
            if kwargs['no_return_escape'] == True:
                self.__disable_return_escape = True

        self.__test_mode = False
        if 'test_mode' in kwargs:
            if kwargs['test_mode'] is not False:
                if kwargs['test_mode'] == 'cancel':
                    self.test_mode = 'cancel'
                else:
                    self.test_mode = 'ok'

        self.__test_display_length = 1000 # milliseconds
        if 'test_display_length' in kwargs:
            tdl = kwargs['test_display_length']
            self.test_display_length = tdl

        ## add minimize button
        self.setWindowFlags(self.windowFlags() |
                            QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowSystemMenuHint)

        ## flag to store if UI got created
        self.__created = False
        ## stores if the last viewing was modal
        self.__last_view_modal = False
        ## return value of a modal dialog
        self.__modal_return_value = True
        ## set focus to this widget
        self._focussed_widget = None
        ## empty widget to accept focus
        self._focus_catching_widget = None

        self._add_last_stretch = True

        ## main layout
        self._layout_main = QtWidgets.QVBoxLayout()

        ## dictionary of managed widgets (with names as keys)
        self._widgets = {}
        ## current active layout structures
        self._openStructures = []

        self._css = ''

        # deal with optional property values
        self._setPropertiesFromKwargs(**kwargs)
        # load fonts and CSS
        self.loadFontsAndCss()

        self.initialize(**kwargs)

        self._connectSignalsToSlots(self, '')

        self.__ui_built = False

    # -------------------------------------------------------------------------
    @property
    def is_child_widget(self):
        """
        """
        return self.__is_child_widget
    @is_child_widget.setter
    def is_child_widget(self, value):
        self.__is_child_widget = False
        if value is True:
            self.__is_child_widget = True

    # -------------------------------------------------------------------------
    @property
    def ui_built(self):
        return self.__ui_built

    # -------------------------------------------------------------------------
    @property
    def last_view_modal(self):
        return self.__last_view_modal

    # -------------------------------------------------------------------------
    @property
    def source_dir(self):
        return self.__source_dir
    # -------------------------------------------------------------------------
    @property
    def source_filename(self):
        return self.__source_filename

    # -------------------------------------------------------------------------
    @property
    def scrollable(self):
        return self.__scrollable
    # -------------------------------------------------------------------------
    @scrollable.setter
    def scrollable(self, value):
        if value is True:
            self.__scrollable = True
        else:
            self.__scrollable = False

    # -------------------------------------------------------------------------
    @property
    def add_last_stretch(self):
        return self._add_last_stretch
    # -------------------------------------------------------------------------
    @add_last_stretch.setter
    def add_last_stretch(self, value):
        if value is True:
            self._add_last_stretch = True
        else:
            self._add_last_stretch = False

    # -------------------------------------------------------------------------
    @property
    def focussed_widget(self):
        result = None
        for item in self._widgets.keys():
            if self._widgets[item].hasFocus():
                result = self._widgets[item]
                break
        return result

    # -------------------------------------------------------------------------
    @property
    def test_mode(self):
        return self.__test_mode

    # -------------------------------------------------------------------------
    @test_mode.setter
    def test_mode(self, value):
        self.__test_mode = value

    # -------------------------------------------------------------------------
    @property
    def test_display_length(self):
        return self.__test_display_length
    # -------------------------------------------------------------------------
    @test_display_length.setter
    def test_display_length(self, value):
        with Guard():
            safety = int(value)
            self.__test_display_length = safety

    # -------------------------------------------------------------------------
    @property
    def modal_return_value(self):
        return self.__modal_return_value
    # -------------------------------------------------------------------------
    @modal_return_value.setter
    def modal_return_value(self, value):
        if value == True:
            self.__modal_return_value = True
        else:
            self.__modal_return_value = False

    # -------------------------------------------------------------------------
    @property
    def disable_return_escape(self):
        return self.__disable_return_escape
    # -------------------------------------------------------------------------
    @disable_return_escape.setter
    def disable_return_escape(self, value):
        if value == True:
            self.__disable_return_escape = True
        else:
            self.__disable_return_escape = False

    # -------------------------------------------------------------------------
    @property
    def created(self):
        return self.__created

    # -------------------------------------------------------------------------
    @property
    def context(self):
        if Dialog._context is None:
            self._resolveContext()
        return Dialog._context

    # -------------------------------------------------------------------------
    @property
    def width(self):
        return self.__width
    # -------------------------------------------------------------------------
    @width.setter
    def width(self, value):
        with Guard():
            legal_width = int(value)
            if legal_width > 0:
                self.__width = legal_width

    # -------------------------------------------------------------------------
    @property
    def height(self):
        return self.__height
    # -------------------------------------------------------------------------
    @height.setter
    def height(self, value):
        with Guard():
            legal_height = int(value)
            if legal_height > 0:
                self.__height = legal_height

    # -------------------------------------------------------------------------
    @property
    def fixed_size(self):
        return self.__fixed_size
    # -------------------------------------------------------------------------
    @fixed_size.setter
    def fixed_size(self, value):
        if value in [1, True, 'True', 'true']:
            self.__fixed_size = True
        else:
            self.__fixed_size = False

    # -------------------------------------------------------------------------
    @property
    def title(self):
        return self.__title
    # -------------------------------------------------------------------------
    @title.setter
    def title(self, value):
        if isinstance(value, str) or isinstance(value, unicode):
            self.__title = ('%s' % value).strip()
            self.setWindowTitle(self.__title)
            self.redraw()

    # -------------------------------------------------------------------------
    def setWidthHeight(self, width, height):
        """Sets the dialog width and height.

        Args:
            width (int)     : dialog width in pixels
            height (int)     : dialog height in pixels

        """
        self.width = width
        self.height = height

    # -------------------------------------------------------------------------
    def initialize(self, **kwargs):
        """Let's you initialize things before the actual dialog creation.

        Implement initialize() in your dialog class.

        """

    # -------------------------------------------------------------------------
    def defineLayout(self):
        """Defines the widgets and layout of this dialog.

        Implement defineLayout() in your dialog class.

        """

    # -------------------------------------------------------------------------
    def postConstructLayout(self):
        """Gets called after defineLayout() is finished, but before the Dialog
        gets displayed.

        Implement postConstructLayout() in your dialog class if needed.

        """

    # -------------------------------------------------------------------------
    def setAsSplashScreen(self):
        """Flags the current dialog window type to act as a splash screen.

        """
        if not self.is_child_widget:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.SplashScreen)
            self.setProperty('labelClass', 'splashscreen')

    # -------------------------------------------------------------------------
    def addTabsGroup(self, widget_id='tabsgroup'):
        """Adds a Tab Manager.

        Call addTabsGroup() and then create the actual tabs in it by calling
        openTab().

        Args:
            widget_id (string) : unique id for this widget
        Returns:
            QTabWidget, or None

        """
        result = None
        # create widget
        widget = QtWidgets.QTabWidget()
        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def openTab(self, tab_widget, widget_id='tab', label=''):
        """Opens a tab in a tab manager.

        Args:
            tab_widget (QTabWidget) : QTabWidget from addTabsGroup()
            widget_id (string)      : unique id for this widget
            label (string)          : label for this Tab

        Returns:
            QWidget representing this Tab

        """
        result = None

        if tab_widget:
            tab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            tab.setLayout(layout)

            # store widget
            widget_id = self._storeWidget(tab, widget_id, add_to_layout=False)
            tab_widget.addTab(tab, label)
            self._addOpenStructure(tab_widget, layout)
            result = tab

        return result

    # -------------------------------------------------------------------------
    def openGroup(self,
                  widget_id='group',
                  label='',
                  frame=True,
                  prominent=True,
                  **kwargs):
        """Opens a group with optional label and displayed frame.

        Args:
            widget_id (string)      : unique id for this widget
            label (string)          : label for this Group
            frame (bool)            : if True draws Frame for this group
            prominent (bool)        : if False dims/greys out group label and frame
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Group, or None

        """
        #create group
        group = None
        group = QtWidgets.QGroupBox(label)
        label_classes = []
        if frame is False:
            label_classes.append('no_frame')
        if label == '':
            label_classes.append('no_label')
        if prominent is False:
            label_classes.append('less_prominent')


        group.setProperty('labelClass', '_'.join(label_classes))

        self._processKwargs(group, kwargs)

        # store widget
        widget_id = self._storeWidget(group, widget_id, add_to_layout=False)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._addOpenStructure(group, layout)

        return group

    # -------------------------------------------------------------------------
    def openScrollable(self,
                  widget_id='scrollarea',
                  **kwargs):
        """Opens a scrollable area.

        Args:
            widget_id (string)      : unique id for this widget
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Scrollable Area, or None

        """
        scrollarea = QtWidgets.QScrollArea()
        scrollarea.setWidgetResizable(True)

        scroll_widget = QtWidgets.QWidget(scrollarea)
        scrollarea.setWidget(scroll_widget)

        self._processKwargs(scrollarea, kwargs)

        # store widget
        widget_id = self._storeWidget(scrollarea, widget_id, add_to_layout=False)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._addOpenStructure(scrollarea, layout)

        return scrollarea

    # -------------------------------------------------------------------------
    def openRow(self, **kwargs):
        """Opens a Row.

        Returns:
            QWidget representing the Row content, or None

        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._addOpenStructure(widget, layout)
        self._processKwargs(widget, kwargs)
        return widget

    # -------------------------------------------------------------------------
    def openWrappedRow(self, **kwargs):
        """Opens a wrapped Row.

        Returns:
            QWidget representing the Row content, or None

        """
        widget = QtWidgets.QWidget()
        layout = WrappedRowLayout(**kwargs)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._addOpenStructure(widget, layout)
        self._processKwargs(widget, kwargs)
        return widget

    # -------------------------------------------------------------------------
    def openColumn(self, **kwargs):
        """Opens a column.

        Returns:
            QWidget representing the Column content, or None

        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._addOpenStructure(widget, layout)
        self._processKwargs(widget, kwargs)
        return widget

    # -------------------------------------------------------------------------
    def closeRow(self):
        """Closes a row.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def closeWrappedRow(self):
        """Closes a wrapped row.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def closeColumn(self):
        """Closes a column.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def closeGroup(self):
        """Closes a group.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def closeScrollable(self):
        """Closes a scrollable area.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def closeTab(self):
        """Closes a tab.

        """
        return self._closeStructure()

    # -------------------------------------------------------------------------
    def addDivider(self, horizontal=True, thickness=1, align='center', **kwargs):
        """Adds a divider.

        Args:
            horizontal (bool)       : if True draws horizontal divider
                                      if False draws vertical divider
            thickness (int)         : thickness of the divider
            align (string)          : controls alignment of widget in layout.
                                      Supported: 'center', 'left', 'right'
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Divider, or None

        """
        # create widget
        widget = Divider(horizontal=horizontal,
                         thickness=thickness,
                         align=align,
                         **kwargs)

        self._processKwargs(widget.line, kwargs)

        # add to active layout
        self._getActiveLayout().addWidget(widget)

        return widget

    # -------------------------------------------------------------------------
    def addSpacer(self, dimension=10):
        """Adds a spacer.

        Depending on the current active layout (row or column) the spacer
        behaves in the expected way automatically.

        Args:
            dimension (int)      : dimension of spacer in pixels

        """
        active_layout = self._getActiveLayout()
        active_layout.addSpacing(dimension)

    # -------------------------------------------------------------------------
    def addStretch(self):
        """Adds a stretch.

        Depending on the current active layout (row or column) the stretch
        behaves in the expected way automatically.

        Returns:
            QWidget representing the stretch, or None

        """
        # create widget
        widget = QtWidgets.QWidget()
        if self._isActiveStructureHorizontal():
            layout = QtWidgets.QHBoxLayout()
        else:
            layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch()
        widget.setLayout(layout)

        # add to active layout
        self._getActiveLayout().addWidget(widget)

        return widget

    # -------------------------------------------------------------------------
    def getWidgetValue(self, widget):
        """Returns the value of the widget.

        Args:
            widget (string, of QWidget) : widget id of the target widget
                                          or the QWidget itself

        Returns:
            value of widget, or None

        """
        if isinstance(widget, str) or isinstance(widget, unicode):
            widget_id = self._conformName(widget)
            if widget_id in self._widgets.keys():
                widget = self._widgets[widget_id]
            else:
                logger.warning("Could not locate Widget for ID '%s'" % widget_id)
                return None

        value = None

        with Guard():
            if type(widget) == QtWidgets.QLineEdit:
                value = widget.text()
            elif type(widget) in [QtWidgets.QTextEdit, QTextEdit]:
                value = widget.toPlainText()
            elif type(widget) == QtWidgets.QComboBox:
                value = (widget.currentIndex(), widget.currentText())
            elif type(widget) == QtWidgets.QCheckBox:
                value = widget.isChecked()
            else:
                value = widget.value()

        return value

    # -------------------------------------------------------------------------
    def showTab(self, tabs_widget, tab):
        """Display the specified tab.

        Args:
            tabs_widget (QTabWidget) : QTabWidget from addTabsGroup()
            tab (QWidget)            : Tab to show

        """
        tabs_widget.setCurrentWidget(tab)

    # -------------------------------------------------------------------------
    def addHeadline(self,
                    widget_id='headline',
                    label='',
                    font='Gotham Light',
                    font_size=20,
                    font_spacing=10.0,
                    **kwargs):
        """Adds a headline.

        Args:
            widget_id (string)      : unique id for this widget
            label (string)          : label of the headline
            font (string)           : target font name.
                                      Defaults to Sehsucht corporate design type.
            font_size (int)         : font size. Defaults to 20
            font_spacing (float)    : font spacing. Defaults to 10.0
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Headline, or None

        """
        result = None

        widget_id = None
        widget = QtWidgets.QLabel(label)
        widget.setAlignment(QtCore.Qt.AlignCenter)

        font_kwargs = {}
        font_kwargs['font'] = font
        font_kwargs['font_size'] = font_size
        font_kwargs['font_spacing'] = font_spacing
        kwargs.update(font_kwargs)

        widget.setProperty('labelClass', 'Headline')

        self._processKwargs(widget, kwargs)

        self.openColumn()

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        self.addSpacer(10)
        self.closeColumn()

        return widget

    # -------------------------------------------------------------------------
    def addLabel(self,
                 widget_id='label',
                 label='',
                 align='left',
                 valign='center',
                 **kwargs):
        """Adds a label.

        Args:
            widget_id (string)      : unique id for this widget
            label (string)          : label for this Label
            align (string)          : align this widget 'left', 'center' or 'right'
                                      Defaults to 'left'
            valign (string)          : align this widget 'top', 'center' or 'bottom'
                                      Defaults to 'center'
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Label, or None

        """
        result = None
        # widget = QtWidgets.QLabel(label)
        widget = ClickableLabel(label)
        if align == 'center':
            h_flag= QtCore.Qt.AlignCenter
        elif align == 'right':
            h_flag = QtCore.Qt.AlignRight
        else:
            # default to 'left'
            h_flag = QtCore.Qt.AlignLeft
        if valign == 'top':
            v_flag= QtCore.Qt.AlignTop
        elif valign == 'bottom':
            v_flag = QtCore.Qt.AlignBottom
        else:
            # default to 'center'
            v_flag = QtCore.Qt.AlignVCenter

        widget.setAlignment(h_flag | v_flag)

        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def conformPath(self, path):
        """Conforms a path and resolves relative paths in relation to
        source_dir.

        Args:
            path (string) : path to resolve

        Returns:
            resolved absolute path

        """
        if path is None:
            return None

        if not self.__source_dir is None:
            if os.path.exists(self.__source_dir):
                wd = os.getcwd()
                os.chdir(self.__source_dir)
                path = os.path.abspath(path)
                os.chdir(wd)

        path = os.path.expandvars(path)
        path = path.replace('\\', '/')

        return path

    # -------------------------------------------------------------------------
    def addImage(self,
                 image_path,
                 image_path_hi=None,
                 widget_id='image',
                 **kwargs):
        """Adds an image.

        Args:
            image_path (string)     : path to image
            image_path_hi (string)  : path to image for the mouse-over state.
                                      (Optional, defaults to None)
            widget_id (string)      : unique id for this widget
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Image, or None

        """
        result = None

        if image_path is None:
            logger.error('not a legal image path:\n%s' % image_path)
            return None

        # legalize paths
        image_path = self.conformPath(image_path)
        image_path_hi = self.conformPath(image_path_hi)
        image = QtGui.QPixmap(image_path)

        image_hi = None
        if image_path_hi is not None:
            image_hi = QtGui.QPixmap(image_path_hi)

        widget = ImageLabel(image, image_hi, working_dir=self.source_dir)

        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def addTextBox(self,
                   widget_id='text',
                   value = '',
                   multiline=False,
                   label=None,
                   label_width=None,
                   expression=None,
                   **kwargs):
        """Adds a text box (either one-line or multi-line).

        Args:
            widget_id (string)      : unique id for this widget
            value (string)          : initial value of this TextBox
            multiline (bool)        : specifies if TextBox is multi-line or oneline
            label (string)          : label for this TextBox.
                                      (optional, defaults to None)
            label_width (int)       : width of label in pixels
                                      (optional, defaults to None)
            expression (string)     : regular expression to control text input
                                      (optional, defaults to None)
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the TextBox, or None

        """
        result = None

        # create widget
        if multiline:
            widget = QTextEdit()
        else:
            widget = QtWidgets.QLineEdit()

        # add expression
        if expression is not None:
            expr = QtCore.QRegExp(expression)
            validator = QtGui.QRegExpValidator(expr)
            widget.setValidator(validator)

        widget.setText(value)
        widget.setAlignment(QtCore.Qt.AlignTop)

        if 'placeholder' in kwargs:
            widget.setPlaceholderText(kwargs['placeholder'])


        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id, add_to_layout=False)

        # deal with label
        if label is not None:
            self.openGroup(frame=False)
            self.openRow()
            label = QtWidgets.QLabel(label)
            if label_width is not None:
                label.setFixedWidth(label_width)
            # TODO is this needed?!?
            if 'labelclass' in kwargs:
                label.setProperty('labelClass', kwargs['labelclass'])

            self._getActiveLayout().addWidget(label)
            self.addSpacer(10)

        # add to active layout
        self._getActiveLayout().addWidget(widget)

        if label is not None:
            self.closeRow()
            self.closeGroup()

        return widget

    # -------------------------------------------------------------------------
    def addFileBrowser(self,
                       widget_id='fileBrowser',
                       mode='open',
                       initialdir='',
                       button_label="...",
                       show_text=True,
                       dialog_caption='',
                       filters=[],
                       selected_file='',
                       label='',
                       height=35,
                       direct_edit=False,
                       **kwargs):
        """Adds a File Browser widget.

        Args:
            widget_id (string)      : unique id for this widget
            mode (string)           : mode of FileBrowser: 'open', 'save', 'folder'
            initialdir (string)     : initial directory
            button_label (string)   : Label of the button
            show_text (bool)        : if True displays picking in read-only TextBox
            dialog_caption (string) : Caption of the fileBrowser dialog
            filters (list)          : list of file filters in the format ['Python (*.py)]'
                                      (optional, defaults to [])
            selected_file (string)  : path of preselected item
                                      (optional, defaults to '')
            label (string)          : Label of the FileBrowser
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the FileBrowser, or None

        """
        result = None
        # create widget
        widget = FileBrowser(label=label,
                             mode=mode,
                             show_text=show_text,
                             button_label=button_label,
                             initialdir=initialdir,
                             selected_file=selected_file,
                             dialog_caption=dialog_caption,
                             filters=filters,
                             direct_edit=direct_edit)

        kwargs['height'] = height
        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def addListBox(self,
                   widget_id='listBox',
                   filtering=False,
                   multiselect=False,
                   selection_controls=False,
                   selection_control_position='left',
                   row_height=25,
                   filter_row_height=35,
                   content=[],
                   **kwargs):
        """Adds a List box.

        Args:
            widget_id (string)      : unique id for this widget
            multiselect (bool)      : if True allows multi selection
                                      (optional, defaults to False)
            content (list)          : list of entries
                                      (optional, defaults to None)
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the ListBox, or None

        """
        result = None
        # create widget
        widget = ListBox(filtering=filtering,
                         multiselect=multiselect,
                         selection_controls=selection_controls,
                         selection_control_position=selection_control_position,
                         row_height=row_height,
                         filter_row_height=filter_row_height,
                         **kwargs)


        # prepare rows
        rows = []
        for index, value in enumerate(content):
            row = value
            if isinstance(value, ListRow):
                row = value
            else:
                row = ListRow(value=value, index=index, **kwargs)
            rows.append(row)
        widget.addItems(rows)

        # widget.addItems(content)

        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def addComboBox(self,
                    widget_id='comboBox',
                    label=None,
                    label_width=None,
                    content=[],
                    value='',
                    **kwargs):
        """Adds a Combo Box.

        Args:
            widget_id (string)      : unique id for this widget
            label (string)          : label for this ComboBox.
                                      (optional, defaults to None)
            label_width (int)       : width of label in pixels
                                      (optional, defaults to None)
            content (list)          : list of entries
                                      (optional, defaults to None)
            value (string)          : selected value
                                      (optional, defaults to '')
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the ComboBox, or None

        """
        result = None
        # create widget
        widget = QtWidgets.QComboBox()
        widget.addItems(content)
        if value in content:
            widget.setCurrentIndex(content.index(value))

        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id, add_to_layout=False)

        # deal with label
        if label is not None:
            self.openGroup(frame=False)
            self.openRow()
            label = QtWidgets.QLabel(label)
            self._processKwargs(label, kwargs)

            if label_width is not None:
                label.setFixedWidth(label_width)
            self._getActiveLayout().addWidget(label)
            self.addSpacer(10)

        # add to active layout
        self._getActiveLayout().addWidget(widget)

        if label is not None:
            # self.addStretch()
            self.closeRow()
            self.closeGroup()

        return widget

    # -------------------------------------------------------------------------
    def addSpinBox(self,
                   widget_id='spinBox',
                   value=0,
                   label=None,
                   label_width=None,
                   **kwargs):
        """Adds a Spin Box for either an Integer or a Float value.

        Args:
            widget_id (string)      : unique id for this widget
            value (int or float)    : value
                                      (optional, defaults to 0)
            label (string)          : label for this SpinBox.
                                      (optional, defaults to None)
            label_width (int)       : width of label in pixels
                                      (optional, defaults to None)
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the SpinBox, or None

        """
        result = None
        # create widget
        if isinstance(value, float):
            widget = QtWidgets.QDoubleSpinBox()
            widget.setMinimum(sys.float_info.min)
            widget.setMaximum(sys.float_info.max)
        else:
            widget = QtWidgets.QSpinBox()
            # max integer that C can store in an int
            max_int = 2147483647
            widget.setMinimum(-max_int-1)
            widget.setMaximum(max_int)

        widget.setValue(value)

        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id, add_to_layout=False)

        # deal with label
        if label is not None:
            self.openRow()
            label = QtWidgets.QLabel(label)
            if label_width is not None:
                label.setFixedWidth(label_width)
            self._getActiveLayout().addWidget(label)
            self.addSpacer(10)

        # add to active layout
        self._getActiveLayout().addWidget(widget)

        if label is not None:
            self.addStretch()
            self.closeRow()

        return widget

    # -------------------------------------------------------------------------
    def addCheckBox(self,
                    widget_id='checkBox',
                    value=True,
                    label=None,
                    **kwargs):
        """Adds a check box.

        Args:
            widget_id (string)      : unique id for this widget
            value (bool)            : value
                                      (optional, defaults to true)
            label (string)          : label for this CheckBox.
                                      (optional, defaults to None)
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the CheckBox, or None

        """
        result = None
        # create widget
        widget = None
        if label is None:
            widget = QtWidgets.QCheckBox()
        else:
            widget = QtWidgets.QCheckBox(label)

        if value == True:
            widget.setCheckState(QtCore.Qt.Checked)
        else:
            widget.setCheckState(QtCore.Qt.Unchecked)
        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def insertWidget(self, widget, widget_id='inserted-widget'):
        """Inserts an already existing QWidget into the Dialog.

        """
        if not isinstance(widget, QtWidgets.QWidget):
            raise AttributeError('Not a QWidget: {}'.widget)

        if isinstance(widget, Dialog):
            widget.is_child_widget = True
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def addWidget(self,
                  widget_id='widget',
                  **kwargs):
        """Adds an empty widget.

        Args:
            widget_id (string)      : unique id for this widget

        Returns:
            QWidget, or None

        """
        result = None
        # create widget
        widget = QtWidgets.QWidget()
        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        return widget

    # -------------------------------------------------------------------------
    def addButton(self,
                  widget_id='button',
                  label='clickMe...',
                  color=None,
                  color_disabled=None,
                  icon_path=None,
                  **kwargs):
        """Adds a Button.

        Args:
            widget_id (string)      : unique id for this widget
            label (string)          : label for this CheckBox.
                                      (optional, defaults to None)
            color (string)          : hex color in the format '#ff00ff'
                                      (optional, defaults to None)
            color_disable (string)  : hex color in the format '#ff00ff'
                                      (optional, defaults to None)
            kwargs (keyword args)   : optional kwargs processed by _processKwargs()

        Returns:
            QWidget representing the Button, or None

        """
        result = None
        # create widget
        widget = QtWidgets.QPushButton(text=label)

        # deal with color
        if color is not None:
            if color_disabled is None:
                color_disabled = '#505050'
            stylesheet = 'QPushButton {background-color:%s;}'\
                         ' QPushButton:disabled {background-color:%s;}' \
                         % (color, color_disabled)
            widget.setStyleSheet(stylesheet)

        if icon_path is not None:
            icon_path = self.conformPath(icon_path)
            if os.path.exists(icon_path):
                icon = QtGui.QIcon()
                pixmap = QtGui.QPixmap(icon_path)
                icon.addPixmap(pixmap)
                widget.setIcon(icon)
                widget.setIconSize(pixmap.size())


        self._processKwargs(widget, kwargs)

        # store widget
        widget_id = self._storeWidget(widget, widget_id)
        widget.setFocusPolicy(QtCore.Qt.TabFocus)

        return widget

    # -------------------------------------------------------------------------
    def _loadCoreCss(self):
        """
        """
        cur_dir = os.getcwd()
        main_ressources_path = self.conformPath(os.path.dirname(__file__))
        main_ressources_path = '%s/ressources' % main_ressources_path
        os.chdir(os.path.dirname(main_ressources_path))

        style_sheet = ''
        css_names = ['main.css', '%s.css' % self.context]
        css_data = []
        for name in css_names:
            css_path = '%s/%s' % (main_ressources_path, name)
            if os.path.exists(css_path):
                refpath = os.path.dirname(main_ressources_path).replace('\\', '/')
                css_data.append(self._loadCss(css_path, refpath=refpath))

        # load core fonts
        for item in os.listdir(main_ressources_path):
            path = '%s/%s' % (main_ressources_path, item)
            if item.lower().endswith('ttf') or item.lower().endswith('otf'):
                if os.path.isfile(path):
                    loaded = self._loadFont(path)

        os.chdir(cur_dir)
        Dialog._core_css = '\n'.join(css_data)

    # -------------------------------------------------------------------------
    def _loadCss(self, filepath, refpath):
        """
        """
        css = ''

        with open(filepath, 'r') as css:
            data = css.read()
            css = self._makePathsAbsoluteInCss(data, refpath)

        return css

    # -------------------------------------------------------------------------
    def _loadFont(self, file_path):
        """
        """
        filename = os.path.basename(file_path).lower()
        if not filename in self.loaded_fonts:
            self.loaded_fonts.append(filename)
            self.font_db.addApplicationFont(file_path)
            return True
        return False

    # -------------------------------------------------------------------------
    @property
    def loaded_fonts(self):
        return Dialog._loaded_fonts

    # -------------------------------------------------------------------------
    @property
    def font_db(self):
        if Dialog._font_db is None:
            Dialog._font_db = QtGui.QFontDatabase()
        return Dialog._font_db

    # -------------------------------------------------------------------------
    @property
    def css(self):
        return self._css

    # -------------------------------------------------------------------------
    @property
    def core_css(self):
        if Dialog._core_css is None:
            self._loadCoreCss()

        return Dialog._core_css

    # -------------------------------------------------------------------------
    def loadFontsAndCss(self):
        """Tries to load custom Fonts and CSS for this dialog.

        """
        css_data = []
        # lazy-load core css and fonts
        css_data.append(self.core_css)

        # append user css and load user fonts
        if self.source_dir is not None:
            for item in os.listdir(self.source_dir):
                path = '%s/%s' % (self.source_dir, item)
                # deal with font
                if item.lower().endswith('ttf') or item.lower().endswith('otf'):
                    if os.path.isfile(path):
                        self._loadFont(path)
                # deal with css
                elif item.lower() == '%s.css' % self.source_filename.lower():
                    if os.path.exists(path):
                        css_data.append(self._loadCss(path, refpath=self.source_dir))

        self._css = '\n'.join(css_data)
        self.setStyleSheet(self.css)


    # -------------------------------------------------------------------------
    @classmethod
    def _resolveContext(cls):
        """
        """
        # dictionary mapping sub-contexts to contexts
        CONTEXT_HASH = {
            'mayabatch'   : 'maya',
            'mayapy'      : 'maya',
            'xsibatch'    : 'xsi',
            'pythonw'     : 'python',
            'houdinicore' : 'houdini',
            'houdinifx'   : 'houdini',
            'hython'      : 'houdini',
            'cinema_4d'   : 'cinema4d',
            'nuke'        : 'nuke'
        }

        context = os.path.basename(sys.executable)
        context = cls._conformName(context)
        context = context.replace('.exe', '')
        if context in CONTEXT_HASH:
            context = CONTEXT_HASH[context]
        else:
            if context.startswith('nuke'):
                context = 'nuke'
                with Guard():
                    import nuke
                    if nuke.env['studio']:
                        context = 'nukestudio'

        Dialog._context = context

    # -------------------------------------------------------------------------
    @classmethod
    def _makePathsAbsoluteInCss(cls, data, ref_path):
        """Patch Css code with the correct absolute paths on the fly.
        """
        stored_wd = os.getcwd()
        os.chdir(ref_path)

        lines = data.split('\n')
        for i in range(len(lines)):
            lines[i] = cls._makePathsAbsolute(lines[i])

        os.chdir(stored_wd)
        return '\n'.join(lines)

    # -------------------------------------------------------------------------
    @classmethod
    def _makePathsAbsolute(cls, line):
        """Convert css path to absolute path.

        Args:
            line(string)    : path to make absolute

        Returns:
            (string)        : absolute path
        """
        tokens = line.split('url(')
        if len(tokens) > 1:
            head = '%surl(' % tokens[0]
            subtokens = tokens[1].split(')')
            if len(subtokens) > 1:

                path = subtokens[0]
                path = os.path.abspath(path)
                path = os.path.expandvars(path)
                path = path.replace('\\', '/')

                subtokens.pop(0)
                tail = ')%s' % ')'.join(subtokens)

                line = '%s%s%s' % (head, path, tail)
        return line

    # -------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """Override keyPressEvent to keep focus on QWidget in Maya.

        """
        if (event.modifiers() & QtCore.Qt.ShiftModifier):
            self.shift = True
            pass # make silent
        elif event.key() == QtCore.Qt.Key_Escape and self.disable_return_escape:
            pass
        elif event.key() == QtCore.Qt.Key_Return and self.disable_return_escape:
            pass
        else:
            super(Dialog, self).keyPressEvent(event)

    # -------------------------------------------------------------------------
    def close(self, deleteLater=False):
        """Closes the open Dialog.

        """
        self.__ui_built = False
        # always clean up for non-modal dialog
        if deleteLater == True or self.last_view_modal == False:
            self.deleteLater()
        super(Dialog, self).close()

    # -------------------------------------------------------------------------
    def clear(self):
        """Clears all previous layout work and created widgets.

        """
        for i in reversed(range(self._layout_main.count())):
            self._layout_main.takeAt(i)
        for item in self._widgets:
            widget = self._widgets[item]
            widget.setParent(None)
            widget.deleteLater()

        self._widgets = {}
        self._openStructures = []
        self._focussed_widget = None
        self._btn_modal_cancel = None
        self._btn_modal_ok = None
        self.__created = False

    # -------------------------------------------------------------------------
    @classmethod
    def redraw(cls):
        """Forces Dialog redraw.
        """
        QtCore.QCoreApplication.processEvents()

    # -------------------------------------------------------------------------
    def rebuild(self, modal=False, **kwargs):
        """
        """
        modal = self.last_view_modal
        self._create(rebuild=True, modal=modal, **kwargs)

    # -------------------------------------------------------------------------
    def show(self):
        """Displays the dialog non-modally.

        """
        self._create(modal=False)
        if not self.is_child_widget:
            self.dialogOpen.emit()

        super(Dialog, self).show()

        if self.test_mode:
            QtCore.QTimer.singleShot(self.__test_display_length, self.close)

        self.redraw()

    # -------------------------------------------------------------------------
    def getWidget(self, widget_id):
        """Locates and returns widget by its widget_id.

        Args:
            widget_id (string) : unique ID of the target widget

        Returns:
            widget or None     : located widget or None

        """
        widget = None

        widget_id = self._conformName(widget_id)

        if widget_id in self._widgets.keys():
            widget = self._widgets[widget_id]
        else:

            logger.error('Failed to locate this widget: %s' % widget_id)
        return widget

    # -------------------------------------------------------------------------
    def getWidgetDetails(self, widget, print_details=True):
        """Prints id, type and available signals for this widget.
        Args:
            widget (QWidget)     : QWidget to to print details for
            print_details (bool) : if True prints out details

        Returns:
            (dict)               : dictionary holding id, type and signals

        """
        details = {}
        details['id'] = self.getWidgetId(widget)
        details['type'] = widget.__class__.__name__

        signals = self._get_supported_signals(widget)
        signal_names = [signal[0] for signal in signals]
        details['signals'] = signal_names

        if print_details is True:
            output = []
            output.append('='*80)
            output.append('Widget ID:    %s' % details['id'])
            output.append('Widget Type:  %s' % details['type'])
            output.append('')
            output.append('available Signals:')
            output.append('')
            for signal in details['signals']:
                output.append('    %s' % signal)
            output.append('')
            output.append('='*80)
            logger.info('\n'.join(output))

        return details

    # -------------------------------------------------------------------------
    def getWidgetId(self, widget):
        """Locates and returns the widget_id for this widget.

        Args:
            widget (QWidget)  : QWidget to locate the ID for

        Returns:
            (string, or None) : located widget_id, or None

        """
        for key in self._widgets.keys():
            if self._widgets[key] == widget:
                return key

        logger.error('Failed to locate this widget: %s' % widget)
        return None


    # -------------------------------------------------------------------------
    def setModalOk(self, button):
        """Sets button to be the Modal OK button for this dialog.

        """
        if isinstance(button, QtWidgets.QPushButton):
            self._btn_modal_ok = button

    # -------------------------------------------------------------------------
    def setModalCancel(self, button):
        """Sets button to be the Modal Cancel button for this dialog.

        """
        if isinstance(button, QtWidgets.QPushButton):
            self._btn_modal_cancel = button

    # -------------------------------------------------------------------------
    def showModal(self):
        """Displays the dialog modally.

        """

        if self.is_child_widget:
            raise AttributeError("Can't be shown modally, is being used as a child widget")

        self._create(modal=True)
        self.dialogOpen.emit()
        self.modal_return_value = False

        if self.test_mode:
            btn = None
            if self.test_mode == 'ok':
                btn = self._btn_modal_ok
            else:
                btn = self._btn_modal_cancel

            if btn is not None:
                t = QtCore.QTimer(None)
                t.setSingleShot(True)
                t.timeout.connect(btn.animateClick)
                t.start(self.__test_display_length)

        self.exec_()

        return self.modal_return_value


    # -------------------------------------------------------------------------
    def _closeStructure(self):
        """Closes the current open layout structure.

        """
        structure = self._popLastOpenStructure()

        if structure == (None, None):
            return False

        widget = structure[0]
        layout = structure[1]

        # deal with special case 'ScrollArea'
        if isinstance(widget, QtWidgets.QScrollArea):
            inner_widget = widget.takeWidget()
            inner_widget.setLayout(layout)
            widget.setWidget(inner_widget)
            self._getActiveLayout().addWidget(widget)

        # deal with special case 'tab'
        elif widget.__class__.__name__ != 'QTabWidget':
            widget.setLayout(layout)
            self._getActiveLayout().addWidget(widget)

        return True

    # -------------------------------------------------------------------------
    def _popLastOpenStructure(self):
        """Removes and returns the last open structure.

        """
        if len(self._openStructures) == 0:
            return (None, None)

        return self._openStructures.pop()

    # -------------------------------------------------------------------------
    def _addOpenStructure(self, widget, layout):
        """Stores the open structure.
        """
        self._openStructures.append((widget, layout))

    # -------------------------------------------------------------------------
    def _isActiveStructureHorizontal(self):
        """Returns True, if the current active Structure is aligned
        horizontally.
        """
        if len(self._openStructures) == 0:
            return False
        else:

            layout =  self._openStructures[-1][1]
            if layout.direction() == QtWidgets.QBoxLayout.Direction.LeftToRight:
                return True
            else:
                return False

    # -------------------------------------------------------------------------
    @classmethod
    def _get_supported_signals(cls, widget):
        """Returns a list of supported signals for widget.

        """
        signals = []

        cls_name = widget if isinstance(widget, type) else type(widget)
        signal = type(QtCore.Signal())

        for name in dir(widget):
            attr = None
            with Guard():
                attr = getattr(cls_name, name)

            if attr is not None:
                if isinstance(attr, signal):
                    new_item = [name, getattr(cls_name, name)]
                    signals.append(new_item)

        return signals

    # -------------------------------------------------------------------------
    def _connectSignalsToSlots(self, widget, widget_id):
        """Connects supported signals to implemented slots.

        Expects implementation based on this naming:
            slot_<widget_id>_<signal>

        So for the signal 'released' and the widget_id 'my_button' you need to
        implement:

            def slot_my_button_released(self):
                pass


        Also slots for a specific context are supported:

            slot<Context>_<widget_id>_<signal>

        So for the signal 'released', the context 'Maya' and the
        widget_id 'my_button' you need to implement:

            def slotMaya_my_button_released(self):
                pass

        The order of slot execution is:

            slot_*
            slot<Context>_*


        """
        # get list of suppported signals for this widget
        signals = self._get_supported_signals(widget)
        if widget_id != '':
            widget_id += '_'

        for item in signals:
            signal_name = item[0]
            signal = item[1]

            # construct slot method name for this signal and this context
            context = self.context
            context = context[0].upper() + context[1:]
            slot_name = 'slot' + context + '_' + widget_id + signal_name
            # is the corresponding slot method implemented?
            if hasattr(self, slot_name):
                slot = getattr(self, slot_name)
                # connect signal to slot
                widget_signal = getattr(widget, signal_name)
                if widget_signal is not None:
                    widget_signal.connect(slot)

            # construct slot method name for this signal
            slot_name = 'slot_' + widget_id + signal_name

            # is the corresponding slot method implemented?
            if hasattr(self, slot_name):
                slot = getattr(self, slot_name)
                # connect signal to slot
                widget_signal = getattr(widget, signal_name)
                if widget_signal is not None:
                    widget_signal.connect(slot)

            # construct global slot method name for this signal
            slot_name = 'slotGlobal_' + signal_name
            # is the corresponding slot method implemented?
            if hasattr(self, slot_name):
                slot = getattr(self, slot_name)
                # connect signal to slot
                widget_signal = getattr(widget, signal_name)
                if widget_signal is not None:
                    widget_signal.connect(slot)


    # -------------------------------------------------------------------------
    def _getActiveLayout(self):
        """Returns the current active Layout object.

        """
        if len(self._openStructures) == 0:
            return self._layout_main

        return self._openStructures[-1][1]

    # -------------------------------------------------------------------------
    def _createUniqueWidgetId(self, widget_id):
        """make sure that widget_id is a unique id.
        If not makes it unique by versioning it up.

        Args:
            widget_id (string) : widget_id to make unique

        Returns:
            (string)      : unique widget_id

        """
        # safety
        if widget_id is None or len(widget_id.strip()) == 0:
            widget_id = 'unnamed_widget'

        widget_id = self._conformName(widget_id)

        # check if this widget_id is already unique
        if widget_id not in self._widgets.keys():
            return widget_id

        # up-version the widget_id and try again
        while widget_id in self._widgets.keys():
            widget_id = self._versionUp(widget_id)

        return widget_id

    # -------------------------------------------------------------------------
    def _storeWidget(self, widget, widget_id, add_to_layout=True):
        """
        """
        # ensure or create a unique widget_id
        widget_id = self._createUniqueWidgetId(widget_id)
        self._widgets[widget_id] = widget

        # connect signals to slots
        self._connectSignalsToSlots(widget, widget_id)
        # add to active layout
        if add_to_layout:
            self._getActiveLayout().addWidget(widget)

        return widget_id

    # -------------------------------------------------------------------------
    def _setPropertiesFromKwargs(self, **kwargs):
        """Checks if kwargs contain supported properties and sets them.

        Args:
            kwargs: keyword arguments.

        """
        for cur_key in kwargs.keys():

            if cur_key == 'width':
                self.width = kwargs['width']

            elif cur_key == 'height':
                self.height = kwargs['height']

            elif cur_key == 'title':
                self.title = kwargs['title']

            elif cur_key == 'fixed_size':
                self.fixed_size = kwargs['fixed_size']


    # -------------------------------------------------------------------------
    def _constructLayout(self, modal=False, rebuild=False, **kwargs):
        """Constructs and initialises all widgets and layout structures.

        """
        # if rebuild is False:
        # add an empty invisible widget to catch the initial focus
        self._focus_catching_widget = QtWidgets.QWidget()
        self._getActiveLayout().addWidget(self._focus_catching_widget)

        # first call defineLayout() which might be implemented by the user
        self.defineLayout(**kwargs)

        # close all open structures
        self._closeAllOpenStructures()

        # trigger creation of any nested Dialog objects
        for item_id in self._widgets:
            item = self._widgets[item_id]
            if isinstance(item, Dialog):
                item._layout_main.setContentsMargins(0, 0, 0, 0)
                item._layout_main.setSpacing(0)

                item._create()

        # add one last stretch
        if self.add_last_stretch:
            self.addStretch()

        # deal with modal widgets
        if modal == True:
            self._addModalWidgets()

        if self.scrollable:
            scrollarea = QtWidgets.QScrollArea()
            scrollarea.setWidgetResizable(True)

            scroll_widget = QtWidgets.QWidget(scrollarea)
            scroll_widget.setLayout(self._layout_main)
            scrollarea.setWidget(scroll_widget)

            self._layout_scroll = QtWidgets.QVBoxLayout()
            self._layout_scroll.setContentsMargins(0, 0, 0, 0)
            self._layout_scroll.setSpacing(0)
            self._layout_scroll.addWidget(scrollarea)
            self.setLayout(self._layout_scroll)
        else:
            # finally register the assembled layout
            self.setLayout(self._layout_main)

        # deal with window activation and widget focus
        try:
            self.activateWindow()
        except Exception as e:
            logger.exception('Failed to activate and focus window')

        self.setFocus()
        self.__ui_built = True
        self.postConstructLayout()

    # -------------------------------------------------------------------------
    def setFocus(self, widget=None):
        """
        """
        if widget is None:
            widget = self._focussed_widget
        if widget is not None:
            self._focussed_widget = widget
            widget.setFocus(QtCore.Qt.TabFocusReason)

    # -------------------------------------------------------------------------
    def _addModalWidgets(self):
        """Adds a separate group with 'OK' and 'CANCEL' buttons to the layout.

        """
        if self._btn_modal_cancel != None and self._btn_modal_ok != None:
            return

        self.openGroup(frame=False)
        self.openRow()
        self.addStretch()
        if not self._btn_modal_ok:
            modal_ok = self.addButton('sehsucht_ui_modalok',
                                      label='Ok',
                                      width=100)
            self._btn_modal_ok = modal_ok #'sehsucht_ui_modalok'


        self.addSpacer(20)

        if not self._btn_modal_cancel:
            modal_cancel = self.addButton('sehsucht_ui_modalcancel',
                                          label='Cancel',
                                          width=100)
            self._btn_modal_cancel = modal_cancel # 'sehsucht_ui_modalcancel'

        self.addStretch()
        self.closeRow()
        self.closeGroup()

        # if there is no focussed widget defined, use OK
        if not self._focussed_widget:
            self._focussed_widget = self._btn_modal_ok

    # -------------------------------------------------------------------------
    def _closeAllOpenStructures(self):
        """Closes all open structures that might still be open.

        """
        status = self._closeStructure()

        while status == True:
            status = self._closeStructure()


    # -------------------------------------------------------------------------
    def _create(self, modal=False, rebuild=False, **kwargs):
        """Creates/initialises the Dialog.

        Makes sure that this gets called only once.

        Size, Title and layout get constructed here.

        """
        if rebuild is True:
            self.clear()

        # is the dialog already created?
        if self.created == True:
            # do we need to repopulate it?
            if modal != self.last_view_modal:
                # clear the layout
                self.clear()
            else:
                # stop here
                return

        if rebuild is False:
            self.setWindowTitle(self.__title)

            if self.fixed_size == True:
                self.setFixedSize(self.width, self.height)
            else:
                self.resize(self.width, self.height)

        self._constructLayout(modal=modal, rebuild=rebuild, **kwargs)

        # flag as 'created'
        self.__created = True
        self.__last_view_modal = modal

    # -------------------------------------------------------------------------
    def _processKwargs(self, widget, kwargs):
        """Tries to apply all known keyword arguments to widget.

        """
        self.__setKwarg(widget, kwargs, 'height', 'setFixedHeight')
        self.__setKwarg(widget, kwargs, 'width', 'setFixedWidth')

        self.__setKwarg(widget, kwargs, 'min_height', 'setMinimumHeight')
        self.__setKwarg(widget, kwargs, 'min_width', 'setMinimumWidth')

        self.__setKwarg(widget, kwargs, 'readonly', 'setReadOnly')
        self.__setKwarg(widget, kwargs, 'enabled', 'setEnabled')

        self.__setKwarg(widget, kwargs, 'labelclass', 'setProperty', ['labelClass'])

        self.__setKwarg(widget, kwargs, 'min', 'setMinimum')
        self.__setKwarg(widget, kwargs, 'max', 'setMaximum')

        self.__setKwarg(widget, kwargs, 'tooltip', 'setToolTip')

        self._dealWithCustomFont(widget, kwargs)

    # -------------------------------------------------------------------------
    def __setKwarg(self, widget, kwargs, key, method, args=[]):
        """
        """
        if key in kwargs:
            value = kwargs[key]
            if hasattr(widget, method):
                call_me = getattr(widget, method)
                combined_args = list(args)
                combined_args.append(value)
                call_me(*combined_args)

    # -------------------------------------------------------------------------
    def _dealWithCustomFont(self, widget, kwargs):
        """
        """
        with Guard():
            font = 'MS Sans Serif'
            if 'font' in kwargs:
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
    def _storeWorkingDirAndFile(self):
        """
        """
        with Guard():
            filename = sys.modules[self.__class__.__module__].__file__
            self.__source_filename = self.conformPath(os.path.basename(filename))
            self.__source_filename = self.__source_filename.replace('.pyc', '').replace('.py', '')
            self.__source_dir = self.conformPath(os.path.abspath(os.path.dirname(filename)))

    # -------------------------------------------------------------------------
    @classmethod
    def _versionUp(cls, name):
        """
        """
        tokens = name.split('_')
        # if name is not already versioned, then we're done
        if len(tokens) == 1:
            name += '_1'
            return name

        netto_name = '_'.join(tokens[:-1])
        number = tokens[-1]
        try:
            number = int(number)
            number += 1
        except Exception as e:
            name += '_1'
            return name

        name = netto_name + '_' + str(number)

        return name

    # -------------------------------------------------------------------------
    @classmethod
    def _conformName(cls, name):
        """
        """
        result = name.strip()
        try: # pragma: no cover_3
            result = unicode(result)
        except NameError: # pragma: no cover_2
            pass

        umlaut_hash = {
            u'ä' : u'a',
            u'ö' : u'o',
            u'ü' : u'u',
            u'Ä' : u'A',
            u'Ö' : u'O',
            u'Ü' : u'U',
        }
        for umlaut in umlaut_hash:
            result = result.replace(umlaut, umlaut_hash[umlaut])

        result = result.encode('ascii', 'ignore').decode('utf-8')
        result = result.replace(' ', '_')
        result = str(result).lower()

        return result

    # -------------------------------------------------------------------------
    def slot_sehsucht_ui_modalok_released(self):
        """Slot implementation for default modal OK button.

        """
        self.modal_return_value = True
        self.close()

    # -------------------------------------------------------------------------
    def slot_sehsucht_ui_modalcancel_released(self):
        """Slot implementation for default modal Cancel button.

        """
        self.modal_return_value = False
        self.close()

    # -------------------------------------------------------------------------
    def msgBox(self,
               title='title',
               message='message',
               ok_label='Ok',
               cancel_label='Cancel',
               **kwargs):
        """Creates and displays a MsgBox that is a child dialog of self.

        """
        return msgBox(title=title,
                      message=message,
                      ok_label=ok_label,
                      cancel_label=cancel_label,
                      parent=self,
                      **kwargs)

    # -------------------------------------------------------------------------
    @classmethod
    def processEvents(cls):
        """Runs our QApplication in exec mode, processing the QEventLoop.

        Will block until all QDialogs are not in use anymore.
        Has no effect and returns immmediately if:
            - we don't use our own QApplication object.
            - not at least one Dialog is in use ( Dialog.count > 0 )

        """
        if cls.app is not None:
            cls.app.exec_()

# ------------------------------------------------------------------------------
def deleteDialog(dialog):
    """
    """
    if isinstance(dialog, QtWidgets.QWidget):
        dialog.setParent(None)
        del dialog

# ------------------------------------------------------------------------------
def createDialog(targetclass=None, parent=None, **kwargs):
    """Creates a Dialog object in the current context.

    Args:
        targetclass (class or None) : target class to use.
                                      (optional, defaults to None)
        parent                      : parent application/dialog
                                      (optional, defaults to None)
        kwargs                      : optional keyword arguments to pass on

    Returns:
        Dialog object, or None

    """
    # try to use targetclass, fall back to Dialog
    resolvedclass = Dialog
    if targetclass is not None:
        if issubclass(targetclass, Dialog):
            resolvedclass = targetclass


    # get context
    Dialog._resolveContext()
    context = Dialog._context

    dialog = None

    if parent is None:

        if context == 'maya':
            parent = maya_main_window
            # for widget in QtWidgets.QApplication.topLevelWidgets():
            #     name = widget.objectName()
            #     if name == 'MayaWindow':
            #         parent = widget
            #         break

        elif context.startswith('nuke'):
            parent = QtWidgets.QApplication.activeWindow()

        elif context.startswith('houdini'):
            import hou
            parent = hou.qt.mainWindow()

        # create our own QAppliction for all other cases
        # (right now these are Python and Cinema4D)
        else:
            if Dialog.app is None:
                Dialog.app = QtWidgets.QApplication(sys.argv)
            # set icon
            icon = os.path.dirname(__file__).replace('\\', '/') + '/ressources/logo.png'
            if os.path.exists(icon):
                Dialog.app.setWindowIcon(QtGui.QIcon(icon))

    # create the dialog object
    dialog = resolvedclass(parent=parent, **kwargs)

    return dialog

# -----------------------------------------------------------------------------
class ListRow(Dialog):
    """
    """
    is_list_row = True

    # -------------------------------------------------------------------------
    def initialize(self, value=None, index=0, **kwargs):
        """
        """
        self.kwargs = kwargs
        self.value = value
        # decoding needed in Python 2.x
        try:
            self.value = self.value.decode('utf-8')
        except AttributeError:
            pass

        self.index = index
        self.keywords = []
        if 'keywords' in kwargs:
            self.keywords = kwargs['keywords']
        self.is_child_widget = True
        self.add_last_stretch = False
        self._layout_main.setContentsMargins(0, 0, 0, 0)
        self._layout_main.setSpacing(0)

    # -------------------------------------------------------------------------
    @property
    def listbox(self):
        return self.parent().parent().parent().parent()
    # -------------------------------------------------------------------------
    @property
    def listrow(self):
        listbox = self.listbox
        for i in range(self.listbox.count()):
            row = self.listbox.item(i)
            if row.value == self:
                return row
    # -------------------------------------------------------------------------
    @property
    def filter_keywords(self):
        return u'{} {}'.format(self.value.lower(), ' '.join(self.keywords).lower())

    # -------------------------------------------------------------------------
    def defineLeftLayout(self):
        pass
    # -------------------------------------------------------------------------
    def defineRightLayout(self):
        pass


    # -------------------------------------------------------------------------
    def defineLayout(self):
        """
        """
        self.openRow()

        self.defineLeftLayout()
        self.label = self.addLabel(**self.kwargs)
        if self.value is not None:
            self.label.setText(self.value)
        self.defineRightLayout()

    # -------------------------------------------------------------------------
    def build(self, add_stretch=False, **kwargs):
        """
        """
        # if add_stretch:
        #     self.addStretch()
        self.closeRow()

        self._create()

    # -------------------------------------------------------------------------
    def update(self):
        """
        """
        self.label.setText(self.value)


# -----------------------------------------------------------------------------
class MsgBox(Dialog):
    """Creates a Messagebox with the provided title, message and button labels.

    """

    # -------------------------------------------------------------------------
    def initialize(self,
                   **kwargs):
        """
        """

        self.setWidthHeight(300, 100)

        self.title = 'MsgBox'
        if 'title' in kwargs:
            self.title = kwargs['title']
        self.title = self.title

        self.message = '...'
        if 'message' in kwargs:
            self.message = kwargs['message']

        self.ok_label = 'Ok'
        if 'ok_label' in kwargs:
            self.ok_label = kwargs['ok_label']

        self.cancel_label = 'Cancel'
        if 'cancel_label' in kwargs:
            self.cancel_label = kwargs['cancel_label']

        self.icon = None
        if 'mode' in kwargs:
            if kwargs['mode'] == 'warning':
                self.icon = './ressources/warning.png'

    # -------------------------------------------------------------------------
    def defineLayout(self):
        """
        """
        self.addStretch()
        self.addSpacer(10)
        self.openColumn()

        self.openRow()

        if self.icon is not None:
            self.addSpacer(10)
            self.addImage(self.icon)
            self.addSpacer(20)
        else:
            self.addStretch()
            self.addSpacer(20)

        self.addLabel(label=self.message)
        self.addSpacer(20)
        self.addStretch()
        self.closeRow()
        self.addSpacer(40)
        self.openRow()
        self.btn_ok = self.addButton(widget_id='sehsucht_ui_modalok',
                                  label=self.ok_label,
                                  width=130)
        self.setModalOk(self.btn_ok)

        if self.cancel_label is not None:
            self.addSpacer(30)
            self.btn_cancel = self.addButton(widget_id='sehsucht_ui_modalcancel',
                                      label=self.cancel_label,
                                      width=130)
            self.setModalCancel(self.btn_cancel)
        else:
            self.setModalCancel(self.btn_ok)

        self.closeRow()

        self.closeColumn()
        self.addSpacer(10)
        self.addStretch()


# -----------------------------------------------------------------------------
def msgBox(parent=None,
           title='title',
           message='message',
           ok_label='Ok',
           cancel_label='Cancel',
           **kwargs):
    """Creates a Messagebox with the provided title, message and button labels.

    Args:
        title (string)          : title of the MessageBox
        message (string)        : the actual message text
        ok_label (string)       : label of the OK button
        cancel_label (string)   : label of the Cancel button.
                                  If value is None, then only the OK button
                                  will be shown.
        kwargs                  : optional keyword arguments to pass on

    Returns:
        (bool)                  : True for OK, False for Cancel

    """
    kwargs['title'] = title
    kwargs['message'] = message
    kwargs['ok_label'] = ok_label
    kwargs['cancel_label'] = cancel_label

    msgbox = createDialog(parent=parent,
                          targetclass=MsgBox,
                          **kwargs)

    status = msgbox.showModal()
    deleteDialog(msgbox)

    return status


# -----------------------------------------------------------------------------
class ClickableLabel(QtWidgets.QLabel):
    """
    """
    labelClicked = QtCore.Signal()

    def mousePressEvent(self, event):
        self.labelClicked.emit()


# -----------------------------------------------------------------------------
class QTextEdit(QtWidgets.QTextEdit):
    """
    """

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(QTextEdit, self).__init__(*args, **kwargs)
        self._placeholderText = ''
        self._placeholderVisible = False
        self.textChanged.connect(self.placeholderVisible)

    # -------------------------------------------------------------------------
    def placeholderVisible(self):
        """Return if the placeholder text is visible,
        and force update if required.

        """
        placeholderCurrentlyVisible = self._placeholderVisible
        self._placeholderVisible = self._placeholderText and self.document().isEmpty() and not self.hasFocus()
        if self._placeholderVisible != placeholderCurrentlyVisible:
            self.viewport().update()
        return self._placeholderVisible

    # -------------------------------------------------------------------------
    def placeholderText(self):
        """Return text used as a placeholder.

        """
        return self._placeholderText

    # -------------------------------------------------------------------------
    def setPlaceholderText(self, text):
        """Set text to use as a placeholder.

        """
        self._placeholderText = text
        if self.document().isEmpty():
            self.viewport().update()

    # -------------------------------------------------------------------------
    def paintEvent(self, event):
        """Override the paint event to add the placeholder text.

        """
        if self.placeholderVisible():
            painter = QtGui.QPainter(self.viewport())
            colour = self.palette().text().color()
            colour.setAlpha(128)
            painter.setPen(colour)
            painter.setClipRect(self.rect())
            margin = self.document().documentMargin()
            textRect = self.viewport().rect().adjusted(margin, margin, 0, 0)
            painter.drawText(textRect, QtCore.Qt.AlignTop | QtCore.Qt.TextWordWrap, self.placeholderText())
        super(QTextEdit, self).paintEvent(event)



class WrappedRowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1, **kwargs):
        super(WrappedRowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(0, 0, 0, 0)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def addSpacing(self, dim):
        spacer = QtWidgets.QWidget()
        spacer.setFixedWidth(dim)
        self.addWidget(spacer)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def direction(self):
        return QtWidgets.QBoxLayout.LeftToRight

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(WrappedRowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()

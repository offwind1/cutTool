from PyQt5.QtWidgets import *


class BaseField():

    def __init__(self, parent, tag, *args, **kw):
        self.parent = parent
        self.tag = tag

        self.initialize()
        self.setStyle()
        self.setConfig()
        self.setLayouts()

    def initialize(self):
        pass

    def setStyle(self):
        pass

    def setConfig(self):
        pass

    def setLayouts(self):
        pass


class ButtonSpinBoxField(BaseField):
    default = 1
    limit = 99999

    def __init__(self, parent, tag, func, *arg, **kw):
        if kw:
            self.default = kw.get("default", self.default)
            self.limit = kw.get("limit", self.limit)

        super().__init__(parent, tag)

        self.button.clicked.connect(func)

    def initialize(self):
        self.button = QPushButton(self.tag, self.parent)
        self.spinbox = QSpinBox(self.parent)

    def setStyle(self):
        self.spinbox.setMinimum(self.default)
        self.spinbox.setMaximum(self.limit)

    def setConfig(self):
        pass

    def setLayouts(self):
        self.parent.from_layout.addRow(self.button, self.spinbox)

    def action(self):
        pass

    def value(self):
        return self.spinbox.value()

    def setValue(self, value):
        return self.spinbox.setValue(value)

    def setDisabled(self, flag):
        self.button.setDisabled(flag)

    def updateButtonText(self, text):
        self.button.setText(text)


class LineSpinBoxField(BaseField):
    default = 2
    limit = 99999

    def __init__(self, *arg, **kw):
        if kw:
            self.default = kw.get("default", self.default)
            self.limit = kw.get("limit", self.limit)

        super().__init__(*arg, **kw)

    def initialize(self):
        self.label = QLabel(self.tag, self.parent)
        self.spinbox = QSpinBox(self.parent)

    def setStyle(self):
        self.spinbox.setMinimum(self.default)
        self.spinbox.setMaximum(self.limit)

    def setConfig(self):
        # self.button.clicked.connect(self.action)
        pass

    def setLayouts(self):
        self.parent.from_layout.addRow(self.label, self.spinbox)

    def action(self):
        pass

    def value(self):
        return self.spinbox.value()


class TextEditField(BaseField):
    def initialize(self):
        self.label = QLabel(self.tag, self.parent)
        self.edit = QLineEdit(self.parent)

    def setStyle(self):
        # self.edit.setReadOnly(True)
        pass

    def setConfig(self):
        pass
        # self.button.clicked.connect(self.action)

    def setLayouts(self):
        self.parent.from_layout.addRow(self.label, self.edit)

    def action(self):
        pass

    def text(self):
        return self.edit.text()

    def setText(self, text):
        self.edit.setText(text)

class LineEditField(BaseField):

    def initialize(self):
        self.button = QPushButton(self.tag, self.parent)
        self.edit = QLineEdit(self.parent)

    def setStyle(self):
        self.edit.setReadOnly(True)

    def setConfig(self):
        self.button.clicked.connect(self.action)

    def setLayouts(self):
        self.parent.from_layout.addRow(self.button, self.edit)

    def action(self):
        pass

    def text(self):
        return self.edit.text()


class PathField(LineEditField):
    '''选择路径'''

    def action(self, *args):
        filename = QFileDialog.getExistingDirectory(self.parent, "选择路径",
                                                    "", QFileDialog.ShowDirsOnly)
        if filename: self.edit.setText(filename)


class FileField(LineEditField):
    '''选择文件'''

    def action(self, *args):
        filepath, filename = QFileDialog.getOpenFileName(self.parent, "选取文件",
                                                         "", "Text Files (*.py;*.json;*.yml)")
        if filepath: self.edit.setText(filepath)


class VoteField(LineSpinBoxField):
    def action(self, *args):
        filepath, filename = QFileDialog.getOpenFileName(self.parent, "选取文件",
                                                         "", "Text Files (*.py;*.json)")
        if filepath: self.edit.setText(filepath)

    def setStyle(self):
        pass


class CheckList(QWidget):

    def __init__(self, list, class_=QCheckBox):
        super().__init__()

        self.check_list = []
        for tag in list:
            self.check_list.append(class_(tag))

        self.initialize()
        self.setConfig()
        self.setLayouts()

    def initialize(self):
        pass

    def setConfig(self):
        pass

    def setLayouts(self):
        layout = QGridLayout()
        for i, widget in enumerate(self.check_list):
            layout.addWidget(widget, i // 2, i % 2)
        self.setLayout(layout)

    def value(self):
        list = []
        for widget in self.check_list:
            list.append(widget.isChecked())

        return list

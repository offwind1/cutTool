from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class BaseWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initialize()
        self.setLayouts()

        self.setField()
        self.setWidget()

    def initialize(self):
        self.layout = QVBoxLayout()
        self.from_layout = QFormLayout()

    def setLayouts(self):
        self.layout.addLayout(self.from_layout)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def setField(self):
        pass

    def setWidget(self):
        pass

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)

    def show_message(self, text):
        QMessageBox.about(self, "提示", text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("割图工具")
        self.tool_bar = QToolBar()
        self.main_widget = QStackedWidget()

        self.setLayouts()

    def setLayouts(self):
        self.tool_bar.setIconSize(QSize(32, 32))
        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.main_widget)

    def changeView(self, view):
        self.main_widget.removeWidget(self.main_widget.currentWidget())
        self.main_widget.addWidget(view)

    def addWindow(self, window, tag):
        action = QAction(tag, self)
        action.triggered.connect(lambda x, v=window: self.changeView(v))
        self.tool_bar.addAction(action)

    def addSeparator(self):
        self.tool_bar.addSeparator()
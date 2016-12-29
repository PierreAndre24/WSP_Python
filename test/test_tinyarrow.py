from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QSplitter, QTextEdit, QHBoxLayout,
                            QVBoxLayout, QToolButton, QApplication, QLabel)


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.splitter = QSplitter( QtCore.Qt.Vertical, self)

        self.splitter.addWidget(QTextEdit(self))
        self.splitter.addWidget(QTextEdit(self))

        layout = QHBoxLayout(self)
        layout.addWidget(self.splitter)
        handle = self.splitter.handle(1)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        button = QToolButton(handle)
        button.setArrowType(QtCore.Qt.UpArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(True,[0,1]))
        layout.addWidget(button)

        button = QToolButton(handle)
        button.setArrowType(QtCore.Qt.DownArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(False,[0,1]))
        layout.addWidget(button)

        handle.setLayout(layout)



    def handleSplitterButton(self, up=True, lines = [0,1]):
        if not all(self.splitter.sizes()):
            self.splitter.setSizes([1, 1, 1])
        elif up:
            self.splitter.setSizes([0, 1, 1])
        else:
            self.splitter.setSizes([1, 0, 1])
        # if not all(self.splitter.sizes()):
        #     self.splitter.setSizes([1, 1])
        # elif up:
        #     self.splitter.setSizes([0, 1])
        # else:
        #     self.splitter.setSizes([1, 0])

class originalWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.splitter = QSplitter(self)
        self.splitter.addWidget(QTextEdit(self))
        self.splitter.addWidget(QTextEdit(self))
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        handle = self.splitter.handle(1)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        button = QToolButton(handle)
        button.setArrowType(QtCore.Qt.LeftArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(True))
        layout.addWidget(button)
        button = QToolButton(handle)
        button.setArrowType(QtCore.Qt.RightArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(False))
        layout.addWidget(button)
        handle.setLayout(layout)

    def handleSplitterButton(self, left=True):
        if not all(self.splitter.sizes()):
            self.splitter.setSizes([1, 1])
        elif left:
            self.splitter.setSizes([0, 1])
        else:
            self.splitter.setSizes([1, 0])

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())

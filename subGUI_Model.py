from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QSplitter, QTextEdit, QHBoxLayout,
                            QVBoxLayout, QToolButton, QApplication, QLabel,
                            QScrollArea)


class Model(QWidget):
    def __init__(self, list_of_widgets):
        QWidget.__init__(self)
        self.splitter = QSplitter( QtCore.Qt.Vertical, self)

        for widget in list_of_widgets:
            scroll = QScrollArea()
            scroll.setWidget(widget)
            scroll.setWidgetResizable(True)
            self.splitter.addWidget(scroll)
        # scroll.setFixedHeight(400)
        # layout = QtGui.QVBoxLayout(self)
        # layout.addWidget(scroll)

        # self.splitter.addWidget(QTextEdit(self))
        # self.splitter.addWidget(QTextEdit(self))

        layout = QHBoxLayout(self)
        layout.addWidget(self.splitter)
        handle = self.splitter.handle(1)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        handle.setLayout(layout)



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

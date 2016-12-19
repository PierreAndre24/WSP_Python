from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QFormLayout,
                            QApplication, QScrollArea, QVBoxLayout, QHBoxLayout,
                            QTabWidget)
import sys

class Main(QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.addButton = QPushButton('button to add other widgets')
        self.addButton.clicked.connect(self.addWidget)

        # scroll area widget contents - layout
        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self):
        self.scrollLayout.addRow(Testtab())


class Testtab(QTabWidget):
    def __init__( self, parent=None):
        super(Testtab, self).__init__(parent)
        tabs = QTabWidget()
        tabs.resize(400, 250)
        # Create tabs
        tab1	= QWidget()
        tab2	= QWidget()
        tab3	= QWidget()

        # Set layout of first tab
        vBoxlayout	= QVBoxLayout()
        pushButton_close = QPushButton("Concatenate")
        pushButton_close.clicked.connect(self.closebutton)
        vBoxlayout.addWidget(pushButton_close)
        tab1.setLayout(vBoxlayout)

        # Add tabs
        tabs.addTab(tab1,"Files")
        tabs.addTab(tab2,"Basic Plots")
        tabs.addTab(tab3,"Advanced Plots")

        #tabs.show()

    def closebutton (self):
        tabs.removeTab(2)

class Test(QWidget):
    def __init__( self, parent=None):
        super(Test, self).__init__(parent)

        self.pushButton = QPushButton('I am in Test widget')
        self.pushButton.clicked.connect(self.closeTab)
        layout = QHBoxLayout()
        layout.addWidget(self.pushButton)
        self.setLayout(layout)



app = QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()

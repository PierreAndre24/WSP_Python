from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QTabWidget, QVBoxLayout)
import sys

def main_UI():

    app 	= QApplication(sys.argv)
    tabs	= QTabWidget()

    # Create tabs
    tab1	= QWidget()
    tab2	= QWidget()
    tab3	= QWidget()

    # Resize width and height
    tabs.resize(400, 250)

    # Set layout of first tab
    vBoxlayout	= QVBoxLayout()
    pushButton_Load = QPushButton("Load")
    pushButton_Save = QPushButton("Save")
    pushButton_SaveAs = QPushButton("Save As")
    pushButton_JoinLastDim = QPushButton("Join Last Dimension")
    pushButton_Concatenate = QPushButton("Concatenate")
    pushButton_Concatenate.clicked.connect(closebutton)
    vBoxlayout.addWidget(pushButton_Load)
    vBoxlayout.addWidget(pushButton_Save)
    vBoxlayout.addWidget(pushButton_SaveAs)
    vBoxlayout.addWidget(pushButton_JoinLastDim)
    vBoxlayout.addWidget(pushButton_Concatenate)
    tab1.setLayout(vBoxlayout)

    # Add tabs
    tabs.addTab(tab1,"Files")
    tabs.addTab(tab2,"Basic Plots")
    tabs.addTab(tab3,"Advanced Plots")

    # Set title and show
    tabs.setWindowTitle('PyQt QTabWidget @ pythonspot.com')
    tabs.show()

    sys.exit(app.exec_())

def closebutton():
    tab1.close()


if __name__ == '__main__':
    main_UI()

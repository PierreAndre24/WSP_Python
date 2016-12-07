from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

def main_UI():

    app 	= QtGui.QApplication(sys.argv)
    tabs	= QtGui.QTabWidget()

    # Create tabs
    tab1	= QtGui.QWidget()
    tab2	= QtGui.QWidget()
    tab3	= QtGui.QWidget()

    # Resize width and height
    tabs.resize(400, 250)

    # Set layout of first tab
    vBoxlayout	= QtGui.QVBoxLayout()
    pushButton_Load = QtGui.QPushButton("Load")
    pushButton_Save = QtGui.QPushButton("Save")
    pushButton_SaveAs = QtGui.QPushButton("Save As")
    pushButton_JoinLastDim = QtGui.QPushButton("Join Last Dimension")
    pushButton_Concatenate = QtGui.QPushButton("Concatenate")
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


if __name__ == '__main__':
    main_UI()

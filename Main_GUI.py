import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QFileDialog
#from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *

class App(QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.title = 'Workspace plotter'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')

        # status bar
        # self.statusBar = QStatusBar()
        # self.setStatusBar(self.statusBar)

        # file menu buttons

        # load a single file
        loadsingleButton = QAction(QIcon('exit24.png'), 'Load single file', self)
        loadsingleButton.setShortcut('Ctrl+O')
        loadsingleButton.setStatusTip('Load single file')
        loadsingleButton.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction(loadsingleButton)

        # load multiple files
        loadmultipleButton = QAction(QIcon('exit24.png'), 'Load multiple files', self)
        loadmultipleButton.setStatusTip('Load multiple files')
        loadmultipleButton.triggered.connect(self.openFileNamesDialog)
        fileMenu.addAction(loadmultipleButton)

        # import file
        importButton = QAction(QIcon('exit24.png'), 'Import file', self)
        importButton.setStatusTip('Import file')
        importButton.setShortcut('Ctrl+I')
        importButton.triggered.connect(self.importFileNameDialog)
        fileMenu.addAction(importButton)

        # system preferences
        preferencesButton = QAction(QIcon('exit24.png'), 'Preferences', self)
        preferencesButton.setStatusTip('System preferences')
        preferencesButton.setShortcut('Ctrl+,')
        preferencesButton.triggered.connect(self.preferences)
        fileMenu.addAction(preferencesButton)

        # exit
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def importFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def preferences(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

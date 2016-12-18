import sys, os, h5py
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QFileDialog, QInputDialog
#from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
import MultiDimExperiment, ExperimentFileManager

class App(QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.title = 'WSP Python'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

        self.FileInfo = {}
        self.openPreferences()
        self.XP = MultiDimExperiment.MultiDimExperiment()
        self.FM = ExperimentFileManager.ExperimentFileManager(self.XP)

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
        self.statusBar().showMessage('Ready')

        ####################
        # file menu buttons

        # load a file (or multiple_files)
        loadsingleButton = QAction(QIcon('exit24.png'), 'Load file', self)
        loadsingleButton.setShortcut('Ctrl+O')
        loadsingleButton.setStatusTip('Load single file')
        loadsingleButton.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction(loadsingleButton)

        # save a file
        savesingleButton = QAction(QIcon('exit24.png'), 'Save file', self)
        savesingleButton.setShortcut('Ctrl+S')
        savesingleButton.setStatusTip('Save file')
        savesingleButton.triggered.connect(self.saveFileNameDialog)
        fileMenu.addAction(savesingleButton)


        # convert a file or multiple files
        convertsingleButton = QAction(QIcon('exit24.png'), 'Convert files', self)
        convertsingleButton.setShortcut('Ctrl+C')
        convertsingleButton.setStatusTip('Convert files')
        convertsingleButton.triggered.connect(self.convertFilesDialog)
        fileMenu.addAction(convertsingleButton)
        fileMenu.addSeparator()

        # system preferences
        preferencesButton = QAction(QIcon('exit24.png'), 'Preferences', self)
        preferencesButton.setStatusTip('System preferences')
        preferencesButton.setShortcut('Ctrl+,')
        preferencesButton.triggered.connect(self.preferences)
        fileMenu.addAction(preferencesButton)
        fileMenu.addSeparator()

        # exit
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.closeApplication)
        fileMenu.addAction(exitButton)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.FileInfo['currentFilePath']):
            path = self.FileInfo['currentFilePath']
        else:
            path = ''
        filename, ok = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", path,"All Files (*);;Python Files (*.py)", options=options)
        if ok:
            if len(filename)>1:
                multiple_files = True
            else:
                multiple_files = False

            currentFilePath,currentFileName = os.path.split(filename[0])
            self.FileInfo['currentFilePath'] = currentFilePath
            self.FileInfo['currentFileName'] = currentFileName

            extension = self.FileInfo['currentFileName'].split('.')
            extension = extension[-1]
            self.XP = MultiDimExperiment.MultiDimExperiment()
            if extension == 'lvm':
                self.statusBar().showMessage('Opening ' + self.FileInfo['currentFileName'])
                self.FM.Read_Experiment_File(filepath = self.FileInfo['currentFilePath'],\
                                    filename = self.FileInfo['currentFileName'],\
                                    read_multiple_files = multiple_files)
            elif extension == 'h5':
                self.statusBar().showMessage('Opening ' + self.FileInfo['currentFileName'])
                self.FM.checkFile(self.FileInfo)
                if self.FileInfo['WSPPython']:
                    self.statusBar().showMessage('Opening ' + self.FileInfo['currentFileName'] + \
                        '. WSPPython file checked.')
                    item, ok = QInputDialog.getItem(self, "Select a group",\
                                "List of groups", self.FileInfo['AvailableGroups'], 0, False)
                    if ok:
                        self.FM.Read_Experiment_File(filepath = self.FileInfo['currentFilePath'],\
                                    filename = self.FileInfo['currentFileName'],\
                                    group_name = item)
            else:
                return
            self.statusBar().showMessage(self.FileInfo['currentFileName'] + ' loaded.')

    def saveFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.FileInfo['currentFilePath']):
            path = self.FileInfo['currentFilePath']
        else:
            path = ''
        filename, ok = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",path,"All Files (*);;Text Files (*.txt)", options=options)
        if ok:
            futureFilePath,futureFileName = os.path.split(filename)
            futureFileNameSplitted = futureFileName.split('.')
            if futureFileNameSplitted[-1] != 'h5':
                futureFileName = futureFileName + '.h5'
                self.statusBar().showMessage('File renamed to: ' + futureFileName)

            # ask for group name
            text, ok = QInputDialog.getText(self, 'Group name', 'Enter the group name:')
            if ok:
                self.FileInfo['currentGroupName'] = text

                self.statusBar().showMessage('Saving ' + futureFileName + '/' + self.FileInfo['currentGroupName'])
                self.FM.Write_Experiment_to_h5(filepath = futureFilePath,\
                                               filename = futureFileName, \
                                               group_name = self.FileInfo['currentGroupName'], \
                                               force_overwrite = True)
                self.FileInfo['currentFilePath'] = futureFilePath
                self.FileInfo['currentFileName'] = futureFileName
                self.statusBar().showMessage(futureFileName + '/' + self.FileInfo['currentGroupName']  + ' saved.')

    def convertFilesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.FileInfo['currentFilePath']):
            path = self.FileInfo['currentFilePath']
        else:
            path = ''
        filename, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", path,"All Files (*);;Python Files (*.py)", options=options)
        if filename:
            if len(filename)>1:
                multiple_files = True
            else:
                multiple_files = False

            currentFilePath,currentFileName = os.path.split(filename[0])
            self.FileInfo['currentFilePath'] = currentFilePath
            self.FileInfo['currentFileName'] = currentFileName

            if os.path.isdir(self.FileInfo['currentFilePath']):
                path = self.FileInfo['currentFilePath']
            else:
                path = ''
            filename, ok = QFileDialog.getSaveFileName(self,"Save file",path,"All Files (*);;Text Files (*.txt)", options=options)
            if ok:
                futureFilePath,futureFileName = os.path.split(filename)
                futureFileNameSplitted = futureFileName.split('.')
                if futureFileNameSplitted[-1] != 'h5':
                    futureFileName = futureFileName + '.h5'

                # ask for group name
                text, ok = QInputDialog.getText(self, 'Group name', 'Enter the group name:')
                if ok:
                    self.FileInfo['currentGroupName'] = text

                    self.statusBar().showMessage('Opening: ' + self.FileInfo['currentFileName'])
                    self.FM.Read_Experiment_File(filepath = self.FileInfo['currentFilePath'],\
                                            filename = self.FileInfo['currentFileName'],\
                                            read_multiple_files = multiple_files)
                    self.statusBar().showMessage('Saving ' + futureFileName)
                    self.FM.Write_Experiment_to_h5(filepath = futureFilePath,\
                                                   filename = futureFileName, \
                                                   group_name = self.FileInfo['currentGroupName'], \
                                                   force_overwrite = True)
                    self.statusBar().showMessage(futureFileName + ' saved.')
                    self.FileInfo['currentFilePath'] = futureFilePath
                    self.FileInfo['currentFileName'] = futureFileName

    def openPreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        # if not os.path.isdir(prefFile):
        #     path = self.FileInfo['currentFilePath']
        # Create the h5 file
        f = h5py.File(prefFile,'a')

        # Give the file version
        if 'currentFilePath' in f.attrs.keys():
            self.FileInfo['currentFilePath'] = f.attrs['currentFilePath']
        else:
            self.FileInfo['currentFilePath'] = ''
        f.close()

    def savePreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        # if not os.path.isdir(prefFile):
        #     path = self.FileInfo['currentFilePath']
        # Create the h5 file
        print prefFile
        f = h5py.File(prefFile,'a')
        print f
        # Give the file version
        f.attrs['currentFilePath'] = self.FileInfo['currentFilePath']
        f.close()


    def closeApplication(self):
        self.savePreferences()
        self.close()

    def preferences(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

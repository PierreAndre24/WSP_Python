import sys, os, h5py
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QAction, QFileDialog, QInputDialog, QFormLayout,
                            QScrollArea, QVBoxLayout, QTabWidget)
from GUI_Preferences import filePreferencesGUI
from PyQt5.QtGui import *
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
        self.initUserMenu()
        self.initUserTabs() # main QWidget
        self.setCentralWidget(self.tabs)
        self.show()

        self.WSPPreferences = {}
        self.filePreferences = {}
        self.loadPreferences()
        self.XP = MultiDimExperiment.MultiDimExperiment()
        self.FM = ExperimentFileManager.ExperimentFileManager(self.XP)

    ################################
    # Init interface
    def initUserMenu(self):
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
        saveasButton = QAction(QIcon('exit24.png'), 'Save file', self)
        saveasButton.setShortcut('Ctrl+S')
        saveasButton.setStatusTip('Save file')
        saveasButton.triggered.connect(self.saveAsFileNameDialog)
        fileMenu.addAction(saveasButton)


        # convert a file or multiple files
        convertsingleButton = QAction(QIcon('exit24.png'), 'Convert files', self)
        convertsingleButton.setShortcut('Ctrl+C')
        convertsingleButton.setStatusTip('Convert files')
        convertsingleButton.triggered.connect(self.convertFilesDialog)
        fileMenu.addAction(convertsingleButton)

        # File preferences
        filePreferencesButton = QAction(QIcon('exit24.png'), 'File preferences', self)
        filePreferencesButton.setShortcut('Ctrl+C')
        filePreferencesButton.setStatusTip('File preferences')
        filePreferencesButton.triggered.connect(self.filePreferencesDialog)
        fileMenu.addAction(filePreferencesButton)
        fileMenu.addSeparator()

        # system preferences
        preferencesButton = QAction(QIcon('exit24.png'), 'Preferences', self)
        preferencesButton.setStatusTip('System preferences')
        preferencesButton.setShortcut('Ctrl+,')
        preferencesButton.triggered.connect(self.WSPPreferences)
        fileMenu.addAction(preferencesButton)
        fileMenu.addSeparator()

        # exit
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.closeApplication)
        fileMenu.addAction(exitButton)

    def initUserTabs(self):
        self.tabs	= QTabWidget()

        # Create tabs
        self.create_TA_UItab() #Trace Analysis
        self.create_IPPM_UItab() #Isolated Position, Pulse Map
        self.create_IPSS_UItab() #Isolated Position, Single Spin

        # Add tabs
        self.tabs.addTab(self.TA_UItab,"Single trace analysis")
        self.tabs.addTab(self.IPPM_UItab,"Isol.Pos.: dI")
        self.tabs.addTab(self.IPSS_UItab,"Isol.Pos.: Single Spin")

        print self.tabs.count()


    ################################
    # Tab selection and tab layouts
    def selectUserTabs(self):
        for i in range(self.tabs.count()):
            self.tabs.removeTab(0)
        if self.filePreferences['ExperimentType'] == 'uspm':
            # Add tabs
            self.tabs.addTab(self.TA_UItab,"Single trace analysis")
            self.tabs.addTab(self.IPPM_UItab,"Isol.Pos.: dI")
        elif self.filePreferences['ExperimentType'] == 'ipss':
            # Add tabs
            self.tabs.addTab(self.TA_UItab,"Single trace analysis")
            self.tabs.addTab(self.IPPM_UItab,"Isol.Pos.: dI")
            self.tabs.addTab(self.IPSS_UItab,"Isol.Pos.: Single Spin")
        else:
            # Add tabs
            self.tabs.addTab(self.TA_UItab,"Single trace analysis")
            self.tabs.addTab(self.IPPM_UItab,"Isol.Pos.: dI")
            self.tabs.addTab(self.IPSS_UItab,"Isol.Pos.: Single Spin")

    def create_TA_UItab(self):
        self.TA_UItab = QWidget() # Single trace analysis tab

    def create_IPPM_UItab(self):
        self.IPPM_UItab = QWidget() #microsecond pulse map tab

    def create_IPSS_UItab(self):
        self.IPSS_UItab = QWidget() #microsecond pulse map tab


    ################################
    # Menu methods
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.WSPPreferences['currentFilePath']):
            path = self.WSPPreferences['currentFilePath']
        else:
            path = ''
        filename, ok = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", path,"All Files (*);;Python Files (*.py)", options=options)
        if ok:
            if len(filename)>1:
                multiple_files = True
            else:
                multiple_files = False

            currentFilePath,currentFileName = os.path.split(filename[0])
            self.WSPPreferences['currentFilePath'] = currentFilePath
            self.WSPPreferences['currentFileName'] = currentFileName[0]


            extension = self.WSPPreferences['currentFileName'].split('.')
            extension = extension[-1]
            self.XP = MultiDimExperiment.MultiDimExperiment()
            if extension == 'lvm':
                self.statusBar().showMessage('Opening ' + self.WSPPreferences['currentFileName'])
                # ask for group name
                text, ok = QInputDialog.getText(self, 'Group name', 'Enter the group name:')
                if ok:
                    self.filePreferences['ExperimentType'] = text
                    self.FM.Read_Experiment_File(\
                            filepath = self.WSPPreferences['currentFilePath'],\
                            filename = self.WSPPreferences['currentFileName'],\
                            read_multiple_files = multiple_files)
            elif extension == 'h5':
                self.statusBar().showMessage('Opening ' + self.WSPPreferences['currentFileName'])
                self.FM.checkFile(
                    self.WSPPreferences['currentFilePath'],\
                    self.WSPPreferences['currentFileName'],\
                    self.filePreferences)
                if self.filePreferences['WSPPython']:
                    self.statusBar().showMessage('Opening ' + self.WSPPreferences['currentFileName'] + \
                        '. WSPPython file checked.')
                    item, ok = QInputDialog.getItem(self, "Select a group",\
                                "List of groups", self.WSPPreferences['AvailableGroups'], 0, False)
                    if ok:
                        self.FM.Read_Experiment_File(filepath = self.WSPPreferences['currentFilePath'],\
                                    filename = self.WSPPreferences['currentFileName'],\
                                    group_name = item)
            else:
                return
            self.statusBar().showMessage(self.WSPPreferences['currentFileName'] + ' loaded.')
            self.selectUserTabs()

    def saveAsFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.WSPPreferences['currentFilePath']):
            path = self.WSPPreferences['currentFilePath']
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
                self.WSPPreferences['currentGroupName'] = text

                # # ask for ExperimentType
                # text, ok = QInputDialog.getText(self, 'Experiment type', 'Enter the experiment type:')
                # if ok:
                #     self.filePreferences['ExperimentType'] = text
                self.statusBar().showMessage('Saving ' + futureFileName + '/' + self.WSPPreferences['currentGroupName'])
                self.FM.Write_Experiment_to_h5(filepath = futureFilePath,\
                                               filename = futureFileName, \
                                               group_name = self.WSPPreferences['currentGroupName'], \
                                               force_overwrite = True,
                                               ExperimentType = self.filePreferences['ExperimentType'])
                self.WSPPreferences['currentFilePath'] = futureFilePath
                self.WSPPreferences['currentFileName'] = futureFileName
                self.statusBar().showMessage(futureFileName + '/' + self.WSPPreferences['currentGroupName']  + ' saved.')

    def convertFilesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.WSPPreferences['currentFilePath']):
            path = self.WSPPreferences['currentFilePath']
        else:
            path = ''
        filename, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", path,"All Files (*);;Python Files (*.py)", options=options)
        if filename:
            if len(filename)>1:
                multiple_files = True
            else:
                multiple_files = False

            currentFilePath,currentFileName = os.path.split(filename[0])
            self.WSPPreferences['currentFilePath'] = currentFilePath
            self.WSPPreferences['currentFileName'] = currentFileName

            if os.path.isdir(self.WSPPreferences['currentFilePath']):
                path = self.WSPPreferences['currentFilePath']
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
                    self.WSPPreferences['currentGroupName'] = text

                    # ask for ExperimentType
                    text, ok = QInputDialog.getText(self, 'Experiment type', 'Enter the experiment type:')
                    if ok:
                        self.filePreferences['ExperimentType'] = text

                        self.statusBar().showMessage('Opening: ' + self.WSPPreferences['currentFileName'])
                        self.FM.Read_Experiment_File(filepath = self.WSPPreferences['currentFilePath'],\
                                                filename = self.WSPPreferences['currentFileName'],\
                                                read_multiple_files = multiple_files)
                        self.statusBar().showMessage('Saving ' + futureFileName)
                        self.FM.Write_Experiment_to_h5(filepath = futureFilePath,\
                                                       filename = futureFileName, \
                                                       group_name = self.WSPPreferences['currentGroupName'], \
                                                       force_overwrite = True,
                                                       ExperimentType = self.filePreferences['ExperimentType'])
                        self.statusBar().showMessage(futureFileName + ' saved.')
                        self.WSPPreferences['currentFilePath'] = futureFilePath
                        self.WSPPreferences['currentFileName'] = futureFileName

    def filePreferencesDialog(self):
        self.filePreferences = {'WSPPython':True,'fileversion':1.0,'ExperimentType':'uspm'}
        if 'WSPPython' in self.filePreferences.keys():
            dia = filePreferencesGUI(filePreferences=self.filePreferences)
            if dia.result():
                self.filePreferences = dia.filePreferences

    def WSPPreferences(self):
        pass

    def loadPreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        # if not os.path.isdir(prefFile):
        #     path = self.WSPPreferences['currentFilePath']
        # Create the h5 file
        f = h5py.File(prefFile,'a')

        # Give the file version
        if 'currentFilePath' in f.attrs.keys():
            self.WSPPreferences['currentFilePath'] = f.attrs['currentFilePath']
        else:
            self.WSPPreferences['currentFilePath'] = ''
        f.close()

    def savePreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        f = h5py.File(prefFile,'a')
        # Give the file version
        f.attrs['currentFilePath'] = self.WSPPreferences['currentFilePath']
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

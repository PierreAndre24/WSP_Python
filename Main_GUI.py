import sys, os, h5py, string
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QAction, QFileDialog, QInputDialog, QFormLayout,
                            QScrollArea, QVBoxLayout, QTextEdit, QGridLayout,
                            QFrame)

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from libs.GUI_Preferences import filePreferencesGUI
import libs.MultiDimExperiment as MultiDimExperiment
import libs.ExperimentFileManager as ExperimentFileManager
from gui.WSPTruncateArray import WSPTruncateArray
from gui.WSP1Dplot import WSP1Dplot

class App(QMainWindow):

    def __init__(self):
        super(App,self).__init__()
        self.title = 'WSP Python'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400

        app_icon = QIcon()
        app_icon.addFile('gui/icons/16x16.png', QSize(16,16))
        app_icon.addFile('gui/icons/24x24.png', QSize(24,24))
        app_icon.addFile('gui/icons/32x32.png', QSize(32,32))
        app_icon.addFile('gui/icons/64x64.png', QSize(64,64))
        app_icon.addFile('gui/icons/128x128.png', QSize(128,128))
        app_icon.addFile('gui/icons/256x256.png', QSize(256,256))
        app_icon.addFile('gui/icons/512x512.png', QSize(512,512))
        app.setWindowIcon(app_icon)

        self.WSPPreferences = {}
        self.filePreferences = {}
        self.loadPreferences()
        self.XP = MultiDimExperiment.MultiDimExperiment()
        self.FM = ExperimentFileManager.ExperimentFileManager(self.XP)

        self.initUserMenu()
        self.initMainGL() # main QWidget

        self.show()

    ################################
    # Init interface
    def initUserMenu(self):
        '''
        Initializes entries of the menu bar
        Todo: clean up icons
        '''
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

        # # system preferences
        # preferencesButton = QAction(QIcon('exit24.png'), 'Preferences', self)
        # preferencesButton.setStatusTip('System preferences')
        # preferencesButton.setShortcut('Ctrl+,')
        # preferencesButton.triggered.connect(self.call_WSPPreferences)
        # fileMenu.addAction(preferencesButton)
        # fileMenu.addSeparator()

        # exit
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.closeApplication)
        fileMenu.addAction(exitButton)

        ####################
        # Help menu buttons

        # load a file (or multiple_files)
        testButton = QAction(QIcon('exit24.png'), 'Test', self)
        testButton.setStatusTip('Test something')
        testButton.triggered.connect(self.testFunction)
        helpMenu.addAction(testButton)

    def initMainGL(self):
        '''
        Initializes the main widget of the application, as well as all subGUI
        that can be called later on.
        To add a new widget, create it and give the position in the selection
        loop.
        Todo:
        '''

        # self.setCentralWidget(QFrame())
        self.mainGL = QGridLayout()
        self.mainW = QWidget(self)

        # Create widgets
        self.WSPWidgets = {}
        self.WSPWidgets['WSPTruncateArray'] = WSPTruncateArray()
        self.WSPWidgets['WSP1Dplot'] = WSP1Dplot()

        # Position widgets
        self.mainGL.addWidget(self.WSPWidgets['WSP1Dplot'],1,1,1,1)
        self.mainGL.addWidget(self.WSPWidgets['WSPTruncateArray'],2,1,1,1)
        # self.create_TA_UI() #Trace Analysis
        # self.create_IPPM_UI() #Isolated Position, Pulse Map
        # self.create_IPSS_UI() #Isolated Position, Single Spin

        # to filter out the initial call
        if 'ExperimentType' in self.filePreferences:
            if self.filePreferences['ExperimentType'] == 'uspm':
                # Add tabs
                print 'uspm'
            elif self.filePreferences['ExperimentType'] == 'ipss':
                # Add tabs
                print 'ipss'
            elif self.filePreferences['ExperimentType'] == 'ippm':
                # Add tabs
                print 'ippm'

        self.mainW.setLayout(self.mainGL)
        self.setCentralWidget(self.mainW)
        # self.setLayout(self.mainGL)

    def refrefhMainGL(self):
        '''
        Refresh elements of all subGUIs.
        Todo:
        '''

        self.WSPWidgets['WSP1Dplot'].updateLayout(self.XP.ExperimentalData['dimensions'])
        self.WSPWidgets['WSPTruncateArray'].updateLayout(self.XP.ExperimentalData['dimensions'])


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
            self.WSPPreferences['currentFileName'] = currentFileName

            extension = self.WSPPreferences['currentFileName'].split('.')
            extension = extension[-1]
            self.XP = MultiDimExperiment.MultiDimExperiment()

            if extension == 'lvm':
                self.statusBar().showMessage('Opening ' + self.WSPPreferences['currentFileName'])
                # ask for group name
                text, ok = QInputDialog.getText(self, 'Experiment type', 'Enter the experiment type:')
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
                                "List of groups", self.filePreferences['AvailableGroups'], 0, False)
                    if ok:
                        self.FM.Read_Experiment_File(filepath = self.WSPPreferences['currentFilePath'],\
                                    filename = self.WSPPreferences['currentFileName'],\
                                    group_name = item)
            else:
                return
            self.statusBar().showMessage(self.WSPPreferences['currentFileName'] + ' loaded.')
            self.refrefhMainGL()

    def saveAsFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if os.path.isdir(self.WSPPreferences['currentFilePath']):
            path = self.WSPPreferences['currentFilePath']
        else:
            path = ''
        defaultpath = path + os.sep + string.split(self.WSPPreferences['currentFileName'],'.')[0] + '.h5'
        filename, ok = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",defaultpath,"All Files (*);;Text Files (*.txt)", options=options)
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

            defaultpath = path + os.sep + string.split(self.WSPPreferences['currentFileName'],'.')[0] + '.h5'
            filename, ok = QFileDialog.getSaveFileName(self,"Save file",defaultpath,"All Files (*);;Text Files (*.txt)", options=options)
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

                        self.refrefhMainGL()

    def filePreferencesDialog(self):
        self.filePreferences = {'WSPPython':True,'fileversion':1.0,'ExperimentType':'uspm'}
        if 'WSPPython' in self.filePreferences.keys():
            dia = filePreferencesGUI(filePreferences = self.filePreferences)
            if dia.result():
                self.filePreferences = dia.filePreferences

    # def call_WSPPreferences(self):
    #     pass

    def loadPreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        # if not os.path.isdir(prefFile):
        #     path = self.WSPPreferences['currentFilePath']
        # Create the h5 file
        f = h5py.File(prefFile,'a')

        ###############################
        # Menu information
        # Give the file version
        if 'currentFilePath' in f.attrs.keys():
            self.WSPPreferences['currentFilePath'] = f.attrs['currentFilePath']
        else:
            self.WSPPreferences['currentFilePath'] = ''

        gn = 'ExperimentTypes'
        if gn in f.keys():
            g = f[gn]
            self.WSPPreferences[gn] = {}
            for sgn in g.keys():
                sg = g[sgn]
                self.WSPPreferences[gn][sgn] = {}
                self.WSPPreferences[gn][sgn]['definition'] = sg.attrs['definition']
                self.WSPPreferences[gn][sgn]['pannels'] = sg.attrs['pannels']

        f.close()

    def savePreferences(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        prefFile = dirname + os.sep + 'preferences.h5'
        f = h5py.File(prefFile,'a')

        ###############################
        # Menu information
        f.attrs['currentFilePath'] = self.WSPPreferences['currentFilePath']

        ###############################
        # Experiment Type names and definitions
        gn = 'ExperimentTypes'
        if gn not in f.keys():
            g = f.create_group(gn)
        else:
            g = f[gn]

        # uspm
        sgn = 'uspm'
        if sgn not in f['ExperimentTypes'].keys():
            sg = g.create_group(sgn)
        else:
            sg = g[sgn]
        sg.attrs['definition'] = 'Micro second pulse map.'
        sg.attrs['pannels'] = ['TimeTrace','usPulseMap']


        # TT_AC_Tunneling
        sgn = 'uspm'
        if sgn not in f['ExperimentTypes'].keys():
            sg = g.create_group(sgn)
        else:
            sg = g[sgn]
        sg.attrs['definition'] = 'Time Trace Across Transition with tunneling event to be characterized.'
        sg.attrs['pannels'] = ['TimeTrace']

        ###############################
        # Tabs
        # we save preferences dependent on ExperimentType
        # Tabs -

        f.close()

    def closeApplication(self):
        self.savePreferences()
        self.close()

    def testFunction(self):
        for t in self.WSPWidgets.keys():
            print t + ' said ' + self.WSPWidgets[t].toPlainText()

    def preferences(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

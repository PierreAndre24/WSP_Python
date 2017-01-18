from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QLabel,
                             QComboBox, QPushButton, QCheckBox)
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from gui.subGUI_Model import Model
from libs.array_operations import *

class WSPBasicArrayOps(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.selectionWidget = []
        self.header = {}
        self.selWid = {}
        self.footer = {}
        self.FLAG_initialized = False
        self.FLAG_figure_open = False
        self.FLAG_auto_update = False
        #self.create_all_widgets()

    def add_all_widgets_to_grid(self):
        self.add_header_widgets_to_grid()
        self.add_selection_widgets_to_grid()

    def add_header_widgets_to_grid(self):
        for k, v in self.header.items():
            self.grid.addWidget(v, 0, v.col, 1, 1)
        self.header_NofLines = 1

    def add_selection_widgets_to_grid(self):
        for dim in range(len(self.originalRanges)):
            for k, v in self.selWid[dim].items():
                self.grid.addWidget(v, dim + self.header_NofLines, v.col, 1, 1)

    def create_all_widgets(self):
        self._create_header_widgets()
        self._create_selection_widgets()

    def _create_header_widgets(self):
        # First line of the widgets
        if 'widget label' not in self.header.keys():
            self.header['widget label'] = QLabel('Array Ops.')
            self.header['widget label'].col = 0
        if 'apply' not in self.header.keys():
            self.header['apply'] = QPushButton("Apply")
            self.header['apply'].clicked.connect(self.call_Apply)
            self.header['apply'].col = 1
        if 'FFT' not in self.header.keys():
            self.header['FFT'] = QLabel('FFT')
            self.header['FFT'].col = 3
        if 'FFT filter' not in self.header.keys():
            self.header['FFT filter'] = QLabel('FFT filt.')
            self.header['FFT filter'].col = 4
        if 'derivative' not in self.header.keys():
            self.header['derivative'] = QLabel('Deriv.')
            self.header['derivative'].col = 5
        if 'smooth' not in self.header.keys():
            self.header['smooth'] = QLabel('Smooth')
            self.header['smooth'].col = 6
        if 'average' not in self.header.keys():
            self.header['average'] = QLabel('Average')
            self.header['average'].col = 7

    def _create_selection_widgets(self):
        for dim in range(len(self.originalRanges)):
            # check if dimension already exists
            if dim not in self.selWid.keys():
                self.selWid[dim] = {}
                self.selWid[dim]['label'] = QLabel('Dim. ' + str(dim))
                self.selWid[dim]['label'].col = 0

                self.selWid[dim]['combo start'] = QComboBox()
                rangetxt = [str(x) for x in range(self.originalRanges[dim])]
                self.selWid[dim]['combo start'].addItems(rangetxt)
                self.selWid[dim]['combo start'].setCurrentIndex(0)
                self.selWid[dim]['combo start'].activated.connect(self.call_selection_update)
                self.selWid[dim]['combo start'].dim = dim
                self.selWid[dim]['combo start'].element = 'combo_start'
                self.selWid[dim]['combo start'].col = 1

                self.selWid[dim]['combo end'] = QComboBox()
                rangetxt = [str(x) for x in range(self.originalRanges[dim])]
                self.selWid[dim]['combo end'].addItems(rangetxt)
                self.selWid[dim]['combo end'].activated.connect(self.call_selection_update)
                self.selWid[dim]['combo end'].setCurrentIndex(self.originalRanges[dim]-1)
                self.selWid[dim]['combo end'].dim = dim
                self.selWid[dim]['combo end'].element = 'combo_end'
                self.selWid[dim]['combo end'].col = 2

                self.selWid[dim]['FFT'] = QCheckBox()
                self.selWid[dim]['FFT'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['FFT'].dim = dim
                self.selWid[dim]['FFT'].element = 'FFT'
                self.selWid[dim]['FFT'].col = 3

                self.selWid[dim]['FFT filter'] = QCheckBox()
                self.selWid[dim]['FFT filter'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['FFT filter'].dim = dim
                self.selWid[dim]['FFT filter'].element = 'FFT filter'
                self.selWid[dim]['FFT filter'].col = 4

                self.selWid[dim]['derivative'] = QCheckBox()
                self.selWid[dim]['derivative'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['derivative'].dim = dim
                self.selWid[dim]['derivative'].element = 'derivative'
                self.selWid[dim]['derivative'].col = 5

                self.selWid[dim]['smooth'] = QCheckBox()
                self.selWid[dim]['smooth'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['smooth'].dim = dim
                self.selWid[dim]['smooth'].element = 'smooth'
                self.selWid[dim]['smooth'].col = 6

                self.selWid[dim]['average'] = QCheckBox()
                self.selWid[dim]['average'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['average'].dim = dim
                self.selWid[dim]['average'].element = 'average'
                self.selWid[dim]['average'].col = 7

    def initial_values(self, ExperimentType, values=None):
        if values == None:
            dac_measurements = ['uspm']
            if ExperimentType in dac_measurements:
                self.call_check_widgets()

    def updateLayout(self,XP):
        # update the available experiment
        self.XP = XP
        self.originalRanges = self.XP.ExperimentalData['dimensions']
        # create the widgets based on the available experiment
        self.create_all_widgets()

        # If necessary, remove all existing widgets
        self.remove_all_widgets_from_grid()

        # Add all widgets to the grid
        self.add_all_widgets_to_grid()

        self.FLAG_initialized = True
        self.setLayout(self.grid)
        self.call_check_widgets()

    def remove_all_widgets_from_grid(self):
        if self.header != {}:
            for w in self.header.keys():
                self.grid.removeWidget(self.header[w])
        if self.footer != {}:
            for w in self.footer.keys():
                self.grid.removeWidget(self.footer[w])
        if self.selWid != {}:
            for d in self.selWid.keys():
                for w in self.selWid[d].keys():
                    self.grid.removeWidget(self.selWid[d][w])

    def call_selection_update(self):
        element = self.sender().element
        dim = self.sender().dim
        # wait for XP loaded and widget initialized
        # if (self.originalRanges[0]) != 0 and len(self.selectionWidget) == len():
        if self.FLAG_initialized:
            if element == 'xaxis_checkbox':
                self.check_xaxis_checkbox(dim)

            if element == 'stack_checkbox':
                self.check_stack_checkbox(dim)

            if  (element == 'left_arrow') or (element == 'right_arrow'):
                self.call_LR_arrow_clicked(element, dim)
                self.check_LR_arrow(dim)

            # if (element == 'combo_start') or (element == 'combo_end'):
            #     self.check_combo_SE(dim)

        self.handle_auto_update()

    def call_check_widgets(self):
        '''
        Method called at the end on the 'load_preferences', to check the
        widget hide/show properties consistency.
        '''
        pass

    def call_Apply(self):
        pass

    def select_slice(self, array):

        FLAG_stack = False
        for dim in range(len(self.originalRanges)):
            if self.selWid[dim]['stack'].isChecked():
                FLAG_stack = True
                jstart = np.min([self.selWid[dim]['combo start'].currentIndex(),\
                                 self.selWid[dim]['combo end'].currentIndex()])
                jend = np.max([self.selWid[dim]['combo start'].currentIndex(),\
                               self.selWid[dim]['combo end'].currentIndex()])

        if not FLAG_stack:
            #y = np.zeros((iend - istart + 1, 1))
            sl = [] # slice
            for dim in range(len(self.originalRanges)):
                if not self.selWid[dim]['x axis'].isChecked():
                    i = self.selWid[dim]['combo start'].currentIndex()
                    sl.append([i])
                elif self.selWid[dim]['x axis'].isChecked():
                    istart = np.min([self.selWid[dim]['combo start'].currentIndex(),\
                                     self.selWid[dim]['combo end'].currentIndex()])
                    iend = np.max([self.selWid[dim]['combo start'].currentIndex(),\
                                   self.selWid[dim]['combo end'].currentIndex()])
                    sl.append([istart, iend ])
            arr = take_subarray(array, sl)
            arr = np.reshape(arr, (iend - istart + 1, 1))
            return arr
        else:
            sl = [] # slice
            for dim in range(len(self.originalRanges)):
                if (not self.selWid[dim]['x axis'].isChecked()) and \
                    not self.selWid[dim]['stack'].isChecked():
                    i = self.selWid[dim]['combo start'].currentIndex()
                    sl.append([i])
                elif self.selWid[dim]['x axis'].isChecked():
                    istart = np.min([self.selWid[dim]['combo start'].currentIndex(),\
                                     self.selWid[dim]['combo end'].currentIndex()])
                    iend = np.max([self.selWid[dim]['combo start'].currentIndex(),\
                                   self.selWid[dim]['combo end'].currentIndex()])
                    sl.append([istart, iend])
                    dim_x = dim
                elif self.selWid[dim]['stack'].isChecked():
                    jstart = np.min([self.selWid[dim]['combo start'].currentIndex(),\
                                     self.selWid[dim]['combo end'].currentIndex()])
                    jend = np.max([self.selWid[dim]['combo start'].currentIndex(),\
                                   self.selWid[dim]['combo end'].currentIndex()])
                    sl.append([jstart, jend])
                    dim_stack = dim
            arr = take_subarray(array, sl)
            if dim_stack < dim_x:
                arr.transpose()
            arr = np.reshape(arr, (iend - istart + 1, jend - jstart + 1))
            return arr

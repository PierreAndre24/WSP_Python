from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QLabel,
                             QComboBox, QPushButton, QCheckBox)
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from gui.subGUI_Model import Model
from libs.array_operations import *

class WSP1D2Dplot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.selectionWidget = []
        self.header = {}
        self.selWid = {}
        self.footer = {}
        self.FLAG_initialized = False
        self.FLAG_figure_1d_open = False
        self.FLAG_figure_2d_open = False
        self.FLAG_auto_update = False
        self.FLAG_stack = False
        #self.create_all_widgets()

    def add_all_widgets_to_grid(self):
        self.add_header_widgets_to_grid()
        self.add_selection_widgets_to_grid()

    def add_header_widgets_to_grid(self):
        self.grid.addWidget(self.header['widget label'], 0, \
                            self.header['widget label'].col, 1, 1)
        self.grid.addWidget(self.header['x axis'], 0, \
                            self.header['x axis'].col, 1, 1)
        self.grid.addWidget(self.header['stack dimension'], 0, \
                            self.header['stack dimension'].col, 1, 1)
        self.grid.addWidget(self.header['plot 1d button'], 0, \
                            self.header['plot 1d button'].col, 1, 1)
        self.grid.addWidget(self.header['plot 2d button'], 0, \
                            self.header['plot 2d button'].col, 1, 1)
        self.grid.addWidget(self.header['auto update'], 0, \
                            self.header['auto update'].col, 1, 1)
        self.header_NofLines = 1

    def add_selection_widgets_to_grid(self):

        for dim in range(len(self.originalRanges)):
            self.grid.addWidget(self.selWid[dim]['label'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['label'].col, 1, 1)

            # which x-axis check box
            self.grid.addWidget(self.selWid[dim]['x axis'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['x axis'].col, 1, 1)

            # if stack, which axis ? check box
            self.grid.addWidget(self.selWid[dim]['stack'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['stack'].col, 1, 1)


            self.grid.addWidget(self.selWid[dim]['combo start'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['combo start'].col, 1, 1)

            self.grid.addWidget(self.selWid[dim]['left arrow'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['left arrow'].col, 1, 1)

            self.grid.addWidget(self.selWid[dim]['right arrow'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['right arrow'].col, 1, 1)

    def create_all_widgets(self):
        self._create_header_widgets()
        self._create_selection_widgets()

    def _create_header_widgets(self):
        # First line of the widgets
        if 'widget label' not in self.header.keys():
            self.header['widget label'] = QLabel('1D plot')
            self.header['widget label'].col = 0
        if 'x axis' not in self.header.keys():
            self.header['x axis'] = QLabel('X-axis')
            self.header['x axis'].col = 1
        if 'stack dimension' not in self.header.keys():
            self.header['stack dimension'] = QLabel('Stack/Y')
            self.header['stack dimension'].col = 2
        if 'plot 1d button' not in self.header.keys():
            self.header['plot 1d button'] = QPushButton("Plot 1D")
            self.header['plot 1d button'].clicked.connect(self.call_Plot1D)
            self.header['plot 1d button'].col = 3

        if 'plot 2d button' not in self.header.keys():
            self.header['plot 2d button'] = QPushButton("Plot 2D")
            self.header['plot 2d button'].setEnabled(False)
            self.header['plot 2d button'].clicked.connect(self.call_Plot2D)
            self.header['plot 2d button'].col = 4

        if 'auto update' not in self.header.keys():
            self.header['auto update'] = QCheckBox("auto update")
            self.header['auto update'].stateChanged.connect(self.call_auto_update)
            self.header['auto update'].setChecked(False)
            self.header['auto update'].col = 5

    def _create_selection_widgets(self):
        for dim in range(len(self.originalRanges)):
            # check if dimension already exists
            if dim not in self.selWid.keys():
                self.selWid[dim] = {}
                self.selWid[dim]['label'] = QLabel('Dimension ' + str(dim))
                self.selWid[dim]['label'].col = 0

                self.selWid[dim]['x axis'] = QCheckBox()
                # self.selWid[dim]['x axis'].setChecked(True)
                self.selWid[dim]['x axis'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['x axis'].dim = dim
                self.selWid[dim]['x axis'].element = 'xaxis_checkbox'
                self.selWid[dim]['x axis'].col = 1

                self.selWid[dim]['stack'] = QCheckBox()
                # self.selWid[dim]['stack'].setChecked(True)
                self.selWid[dim]['stack'].stateChanged.connect(self.call_selection_update)
                self.selWid[dim]['stack'].dim = dim
                self.selWid[dim]['stack'].element = 'stack_checkbox'
                self.selWid[dim]['stack'].col = 2

                self.selWid[dim]['combo start'] = QComboBox()
                rangetxt = [str(x) for x in range(self.originalRanges[dim])]
                self.selWid[dim]['combo start'].addItems(rangetxt)
                self.selWid[dim]['combo start'].setCurrentIndex(0)
                self.selWid[dim]['combo start'].activated.connect(self.call_selection_update)
                self.selWid[dim]['combo start'].dim = dim
                self.selWid[dim]['combo start'].element = 'combo_start'
                self.selWid[dim]['combo start'].col = 3

                self.selWid[dim]['combo end'] = QComboBox()
                rangetxt = [str(x) for x in range(self.originalRanges[dim])]
                self.selWid[dim]['combo end'].addItems(rangetxt)
                self.selWid[dim]['combo end'].activated.connect(self.call_selection_update)
                self.selWid[dim]['combo end'].setCurrentIndex(self.originalRanges[dim]-1)
                self.selWid[dim]['combo end'].dim = dim
                self.selWid[dim]['combo end'].element = 'combo_end'
                self.selWid[dim]['combo end'].col = 4


                self.selWid[dim]['left arrow'] = QToolButton()
                self.selWid[dim]['left arrow'].setArrowType(QtCore.Qt.LeftArrow)
                self.selWid[dim]['left arrow'].clicked.connect(self.call_selection_update)
                self.selWid[dim]['left arrow'].dim = dim
                self.selWid[dim]['left arrow'].element = 'left_arrow'
                self.selWid[dim]['left arrow'].col = 4

                self.selWid[dim]['right arrow'] = QToolButton()
                self.selWid[dim]['right arrow'].setArrowType(QtCore.Qt.RightArrow)
                self.selWid[dim]['right arrow'].clicked.connect(self.call_selection_update)
                self.selWid[dim]['right arrow'].dim = dim
                self.selWid[dim]['right arrow'].element = 'right_arrow'
                self.selWid[dim]['right arrow'].col = 5

    def initial_values(self, ExperimentType, values=None):
        if values == None:
            dac_measurements = ['uspm']
            if ExperimentType in dac_measurements:

                # default x-axis is dim 1
                for dim in range(len(self.originalRanges)):
                    if dim == 1:
                        self.selWid[dim]['x axis'].setCheckState(2)
                    else:
                        self.selWid[dim]['x axis'].setCheckState(0)

                # no stack
                for dim in range(len(self.originalRanges)):
                    self.selWid[dim]['stack'].setCheckState(0)
                self.call_check_widgets()

    def updateLayout(self, XP, WSPPreferences):
        # update the available experiment
        self.XP = XP
        self.WSPPreferences = WSPPreferences
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
        for dim in range(len(self.originalRanges)):
            self.check_LR_arrow(dim)

    def call_LR_arrow_clicked(self, element, dim):
        '''
        Change the current index of the start combo box upon click
        '''
        currentIndex = self.selWid[dim]['combo start'].currentIndex()
        if element == 'right_arrow':
            currentIndex += 1
        elif element == 'left_arrow':
            currentIndex -= 1
        self.selWid[dim]['combo start'].setCurrentIndex(currentIndex)

    def check_xaxis_checkbox(self, dim):
        '''
        Plotting multiple traces is authorized only for a single dimension.
        Checkbox mutual exclusion.
        '''
        # Checkbox first
        # Then, their states are checked to enable or disable some widgets
        # Only one can be unchecked
        # If the check box at dim is released, then do
        if not self.selWid[dim]['x axis'].isChecked():
            for i in range(len(self.originalRanges)):
                if i != dim:
                    self.selWid[i]['x axis'].setChecked(True)
        for i in range(len(self.originalRanges)):
            self.check_isVisible_combobox(i)

    def check_stack_checkbox(self, dim):
        '''
        Plotting multiple traces is authorized only for a single dimension.
        Checkbox mutual exclusion.
        '''
        # Checkbox first
        # Then, their states are checked to enable or disable some widgets
        # Only one can be unchecked
        # If the check box at dim is released, then do
        if self.selWid[dim]['stack'].isChecked():
            if self.selWid[dim]['x axis'].isChecked():
                self.selWid[dim]['stack'].setChecked(False)
            else:
                for i in range(len(self.originalRanges)):
                    if i != dim:
                        self.selWid[i]['stack'].setChecked(False)
        for i in range(len(self.originalRanges)):
            self.check_isVisible_combobox(i)

        self.check_2d_plotbutton()

    def check_2d_plotbutton(self):
        self.FLAG_stack = False
        for k, v in self.selWid.items():
            if v['stack'].isChecked():
                self.FLAG_stack = True
        if self.FLAG_stack:
            self.header['plot 2d button'].setEnabled(True)
        else:
            self.header['plot 2d button'].setEnabled(False)

    def check_isVisible_combobox(self,dim):
        '''
        Show or hide the combobox end and the left/right selection buttons
        depending on the checkbox state
        '''
        # Checkbox Single trace/dim or range
        if not (self.selWid[dim]['stack'].isChecked() or self.selWid[dim]['x axis'].isChecked()):
            self.grid.removeWidget(self.selWid[dim]['combo end'])
            self.selWid[dim]['combo end'].setVisible(False)

            self.grid.addWidget(self.selWid[dim]['left arrow'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['left arrow'].col, 1, 1)
            self.selWid[dim]['left arrow'].setVisible(True)

            self.grid.addWidget(self.selWid[dim]['right arrow'], \
                                dim + self.header_NofLines,
                                self.selWid[dim]['right arrow'].col, 1, 1)
            self.selWid[dim]['right arrow'].setVisible(True)

        else:
            self.grid.removeWidget(self.selWid[dim]['left arrow'])
            self.selWid[dim]['left arrow'].setVisible(False)

            self.grid.removeWidget(self.selWid[dim]['right arrow'])
            self.selWid[dim]['right arrow'].setVisible(False)

            self.grid.addWidget(self.selWid[dim]['combo end'], \
                                dim + self.header_NofLines, \
                                self.selWid[dim]['combo end'].col, 1, 2)
            self.selWid[dim]['combo end'].setVisible(True)

    def check_LR_arrow(self,dim):
        '''
        Show or hide the left/right button depending on the combobox selection
        '''
        # first/last element selected
        if self.selWid[dim]['stack'].isChecked():
            if self.originalRanges[dim] == 1:
                self.grid.removeWidget(self.selWid[dim]['left arrow'])
                self.selWid[dim]['left arrow'].setVisible(False)
                self.grid.removeWidget(self.selWid[dim]['right arrow'])
                self.selWid[dim]['right arrow'].setVisible(False)
            elif self.selWid[dim]['combo start'].currentIndex() == 0:
                self.grid.removeWidget(self.selWid[dim]['left arrow'])
                self.selWid[dim]['left arrow'].setVisible(False)
                if not self.selWid[dim]['right arrow'].isVisible():
                    self.grid.addWidget(self.selWid[dim]['right arrow'], \
                                        dim + self.header_NofLines, \
                                        self.selWid[dim]['right arrow'].col, 1, 1)
                    self.selWid[dim]['right arrow'].setVisible(True)
            elif self.selWid[dim]['combo start'].currentIndex() == self.originalRanges[dim]-1:
                self.grid.removeWidget(self.selWid[dim]['right arrow'])
                self.selWid[dim]['right arrow'].setVisible(False)
                if not self.selWid[dim]['left arrow'].isVisible():
                    self.grid.addWidget(self.selWid[dim]['left arrow'], \
                                        dim + self.header_NofLines, \
                                        self.selWid[dim]['left arrow'].col, 1, 1)
                    self.selWid[dim]['left arrow'].setVisible(True)
            else:
                self.grid.addWidget(self.selWid[dim]['left arrow'], \
                                    dim + self.header_NofLines, \
                                    self.selWid[dim]['left arrow'].col, 1, 1)
                self.selWid[dim]['left arrow'].setVisible(True)

                self.grid.addWidget(self.selWid[dim]['right arrow'], \
                                    dim + self.header_NofLines, \
                                    self.selWid[dim]['right arrow'].col, 1, 1)
                self.selWid[dim]['right arrow'].setVisible(True)

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

    def handle_figure_1d_close(self):
        self.FLAG_figure_1d_open = False

    def handle_figure_2d_close(self):
        self.FLAG_figure_2d_open = False

    def call_Plot1D(self):
        if not self.FLAG_figure_1d_open:
            self.init_Plot1D()
        self.update_Plot1D() # apply only if the figure exists

    def call_Plot2D(self):
        if not self.FLAG_figure_2d_open:
            self.init_Plot2D()
        self.update_Plot2D() # apply only if the figure exists

    def call_auto_update(self):
        if self.header['auto update'].isChecked():
            self.FLAG_auto_update = True
        else:
            self.FLAG_auto_update = False

    def handle_auto_update(self):
        if self.FLAG_auto_update:
            if self.FLAG_figure_1d_open:
                self.update_Plot1D()
            if self.FLAG_figure_2d_open:
                self.update_Plot2D()

    def update_Plot1D(self):
        if self.FLAG_figure_1d_open:
            # select data
            Y = self.select_slice(self.XP.ExperimentalData['data'])
            X = np.arange(Y.shape[0])
            # sl, rs = self.select_slice()
            # Y = np.reshape(self.XP.ExperimentalData['data'][sl],rs)
            # draw
            for j,line in enumerate(self.lines_Plot1D):
                line.set_ydata(Y[:,j])
                line.set_xdata(X)
            self.fig_Plot1D.canvas.draw()

    def update_Plot2D(self):
        if self.FLAG_figure_2d_open:
            # select data
            # Y = self.select_slice(self.XP.ExperimentalData['data'])
            # X = np.arange(Y.shape[0])
            z = self.select_slice(self.XP.ExperimentalData['data'])
            # z = XP.ExperimentalData['data'][qpc,0,:,:,0]
            self.lines_Plot2D.set_data(z)
            # draw
            self.fig_Plot2D.canvas.draw()


    def init_Plot1D(self):
        plt.ion()
        self.fig_Plot1D = plt.figure(1)
        self.fig_Plot1D.canvas.mpl_connect('close_event', self.handle_figure_1d_close)
        self.FLAG_figure_1d_open = True
        self.ax_Plot1D = self.fig_Plot1D.add_subplot(1, 1, 1)
        Y = self.select_slice(self.XP.ExperimentalData['data'])
        self.lines_Plot1D = self.ax_Plot1D.plot(Y)

    def init_Plot2D(self):
        plt.ion()
        self.fig_Plot2D = plt.figure(2)
        self.fig_Plot2D.canvas.mpl_connect('close_event', self.handle_figure_2d_close)
        self.FLAG_figure_2d_open = True
        self.ax_Plot2D = self.fig_Plot2D.add_subplot(1, 1, 1)
        z = self.select_slice(self.XP.ExperimentalData['data'])
        # self.lines_Plot2D = self.ax_Plot2D.plot(Y)
        self.lines_Plot2D = plt.imshow(z, interpolation='none')
        plt.clim()   # clamp the color limits
        plt.title("map of " + self.WSPPreferences['currentFileName'])

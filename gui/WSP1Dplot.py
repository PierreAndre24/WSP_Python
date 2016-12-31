from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QLabel,
                             QComboBox, QPushButton, QCheckBox)
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from gui.subGUI_Model import Model

class WSP1Dplot(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.selectionWidget = []
        self.FLAG_initialized = False

    def updateLayout(self,XP):

        self.XP = XP
        originalRanges = self.XP.ExperimentalData['dimensions']

        # If necessary, remove all existing widgets
        if len(self.selectionWidget) > 0:
            flattened  = [val for sublist in self.selectionWidget for val in sublist]
            for w in flattened:
                self.grid.removeWidget(w)

        # First line of the widgets
        selectionWidgetCurrentDim = []
        label = QLabel('1D plot')
        selectionWidgetCurrentDim.append(label)
        self.grid.addWidget(label, 0, 0, 1, 1)
        self.selectionWidget.append(selectionWidgetCurrentDim)

        # put the new widgets
        self.originalRanges = originalRanges

        for dim in range(len(self.originalRanges)):
            selectionWidgetCurrentDim = []

            label = QLabel('Dimension ' + str(dim))
            selectionWidgetCurrentDim.append(label)
            self.grid.addWidget(label, dim + 1, 0, 1, 1)

            selectionWidgetCurrentDim.append(QCheckBox("first only " + str(dim)))
            selectionWidgetCurrentDim[1].setChecked(True)
            selectionWidgetCurrentDim[1].stateChanged.connect(self.call_selection_update)
            selectionWidgetCurrentDim[1].dim = dim
            selectionWidgetCurrentDim[1].element = 'single_trace_checkbox'
            self.grid.addWidget(selectionWidgetCurrentDim[1], \
                                dim + 1, 1, 1, 1)

            rangetxt = [str(x) for x in range(self.originalRanges[dim])]
            combo_start = QComboBox()
            combo_start.addItems(rangetxt)
            combo_start.setCurrentIndex(0)
            selectionWidgetCurrentDim.append(combo_start)
            self.grid.addWidget(combo_start, dim + 1, 2, 1, 1)

            rangetxt = [str(x) for x in range(self.originalRanges[dim])]
            combo_end = QComboBox()
            combo_end.addItems(rangetxt)
            combo_end.setCurrentIndex(self.originalRanges[dim] - 1)
            selectionWidgetCurrentDim.append(combo_end)
            #self.grid.addWidget(combo_end, dim + 1, 3, 1, 1)

            button_left = QToolButton()
            button_left.setArrowType(QtCore.Qt.LeftArrow)
            selectionWidgetCurrentDim.append(button_left)
            self.grid.addWidget(button_left, dim + 1, 3, 1, 1)

            button_right = QToolButton()
            button_right.setArrowType(QtCore.Qt.RightArrow)
            selectionWidgetCurrentDim.append(button_right)
            self.grid.addWidget(button_right, dim + 1, 4, 1, 1)


            # check_firstonly = QCheckBox("first only")
            # el = 'single_trace_checkbox'
            # check_firstonly.setChecked(True)
            # check_firstonly.stateChanged.connect(lambda:self.call_selection_update(dim, el))
            # selectionWidgetCurrentDim.append(check_firstonly)
            # self.grid.addWidget(check_firstonly, dim + 1, 3, 1, 1)

            self.selectionWidget.append(selectionWidgetCurrentDim)

        # Last line of the widget
        # Buttons for plotting
        selectionWidgetCurrentDim = []
        self.btn_Plot1D = QPushButton("Plot 1D")
        self.btn_Plot1D.clicked.connect(self.call_Plot1D)
        self.grid.addWidget(self.btn_Plot1D, len(self.originalRanges) + 2, 0, 1, 1)
        selectionWidgetCurrentDim.append(self.btn_Plot1D)

        self.check_AutoUpdate = QCheckBox("auto update")
        self.grid.addWidget(self.check_AutoUpdate, len(self.originalRanges) + 2, 1, 1, 1)
        selectionWidgetCurrentDim.append(self.check_AutoUpdate)
        self.selectionWidget.append(selectionWidgetCurrentDim)

        self.FLAG_initialized = True
        self.setLayout(self.grid)

    def call_selection_update(self):
        element = self.sender().element
        dim = self.sender().dim
        # wait for XP loaded and widget initialized
        # if (self.originalRanges[0]) != 0 and len(self.selectionWidget) == len():
        if self.FLAG_initialized:
            # Checkbox first
            # Then, their states are checked to enable or disable some widgets
            # Only one can be unchecked
            if element == 'single_trace_checkbox':
                if not self.selectionWidget[dim + 1][1].isChecked():
                    for i in range(len(self.originalRanges)):
                        if i != dim:
                            self.selectionWidget[i + 1][1].setChecked(True)
            for i in range(len(self.originalRanges)):
                if self.selectionWidget[i + 1][1].isChecked():
                    self.grid.removeWidget(self.selectionWidget[i + 1][3])
                    self.selectionWidget[i + 1][3].setVisible(False)

                    self.grid.addWidget(self.selectionWidget[i + 1][4], i + 1, 3, 1, 1)
                    self.selectionWidget[i + 1][4].setVisible(True)

                    self.grid.addWidget(self.selectionWidget[i + 1][5], i + 1, 4, 1, 1)
                    self.selectionWidget[i + 1][5].setVisible(True)

                else:
                    self.grid.removeWidget(self.selectionWidget[i + 1][4])
                    self.selectionWidget[i + 1][4].setVisible(False)

                    self.grid.removeWidget(self.selectionWidget[i + 1][5])
                    self.selectionWidget[i + 1][5].setVisible(False)

                    self.grid.addWidget(self.selectionWidget[i + 1][3], i + 1, 3, 1, 2)
                    self.selectionWidget[i + 1][3].setVisible(True)

    def call_Plot1D(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.plot(self.XP.ExperimentalData['data'][1,:,0,0,0])
        plt.show()

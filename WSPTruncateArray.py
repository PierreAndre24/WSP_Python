from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QLabel, QComboBox)

from subGUI_Model import Model

class WSPTruncateArray(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.selectionWidget = []

    def updateLayout(self,originalRanges):

        # If necessary, remove all existing widgets
        if len(self.selectionWidget) > 0:
            flattened  = [val for sublist in self.selectionWidget for val in sublist]
            for w in flattened:
                self.grid.removeWidget(w)

        # put the new widgets
        self.originalRanges = originalRanges
        
        for dim in range(len(self.originalRanges)):
            selectionWidgetCurrentDim = []
            label = QLabel('Dimension ' + str(dim))
            selectionWidgetCurrentDim.append(label)
            self.grid.addWidget(label,dim,0,1,1)

            rangetxt = [str(x) for x in range(self.originalRanges[dim])]
            combo_start = QComboBox()
            combo_start.addItems(rangetxt)
            combo_start.setCurrentIndex(0)
            selectionWidgetCurrentDim.append(combo_start)
            self.grid.addWidget(combo_start,dim,1,1,1)

            rangetxt = [str(x) for x in range(self.originalRanges[dim])]
            combo_end = QComboBox()
            combo_end.addItems(rangetxt)
            combo_end.setCurrentIndex(-1)
            selectionWidgetCurrentDim.append(combo_end)
            self.grid.addWidget(combo_end,dim,2,1,1)

            self.selectionWidget.append(selectionWidgetCurrentDim)

        self.setLayout(self.grid)

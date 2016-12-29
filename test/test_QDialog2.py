import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                        QAction, QFileDialog, QInputDialog, QFormLayout,
                        QLineEdit)

class inputdialogdemo(QWidget):
    def __init__(self, parent = None):
        super(inputdialogdemo, self).__init__(parent)

        layout = QFormLayout()

        items = ("C", "C++", "Java", "Python")
        self.btn = QPushButton("Choose from list")
        self.btn.clicked.connect(self.getItem)
        self.le = QLineEdit()
        layout.addRow(self.btn,self.le)

        self.setLayout(layout)
        self.setWindowTitle("Input Dialog demo")



    def getItem(self):
        items = ("C", "C++", "Java", "Python")

        item, ok = QInputDialog.getItem(self, "select input dialog",
            "list of languages", items, 0, False)

        if ok and item:
            self.le.setText(item)

    def gettext(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')

        if ok:
            self.le1.setText(str(text))

    def getint(self):
        num,ok = QInputDialog.getInt(self,"integer input dualog","enter a number")

        if ok:
            self.le2.setText(str(num))

    def getfile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, ok = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        print type(filename)
        if ok:
            self.le3.setText(filename)

def main():
    app = QApplication(sys.argv)
    ex = inputdialogdemo()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

from PyQt5.QtWidgets import QApplication, QStackedWidget,QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
import sys

class TitleWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/title_window.ui", self)

        self.btn_play.clicked.connect(self.clickedPlay)

    def clickedPlay(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def toQckSolv(self):
        if self.check_quk_solv.isChecked():
            pass


app = QApplication([])
widget = QStackedWidget()

title_window = TitleWindow()

widget.addWidget(title_window)

# StackedWidget Configurations
#size
widget.setFixedHeight(475)
widget.setFixedWidth(400)

#Title
widget.setWindowTitle("Sudoku Solver")
    
#Set Icon
widget.setWindowIcon(QIcon("img/sudoku.png"))

#Set backdrop
img = QImage("img/backdrop_main.png")
palette = QPalette()
palette.setBrush(QPalette.Window, QBrush(img))
widget.setPalette(palette)

#display
widget.show()
sys.exit(app.exec_())

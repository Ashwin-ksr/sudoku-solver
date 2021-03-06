from PyQt5.QtWidgets import QApplication, QStackedWidget,QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QFont
import sys

class TitleWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/title_window.ui", self)

        self.btn_play.clicked.connect(self.clickedPlay)

    def clickedPlay(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def toQckSolv(self):
        if self.checkBox_quk_solv.isChecked():
            return True
        return False


class DiffWindow(QWidget):
    def __init__(self):
        super(DiffWindow, self).__init__()
        uic.loadUi("ui/diff_window.ui", self)

        #selected difficulty
        self.btn_back.clicked.connect(self.clickedBack)
        self.btn_easy.clicked.connect(self.clickedEasy)
        self.btn_medium.clicked.connect(self.clickedMedium)
        self.btn_hard.clicked.connect(self.clickedHard)
        self.btn_expert.clicked.connect(self.clickedExpert)
        self.btn_cstm.clicked.connect(self.clickedCstm)

    #Actions
    def clickedBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
    
    def clickedEasy(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        board_window.parse_brd("brds/easy.txt")
        
    
    def clickedMedium(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        board_window.parse_brd("brds/medium.txt")

    def clickedHard(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        board_window.parse_brd("brds/hard.txt")

    def clickedExpert(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        board_window.parse_brd("brds/expert.txt")
    
    def clickedCstm(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        board_window.parse_brd("brds/custom.txt")


class BoardWindow(QWidget):
    def __init__(self):
        super(BoardWindow, self).__init__()
        uic.loadUi("ui/board_window.ui", self)
        self.brd = []

        #button clicked
        self.btn_back.clicked.connect(self.clickedBack)
        self.btn_solve.clicked.connect(self.clickedSolve)
        self.btn_clr.clicked.connect(self.clickedClear)
    
    def parse_brd(self, f_name):
        self.brd = []
        try:
            with open(f_name, 'r') as brd_file:
                lines = brd_file.readlines(150)
                if len(lines) == 9:
                    for line in lines:
                        temp = line.rstrip('\n').rsplit(" ")
                        if len(temp) == 9:
                            temp = [int(x) for x in temp]
                            self.brd.append(temp)
                        else:
                            print("Unsupported file")
                else:
                    print("Unspported file")
            self.fill_brd(self.brd)
        except FileNotFoundError:
            #print("Board file is not found")
            pass
    
    def parse_crnt_brd(self):
        crnt_brd =[]
        for row in range(0, 9):
            temp = []
            for col in range(0, 9):
                if getattr(self, "lineEdit_"+ str(row) + "x" + str(col)).text() != '':
                    temp.append(int(getattr(self, "lineEdit_"+ str(row) + "x" + str(col)).text()))
                else:
                    temp.append(0)
            crnt_brd.append(temp)
        return crnt_brd

    def fill_brd(self, board):
        palette = QPalette()
        try:
            for row in range(0, 9):
                for col in range(0, 9):
                    if board[row][col] != 0:
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setText(str(board[row][col]))
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setAlignment(Qt.AlignCenter)
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setFont(QFont("Courier", weight= QtGui.QFont.Bold))
                        palette.setColor(QPalette.Text, Qt.black)
                        getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setPalette(palette)
                        getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setReadOnly(True)

                    else:
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setText('')
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setAlignment(Qt.AlignCenter)
                        getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setFont(QFont("Courier", weight= QtGui.QFont.Normal))
                        palette.setColor(QPalette.Text, Qt.red)
                        getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setPalette(palette)
                        getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setReadOnly(False)
        except TypeError:
            print("No possible solution is found")

    def clr_brd(self):
        palette = QPalette()
        for row in range(0, 9):
            for col in range(0, 9):
                getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setText('')
                getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setAlignment(Qt.AlignCenter)
                getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setFont(QFont("Courier", weight= QtGui.QFont.Normal))
                palette.setColor(QPalette.Text, Qt.black)
                getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setPalette(palette)
                getattr(self, "lineEdit_"+str(row)+"x"+str(col)).setReadOnly(False)
    
    def find_empty(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if getattr(self, "lineEdit_" + str(row) + "x" + str(col)).text() == '':
                    return (row, col)
        return None
    
    def isValid(self, num, pos): 
        #checks horizontally
        for col in range(0, 9):
            if getattr(self, "lineEdit_" + str(pos[0]) + "x" + str(col)).text() == str(num) and col != pos[1]:
                return False
        
        #checks vertically
        for row in range(0, 9):
            if getattr(self, "lineEdit_" + str(row) + "x" + str(pos[1])).text() == str(num) and row != pos[0]:
                return False
        
        Xbox = pos[1] // 3
        YBox = pos[0] // 3
        #check nonet
        for row in range(YBox*3, YBox*3 + 3):
            for col in range(Xbox*3, Xbox*3 + 3):
                if getattr(self, "lineEdit_" + str(row) + "x" + str(col)).text() == str(num) and (row, col) != pos:
                    return False
        
        #if conditions are met then the number is valid
        return True
    
    def solve(self):
        empty_space = self.find_empty()
        if not empty_space:
            return True
        else:
            row, col = empty_space
        
        for i in range(1, 10):
            if self.isValid(i, (row, col)):
                getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setText(str(i))
                if self.solve():
                    return True
                getattr(self, "lineEdit_" + str(row) + "x" + str(col)).setText('')
        
        return False
                    
    def clickedBack(self):
        self.clr_brd()
        widget.setCurrentIndex(widget.currentIndex()-1)

    def clickedSolve(self):
        if title_window.toQckSolv():
            crnt_brd = self.parse_crnt_brd()
            self.fill_brd(quick_solve.quickSol(crnt_brd))
            self.parse_crnt_brd()
        else:
            self.solve()

    def clickedClear(self):
        self.clr_brd()


class QucikSolve():
    def __init__(self):
        pass

    def find_empty(self, brd):
        for i, row in enumerate(brd):
            for j, ele in enumerate(row):
                if ele == 0:
                    return (i, j) 
        return None
    
    def isValid(self, brd, num, pos):
        #check horizontally
        for col in range(9):
            if brd[pos[0]][col] == num and  pos[1] != col:
                return False 

        #check vertically
        for row in range(9):
            if brd[row][pos[1]] == num and pos[0] != row :
                return False

        #check nonet
        for row in range((pos[0]//3)*3, (pos[0]//3)*3 + 3):
            for col in range((pos[1]//3)*3, (pos[1]//3)*3 + 3):
                if brd[row][col] == num and (row, col) != pos:
                    return False

        return True

    def solver(self, brd):
        empty_space = self.find_empty(brd)
        if not empty_space:
            return True
        else: 
            row, col = empty_space

        for i in range(1, 10):
            if self.isValid(brd, i, (row, col)):
                brd[row][col] = i

                if self.solver(brd):
                    return brd

                brd[row][col] = 0

        return False
    
    def quickSol(self, board):
        self.brd = self.solver(board)
        return self.brd


app = QApplication([])
widget = QStackedWidget()

title_window = TitleWindow()
diff_window = DiffWindow()
board_window = BoardWindow()
quick_solve = QucikSolve()

#Adding the widgets to Stack
widget.addWidget(title_window)
widget.addWidget(diff_window)
widget.addWidget(board_window)

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

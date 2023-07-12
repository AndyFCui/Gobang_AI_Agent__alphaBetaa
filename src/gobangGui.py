"""
Gobang GUI
CS5150 Final project
@author: Andy(Xiang-Yu) Cui
"""

import warnings
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound
from gobangBoard import ChessBoard
from gobangAgent import Search

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set the GUI windows
WIDTH = 540
HEIGHT = 540
MARGIN = 22
GRID = (WIDTH - 2 * MARGIN) / (15 - 1)
PIECE = 34
EMPTY = 0
BLACK = 1
WHITE = 2


# Execute AI action
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)

    # Constructor of AI
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board

    # Override run()
    def run(self):
        self.ai = Search()
        self.ai.board = self.board
        score, x, y = self.ai.search(2, 2)
        self.finishSignal.emit(x, y)


# Re-define Label class
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()


class GoBang(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.chessboard = ChessBoard()
        # Set board background
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('../res/img/chessboard.jpg')))
        self.setPalette(palette1)
        self.setCursor(Qt.PointingHandCursor)  # Set mouse hand
        # load wav sound for games
        self.sound_piece = QSound("../res/sound/move.wav")
        self.sound_win = QSound("../res/sound/win.wav")
        self.sound_defeated = QSound("../res/sound/defeated.wav")
        self.resize(WIDTH, HEIGHT)  # size 540*540
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        # Set windows name & Icon
        self.setWindowTitle("GoBang-AlphaBeta-Graph")
        self.setWindowIcon(QIcon('../res/img/black.png'))

        # load chess
        self.black = QPixmap('../res/img/black.png')
        self.white = QPixmap('../res/img/white.png')

        # Set the sequence
        self.piece_now = BLACK  # Black first
        self.my_turn = True  # player first
        self.step = 0  # step init to 0
        self.x, self.y = 1000, 1000
        self.mouse_point = LaBel(self)  # Change mouse icon to chess png
        self.mouse_point.setScaledContents(True)
        self.mouse_point.setPixmap(self.black)  # load black chess
        self.mouse_point.setGeometry(270, 270, PIECE, PIECE)
        self.pieces = [LaBel(self) for i in range(225)]  # ready for draw chess
        for piece in self.pieces:
            piece.setVisible(True)
            piece.setScaledContents(True)

        # Mouse always on top layer
        self.mouse_point.raise_()
        self.ai_down = True  # Mark AI down chess and lock mousePressEvent

        self.setMouseTracking(True)
        self.show()

    # Mark chess put position
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    # black chess move with mouse
    def mouseMoveEvent(self, e):
        # self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
        self.mouse_point.move(e.x() - 16, e.y() - 16)

    # Implement player put chess
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.ai_down == True:
            x, y = e.x(), e.y()  # Mouse position (x, y)
            i, j = self.coordinate_transform_pixel2map(x, y)  # Board position(x, y)
            if not i is None and not j is None:  # check boundary
                if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY:  # put the chess to null
                    self.draw(i, j)
                    self.ai_down = False
                    board = self.chessboard.board()
                    self.AI = AI(board)
                    self.AI.finishSignal.connect(self.AI_draw)
                    self.AI.start()

    def AI_draw(self, i, j):
        if self.step != 0:
            self.draw(i, j)
            self.x, self.y = self.coordinate_transform_map2pixel(i, j)
        self.ai_down = True
        self.update()

    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if self.piece_now == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # put black chess
            self.piece_now = WHITE
            self.chessboard.draw_xy(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # put white chess
            self.piece_now = BLACK
            self.chessboard.draw_xy(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # Draw chess
        self.sound_piece.play()  # play sound put chess
        self.step += 1

        winner = self.chessboard.anyone_win(i, j)  # Check who win the game
        if winner != EMPTY:
            self.mouse_point.clear()
            self.gameover(winner)

    def drawLines(self, qp):  # Show AI chess position
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

    # From chessMap to UI Pos
    def coordinate_transform_map2pixel(self, i, j):
        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    # From UI to chessMap Pos
    def coordinate_transform_pixel2map(self, x, y):
        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))
        # check MAGIN boundary
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            return None, None
        else:
            return i, j
    """
    Set when game over will get QMessagebox
    
    """
    #
    def gameover(self, winner):
        # Win
        if winner == BLACK:
            self.sound_win.play()
            reply = QMessageBox.question(self, 'You Win!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Fail
        else:
            self.sound_defeated.play()
            reply = QMessageBox.question(self, 'You Lost!', 'Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # Yes，reset
        if reply == QMessageBox.Yes:
            self.piece_now = BLACK
            self.mouse_point.setPixmap(self.black)
            self.step = 0
            for piece in self.pieces:
                piece.clear()
            self.chessboard.reset()
            self.update()
        # No, exit
        else:
            self.close()




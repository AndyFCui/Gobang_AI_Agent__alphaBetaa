"""
Main driver: start game
CS5150 Final project
@author: Andy(Xiang-Yu) Cui
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gobangGui import GoBang


def main():
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

"""
CS5150 Final project
Gobang game board.
@author: Andy(Xiang-Yu) Cui
"""

# init chess style
EMPTY = 0
BLACK = 1
WHITE = 2


"""
Define the chess board class, and draw the game board.
"""
class ChessBoard(object):
    def __init__(self):
        self.__board = [[EMPTY for n in range(15)] for m in range(15)]
        self.__dir = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        #                (L      R)      (U       D)     (LD     RU)      (LU     RD)

    def board(self):
        return self.__board

    # Get put chess pos status
    def draw_xy(self, x, y, state):
        self.__board[x][y] = state

    # Get appointed put chess pos status
    def get_xy_on_logic_state(self, x, y):
        return self.__board[x][y]

    """"
    Get the appointed pu chess pos.
    :param point the chess
    :param the direction of point
    """
    @staticmethod
    def get_next_xy(point, direction):
        x = point[0] + direction[0]
        y = point[1] + direction[1]
        if x < 0 or x >= 15 or y < 0 or y >= 15:
            return False
        else:
            return x, y

    """
    Get the appointed direction status.
    :param self board
    :param point the point
    :param direction the direction of point
    """
    def get_xy_on_direction_state(self, point, direction):
        if point is not False:
            xy = self.get_next_xy(point, direction)
            if xy is not False:
                x, y = xy
                return self.__board[x][y]
        return False

    def anyone_win(self, x, y):
        state = self.get_xy_on_logic_state(x, y)
        for directions in self.__dir:  # Check 4 direction the direction of point five chess
            count = 1
            for direction in directions:  # check put chess both side
                point = (x, y)
                while True:
                    if self.get_xy_on_direction_state(point, direction) == state:
                        count += 1
                        point = self.get_next_xy(point, direction)
                    else:
                        break
            if count >= 5:
                return state
        return EMPTY

    def reset(self):  # Reset
        self.__board = [[EMPTY for n in range(15)] for m in range(15)]

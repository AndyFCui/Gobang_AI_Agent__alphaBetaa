"""
CS5150 Final project
The Go-bang chess AI agent.
@author: Andy(Xiang-Yu Cui)
"""

"""
evaluation:get the return profit value of AI turn
10 basic chess piece shape:
1. 冲二(STWO): If you add one more son to your side, only one point can become one of two.
                
2. 冲三(STHREE): If you add one more son to your side, only one point can make two of three.

3. 冲四(SFOUR): Means If you add one more son to your side, 
                only one point can be made into four of five. 
                Including continuous punch four and jump punch four, 
                jump punch four is also known as "embedded five"
                
4. 活二(TWO): Add one son to your side to form two of three living three.

5. 活三(THREE): Add one more son to your side, and you can form a three of a living four.

6. 活四(FOUR): Add one son to your side, and there are two points that can be a single four of five.

7. 活五(Five): Five chess pieces of the same color that are closely connected on a positive or negative line.

8. 双四(DFOUR): When a pawn falls, 2 rushing fours are formed at the same time.

9. 四三(FOURT): When rushing to the fourth, a live three is formed, and the next move is a live four to win.

10. 双三(DTHREE): When a pawn falls, 2 live threes are formed at the same time.
"""


class Evaluation(object):
    def __init__(self):
        self.POS = []
        for i in range(15):
            row = [(7 - max(abs(i - 7), abs(j - 7))) for j in range(15)]
            self.POS.append(tuple(row))
        self.POS = tuple(self.POS)
        self.STWO = 1  # 冲二
        self.STHREE = 2  # 冲三
        self.SFOUR = 3  # 冲四
        self.TWO = 4  # 活二
        self.THREE = 5  # 活三
        self.FOUR = 6  # 活四
        self.FIVE = 7  # 活五
        self.DFOUR = 8  # 双四
        self.FOURT = 9  # 四三
        self.DTHREE = 10  # 双三
        self.ANALYSED = 255  # analysed
        self.next = 0  # None analysis
        self.result = [0 for i in range(30)]  # line data result
        self.line = [0 for i in range(30)]  # line data
        self.record = []  # Analysis all board [row][col][direction]
        for i in range(15):
            self.record.append([])
            self.record[i] = []
            for j in range(15):
                self.record[i].append([0, 0, 0, 0])
        self.count = []  # different kind chess frame count [black/white][mode]
        for i in range(3):
            data = [0 for i in range(20)]
            self.count.append(data)
        self.reset()

    # reset data value
    def reset(self):
        next = self.next
        count = self.count
        for i in range(15):
            line = self.record[i]
            for j in range(15):
                line[j][0] = next
                line[j][1] = next
                line[j][2] = next
                line[j][3] = next
        for i in range(20):
            count[0][i] = 0
            count[1][i] = 0
            count[2][i] = 0
        return 0

    # Four direction（horizon，vertical，left corner，right corner）analysis board, and grade.
    def evaluate(self, board, turn):
        score = self.__evaluate(board, turn)
        count = self.count
        if score < -9000:
            stone = turn == 1 and 2 or 1
            for i in range(20):
                if count[stone][i] > 0:
                    score -= i
        elif score > 9000:
            stone = turn == 1 and 2 or 1
            for i in range(20):
                if count[turn][i] > 0:
                    score += i
        return score

    # Four direction（horizon，vertical，left corner，right corner）analysis board, and grade.
    def __evaluate(self, board, turn):
        record, count = self.record, self.count
        next, ANALYSED = self.next, self.ANALYSED
        self.reset()
        for i in range(15):
            boardrow = board[i]
            recordrow = record[i]
            for j in range(15):
                if boardrow[j] != 0:
                    if recordrow[j][0] == next:  # None analysis horizon
                        self.__analysis_horizon(board, i, j)
                    if recordrow[j][1] == next:  # None analysis vertical
                        self.__analysis_vertical(board, i, j)
                    if recordrow[j][2] == next:  # None analysis left corner
                        self.__analysis_left(board, i, j)
                    if recordrow[j][3] == next:  # None analysis right corner
                        self.__analysis_right(board, i, j)

        FIVE, FOUR = self.FIVE, self.FOUR
        THREE, TWO = self.THREE, self.TWO
        SFOUR, STHREE, STWO = self.SFOUR, self.STHREE, self.STWO
        check = {}

        # Calculate<W/B>：number of FIVE, FOUR, THREE, TWO
        for c in (FIVE, FOUR, SFOUR, THREE, STHREE, TWO, STWO):
            check[c] = 1
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    for k in range(4):
                        ch = record[i][j][k]
                        if ch in check:
                            count[stone][ch] += 1

        # If get five then return
        BLACK, WHITE = 1, 2
        if turn == WHITE:  # white
            if count[BLACK][FIVE]:
                return -9999
            if count[WHITE][FIVE]:
                return 9999
        else:  # black
            if count[WHITE][FIVE]:
                return -9999
            if count[BLACK][FIVE]:
                return 9999

        # if two 冲四，then have one 活四
        if count[WHITE][SFOUR] >= 2:
            count[WHITE][FOUR] += 1
        if count[BLACK][SFOUR] >= 2:
            count[BLACK][FOUR] += 1

        # Grade
        wvalue, bvalue, win = 0, 0, 0
        if turn == WHITE:
            if count[WHITE][FOUR] > 0: return 9990
            if count[WHITE][SFOUR] > 0: return 9980
            if count[BLACK][FOUR] > 0: return -9970
            if count[BLACK][SFOUR] and count[BLACK][THREE]:
                return -9960
            if count[WHITE][THREE] and count[BLACK][SFOUR] == 0:
                return 9950
            if count[BLACK][THREE] > 1 and \
                    count[WHITE][SFOUR] == 0 and \
                    count[WHITE][THREE] == 0 and \
                    count[WHITE][STHREE] == 0:
                return -9940
            if count[WHITE][THREE] > 1:
                wvalue += 2000
            elif count[WHITE][THREE]:
                wvalue += 200
            if count[BLACK][THREE] > 1:
                bvalue += 500
            elif count[BLACK][THREE]:
                bvalue += 100
            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]
        else:
            if count[BLACK][FOUR] > 0: return 9990
            if count[BLACK][SFOUR] > 0: return 9980
            if count[WHITE][FOUR] > 0: return -9970
            if count[WHITE][SFOUR] and count[WHITE][THREE]:
                return -9960
            if count[BLACK][THREE] and count[WHITE][SFOUR] == 0:
                return 9950
            if count[WHITE][THREE] > 1 and \
                    count[BLACK][SFOUR] == 0 and \
                    count[BLACK][THREE] == 0 and \
                    count[BLACK][STHREE] == 0:
                return -9940
            if count[BLACK][THREE] > 1:
                bvalue += 2000
            elif count[BLACK][THREE]:
                bvalue += 200
            if count[WHITE][THREE] > 1:
                wvalue += 500
            elif count[WHITE][THREE]:
                wvalue += 100
            if count[BLACK][STHREE]:
                bvalue += count[BLACK][STHREE] * 10
            if count[WHITE][STHREE]:
                wvalue += count[WHITE][STHREE] * 10
            if count[BLACK][TWO]:
                bvalue += count[BLACK][TWO] * 4
            if count[WHITE][TWO]:
                wvalue += count[WHITE][TWO] * 4
            if count[BLACK][STWO]:
                bvalue += count[BLACK][STWO]
            if count[WHITE][STWO]:
                wvalue += count[WHITE][STWO]

        # Set pos h value, center is 7, out one (-1), boundary is 0
        wc, bc = 0, 0
        for i in range(15):
            for j in range(15):
                stone = board[i][j]
                if stone != 0:
                    if stone == WHITE:
                        wc += self.POS[i][j]
                    else:
                        bc += self.POS[i][j]
        wvalue += wc
        bvalue += bc

        if turn == WHITE:
            return wvalue - bvalue

        return bvalue - wvalue

    # Analysis horizon
    def __analysis_horizon(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        next = self.next
        for x in range(15):
            line[x] = board[i][x]
        self.analysis_line(line, result, 15, j)
        for x in range(15):
            if result[x] != next:
                record[i][x][0] = result[x]
        return record[i][j][0]

    # Analysis vertical
    def __analysis_vertical(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        next = self.next
        for x in range(15):
            line[x] = board[x][j]
        self.analysis_line(line, result, 15, i)
        for x in range(15):
            if result[x] != next:
                record[x][j][1] = result[x]
        return record[i][j][1]

    # Check left corner
    def __analysis_left(self, board, i, j):
        line, result, record = self.line, self.result, self.record
        next = self.next
        if i < j:
            x, y = j - i, 0
        else:
            x, y = 0, i - j
        k = 0
        while k < 15:
            if x + k > 14 or y + k > 14:
                break
            line[k] = board[y + k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != next:
                record[y + s][x + s][2] = result[s]
        return record[i][j][2]

    # Check right corner
    def __analysis_right(self, board, i, j):
        line, result = self.line, self.result
        record = self.record
        next = self.next
        if 14 - i < j:
            x, y, realnum = j - 14 + i, 14, 14 - i
        else:
            x, y, realnum = 0, i + j, j
        k = 0
        while k < 15:
            if x + k > 14 or y - k < 0:
                break
            line[k] = board[y - k][x + k]
            k += 1
        self.analysis_line(line, result, k, j - x)
        for s in range(k):
            if result[s] != next:
                record[y - s][x + s][3] = result[s]
        return record[i][j][3]

    # 分析一条线：五四三二等棋型
    def analysis_line(self, line, record, num, pos):
        next, ANALYSED = self.next, self.ANALYSED
        THREE, STHREE = self.THREE, self.STHREE
        FOUR, SFOUR = self.FOUR, self.SFOUR
        while len(line) < 30: line.append(0xf)
        while len(record) < 30: record.append(next)
        for i in range(num, 30):
            line[i] = 0xf
        for i in range(num):
            record[i] = next
        if num < 5:
            for i in range(num):
                record[i] = ANALYSED
            return 0
        stone = line[pos]
        inverse = (0, 2, 1)[stone]
        num -= 1
        xl = pos
        xr = pos
        while xl > 0:  # check left boundary
            if line[xl - 1] != stone: break
            xl -= 1
        while xr < num:  # check right boundary
            if line[xr + 1] != stone: break
            xr += 1
        left_range = xl
        right_range = xr
        while left_range > 0:  # check left range
            if line[left_range - 1] == inverse: break
            left_range -= 1
        while right_range < num:  # check right range
            if line[right_range + 1] == inverse: break
            right_range += 1

        # if right range lower than 5，return
        if right_range - left_range < 4:
            for k in range(left_range, right_range + 1):
                record[k] = ANALYSED
            return 0

        # Mark analysed
        for k in range(xl, xr + 1):
            record[k] = ANALYSED

        srange = xr - xl

        # if 5 in row
        if srange >= 4:
            record[pos] = self.FIVE
            return self.FIVE

        # if 4 in row
        if srange == 3:
            leftfour = False  # Check left space
            if xl > 0:
                if line[xl - 1] == 0:  # 活四
                    leftfour = True
            if xr < num:
                if line[xr + 1] == 0:
                    if leftfour:
                        record[pos] = self.FOUR  # 活四
                    else:
                        record[pos] = self.SFOUR  # 冲四
                else:
                    if leftfour:
                        record[pos] = self.SFOUR  # 冲四
            else:
                if leftfour:
                    record[pos] = self.SFOUR  # 冲四
            return record[pos]

        # If get Triple
        if srange == 2:  # Triple
            left3 = False  # check space left
            if xl > 0:
                if line[xl - 1] == 0:  # Left get
                    if xl > 1 and line[xl - 2] == stone:
                        record[xl] = SFOUR
                        record[xl - 2] = ANALYSED
                    else:
                        left3 = True
                elif xr == num or line[xr + 1] != 0:
                    return 0
            if xr < num:
                if line[xr + 1] == 0:  # Right get
                    if xr < num - 1 and line[xr + 2] == stone:
                        record[xr] = SFOUR  # XXX-X Go-Four 冲四
                        record[xr + 2] = ANALYSED
                    elif left3:
                        record[xr] = THREE
                    else:
                        record[xr] = STHREE
                elif record[xl] == SFOUR:
                    return record[xl]
                elif left3:
                    record[pos] = STHREE
            else:
                if record[xl] == SFOUR:
                    return record[xl]
                if left3:
                    record[pos] = STHREE
            return record[pos]

            # Get double
        if srange == 1:  # Double
            left2 = False
            if xl > 2:
                if line[xl - 1] == 0:  # Left get
                    if line[xl - 2] == stone:
                        if line[xl - 3] == stone:
                            record[xl - 3] = ANALYSED
                            record[xl - 2] = ANALYSED
                            record[xl] = SFOUR
                        elif line[xl - 3] == 0:
                            record[xl - 2] = ANALYSED
                            record[xl] = STHREE
                    else:
                        left2 = True
            if xr < num:
                if line[xr + 1] == 0:  # 左边有气
                    if xr < num - 2 and line[xr + 2] == stone:
                        if line[xr + 3] == stone:
                            record[xr + 3] = ANALYSED
                            record[xr + 2] = ANALYSED
                            record[xr] = SFOUR
                        elif line[xr + 3] == 0:
                            record[xr + 2] = ANALYSED
                            record[xr] = left2 and THREE or STHREE
                    else:
                        if record[xl] == SFOUR:
                            return record[xl]
                        if record[xl] == STHREE:
                            record[xl] = THREE
                            return record[xl]
                        if left2:
                            record[pos] = self.TWO
                        else:
                            record[pos] = self.STWO
                else:
                    if record[xl] == SFOUR:
                        return record[xl]
                    if left2:
                        record[pos] = self.STWO
            return record[pos]
        return 0


# ----------------------------------------------------------------------


# DFS: Game Tree Search(Use a little bit MCTS logic)
# ----------------------------------------------------------------------
class Search(object):
    # init game
    def __init__(self):
        self.evaluator = Evaluation()
        self.board = [[0 for n in range(15)] for i in range(15)]
        self.game_over = 0
        self.overvalue = 0
        self.max_depth = 3

    # Create current move method
    def root_move(self, turn):
        moves = []
        board = self.board
        position = self.evaluator.POS
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    score = position[i][j]
                    moves.append((score, i, j))
        moves.sort()
        moves.reverse()
        return moves

    # DFS：Return best score
    def __search(self, turn, depth, alpha, beta):

        # depth lower than 0, return
        if depth <= 0:
            score = self.evaluator.evaluate(self.board, turn)
            return score

        # If game over, then return
        score = self.evaluator.evaluate(self.board, turn)
        if abs(score) >= 9999 and depth < self.max_depth:
            return score

        # Create new move method
        moves = self.root_move(turn)
        best_move = None

        for score, row, col in moves:

            # Mark move method to board
            self.board[row][col] = turn

            # Calculate next turn
            nturn = turn == 1 and 2 or 1

            # DFS score
            score = -self.__search(nturn, depth - 1, -beta, -alpha)

            # Delete current move
            self.board[row][col] = 0

            # alpha/beta pruning
            if score > alpha:
                alpha = score
                best_move = (row, col)
                if alpha >= beta:
                    break

        # if find the best move store it
        if depth == self.max_depth and best_move:
            self.best_move = best_move

        # return the best move
        return alpha

    # Search：(turn=1/2)，(depth)
    def search(self, turn, depth=3):
        self.max_depth = depth
        self.best_move = None
        score = self.__search(turn, depth, -0x7fffffff, 0x7fffffff)
        if abs(score) > 8000:
            self.max_depth = depth
            score = self.__search(turn, 1, -0x7fffffff, 0x7fffffff)
        row, col = self.best_move
        return score, row, col

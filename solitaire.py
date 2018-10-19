import itertools
import copy
import search
import utils
from search import *
from utils import *

# TAI content
def c_peg ():
    return "O"

def c_empty ():
    return "_"

def c_blocked ():
    return "X"

def is_empty (e):
    return e == c_empty()

def is_peg (e):
    return e == c_peg()
    
def is_blocked (e):
    return e == c_blocked()


# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)

def pos_l (pos):
    return pos[0]

def pos_c (pos):
    return pos[1]


# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]

def move_initial (move):
    return move[0]

def move_final (move):
    return move[1]


# TAI board
def check_conditions_left_empty(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_peg(board[line][col-2]) and is_peg(board[line][col-1]):
        newMove = make_move(make_pos(line, col-2), make_pos(line, col))
        return newMove

    return

def check_conditions_right_empty(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_peg(board[line][col+2]) and is_peg(board[line][col+1]):
        newMove = make_move(make_pos(line, col+2), make_pos(line, col))
        return newMove

    return

def check_conditions_top_empty(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_peg(board[line-2][col]) and is_peg(board[line-1][col]):
        newMove = make_move(make_pos(line-2, col), make_pos(line, col))
        return newMove

    return

def check_conditions_bottom_empty(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_peg(board[line+2][col]) and is_peg(board[line+1][col]):
        newMove = make_move(make_pos(line+2, col), make_pos(line, col))
        return newMove

    return


def check_conditions_left_peg(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_empty(board[line][col-2]) and is_peg(board[line][col-1]):
        newMove = make_move(make_pos(line, col), make_pos(line, col-2))
        return newMove

    return

def check_conditions_right_peg(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_empty(board[line][col+2]) and is_peg(board[line][col+1]):
        newMove = make_move(make_pos(line, col), make_pos(line, col+2))
        return newMove

    return

def check_conditions_top_peg(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_empty(board[line-2][col]) and is_peg(board[line-1][col]):
        newMove = make_move(make_pos(line, col), make_pos(line-2, col))
        return newMove

    return

def check_conditions_bottom_peg(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)

    if is_empty(board[line+2][col]) and is_peg(board[line+1][col]):
        newMove = make_move(make_pos(line, col), make_pos(line+2, col))
        return newMove

    return


def check_move_empty(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)
    moves = []
    
    # general case: we check for moves coming from every direction
    # probably will need to check if there are at least 3 col or 3 lines
    if line not in (0, 1, len(board)-1, len(board)-2) and col not in (0, 1, len(board[line])-1, len(board[line])-2):

        moves.append(check_conditions_left_empty(board, pos))
        moves.append(check_conditions_right_empty(board, pos))
        moves.append(check_conditions_top_empty(board, pos))
        moves.append(check_conditions_bottom_empty(board, pos))
    
    # we don't check for moves coming from the top
    # probably will need to check if there are at least 3 col or 3 lines
    elif line in (0,1):
        moves.append(check_conditions_bottom_empty(board, pos))
        if col in (0, 1):
            moves.append(check_conditions_right_empty(board, pos))
        elif col in (len(board[line])-1, len(board[line])-2):
            moves.append(check_conditions_left_empty(board, pos))
        else:
            moves.append(check_conditions_right_empty(board, pos))
            moves.append(check_conditions_left_empty(board, pos))

    # we don't need to check for moves coming from the bottom
    # probably will need to check if there are at least 3 col or 3 lines
    else:
        moves.append(check_conditions_top_empty(board, pos))
        if col in (0, 1):
            moves.append(check_conditions_right_empty(board, pos))
        elif col in (len(board[line])-1, len(board[line])-2):
            moves.append(check_conditions_left_empty(board, pos))
        else:
            moves.append(check_conditions_right_empty(board, pos))
            moves.append(check_conditions_left_empty(board, pos))

    return removeall(None, moves)

def check_move_peg(board, pos):
    line = pos_l(pos)
    col = pos_c(pos)
    moves = []

    # general case: we check for possible moves in every direction
    # probably will need to check if there are at least 3 col or 3 lines
    if line not in (0, 1, len(board)-1, len(board)-2) and col not in (0, 1, len(board[line])-1, len(board[line])-2):

        moves.append(check_conditions_left_peg(board, pos))
        moves.append(check_conditions_right_peg(board, pos))
        moves.append(check_conditions_top_peg(board, pos))
        moves.append(check_conditions_bottom_peg(board, pos))

    # we don't check for moves to the top
    # probably will need to check if there are at least 3 col or 3 lines
    elif line in (0,1):
        moves.append(check_conditions_bottom_peg(board, pos))
        if col in (0, 1):
            moves.append(check_conditions_right_peg(board, pos))
        elif col in (len(board[line])-1, len(board[line])-2):
            moves.append(check_conditions_left_peg(board, pos))
        else:
            moves.append(check_conditions_right_peg(board, pos))
            moves.append(check_conditions_left_peg(board, pos))

    # we don't need to check for moves to the bottom
    # probably will need to check if there are at least 3 col or 3 lines
    else:
        moves.append(check_conditions_top_peg(board, pos))
        if col in (0, 1):
            moves.append(check_conditions_right_peg(board, pos))
        elif col in (len(board[line])-1, len(board[line])-2):
            moves.append(check_conditions_left_peg(board, pos))
        else:
            moves.append(check_conditions_right_peg(board, pos))
            moves.append(check_conditions_left_peg(board, pos))
    
    return removeall(None, moves)


def calcPos(initial, final):
    line = (pos_l(initial) + pos_l(final)) // 2
    col = (pos_c(initial) + pos_c(final)) // 2 
    middlePos = make_pos(line, col)
    return middlePos


def board_moves(board): 
    merged = list(itertools.chain.from_iterable(board))
    mostCommonItem = mode(merged)
    movesList=[]

    # when there are more peg than empty, finds the empty ones and 
    # checks if it is possible to make a move there
    if is_peg(mostCommonItem):
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if is_empty(board[row][col]):
                    pos = make_pos(row, col)
                    for move in check_move_empty(board, pos):
                        movesList.append(move)

    # when there are more empty than peg, finds the peg ones and 
    # checks if it is possible to make a move from there
    elif is_empty(mostCommonItem):
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if is_peg(board[row][col]):
                    pos = make_pos(row, col)
                    for move in check_move_peg(board, pos):
                        movesList.append(move)

    return movesList
                    
def board_perform_move(board, move):
    finalBoard = copy.deepcopy(board)
    initialPos = move_initial(move)
    finalPos = move_final(move)
    middlePos = calcPos(initialPos, finalPos)

    finalBoard[pos_l(initialPos)][pos_c(initialPos)] = c_empty()
    finalBoard[pos_l(middlePos)][pos_c(middlePos)] = c_empty()
    finalBoard[pos_l(finalPos)][pos_c(finalPos)] = c_peg()

    return finalBoard


#TAI sol_state
class sol_state:
    def __init__(self, board):
        self.board = board
    
    def __lt__():
        pass

#TAI solitaire
class solitaire(Problem):
    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):
        pass
    
    def result(self, state, action):
        pass
    
    def path_cost(self, c, s, a, s2):
        return c+1
    
    def goal_test(self, state):
        pass

    def h(self, node):
        pass

def main():
    board = [["O","O","O","X"],["O","O","O","O"],["O","_","O","O"],["O","O","O","O"]]
    print_table(board)
    moves = board_moves(board)
    print(moves)
    newBoard = board_perform_move(board, moves[0])
    print_table(newBoard)

if __name__ == "__main__":
    #main(sys.argv[1])
    main()
    sys.exit(0)
"""
Tic Tac Toe Player
"""

import math
import copy
import time

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in board:
        for j in i:
            if j is not EMPTY:
                count += 1
    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    i = 0
    for row in board:
        j = 0
        for cell in row:
            if cell is EMPTY:
                action = (i,j)
                actions.add(action)
            j += 1
        i += 1
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board)
    newBoard = copy.deepcopy(board)
    if newBoard[action[0]][action[1]] is EMPTY:
        newBoard[action[0]][action[1]] = p
    else:
        raise ValueError("The action is not valid!")
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        test = [row[0], row[1], row[2]]
        if test == [O, O, O]:
            return O
        elif test == [X, X, X]:
            return X

    # Check columns
    for j in range(3):
        test = []
        for row in board:
            test.append(row[j])
            if test == [O, O, O]:
                return O
            elif test == [X, X, X]:
                return X
    
    # Check diagonal
    diagonal1 = [board[0][0],board[1][1],board[2][2]]
    diagonal2 = [board[0][2],board[1][1],board[2][0]]
    if diagonal1 == [O, O, O] or diagonal2 == [O, O, O]:
        return O
    elif diagonal1 == [X, X, X] or diagonal2 == [X, X, X]:
        return X

    return None


def full(board):
    """
    Returns True if the board is full (no EMPTY cells), False otherwise
    """
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None and full(board) is False:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    elif winner(board) is O:
        return -1
    else:
        return 0

# Alpha-beta pruning version
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    X is the Max player and O is the Min player.
    """
    time_start= time.time()
    if terminal(board):
        return None

    if player(board) is X:
        maxV, bestAction = MaxValue(board, None)
    else:
        minV, bestAction = MinValue(board, None)
    time_end = time.time()
    print('AI calculation took...' + str(time_end - time_start))
    return bestAction

    
def MaxValue(board, v_max):
    """
    Returns the max value possible for all possible actions of Max player
    """
    if terminal(board):
        return utility(board), None

    v = -math.inf
    bestAction = None

    # For each action on a board
    for action in actions(board):
        # Check whats the min possible value from opponent for that action
        minValue = MinValue(result(board, action), v)[0]
        # Print action and value only for first layer
        if v_max == None:
            print(action, minValue)
        # Maximaze this for our best action
        if minValue > v:
            v = minValue
            bestAction = action
        # Don't check anymore if a value is found larger than previous v_max
        if v_max:
            if minValue > v_max:
                break

    return v, bestAction


def MinValue(board, v_min):
    """
    Returns the min value possible for all possible actions of Min player
    """
    if terminal(board):
        return utility(board), None

    v = math.inf
    bestAction = None

    # For each action on a board
    for action in actions(board):
        # Check whats the max possible value from opponent for that action
        maxValue = MaxValue(result(board, action), v)[0]
        # Print action and value only for first layer
        if v_min == None:
            print(action, maxValue)
        # Minimize this for our best action
        if maxValue < v:
            v = maxValue
            bestAction = action
        # Don't check anymore if a value is found lower than previous v_min
        if v_min:
            if maxValue < v_min:
                break
        
    return v, bestAction


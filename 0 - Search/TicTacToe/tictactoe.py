"""
Tic Tac Toe Player
"""

import math
import copy

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
    if all(initial_state()) == EMPTY:
        return X
    elif not terminal(board):
        count_O = sum(row.count('O') for row in board)
        count_X = sum(row.count('X') for row in board)
        if count_X == count_O:
            return X
        elif count_X > count_O:
            return O
    # if the game is over, return None
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("The action is not allowed")
    else:
        new_board = copy.deepcopy(board)
        (action_row, action_col) = action
        new_board[action_row][action_col] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for horizontal solutions
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]\
                and board[i][0] is not None:
            win_player = board[i][0]
            return win_player
    # Check for vertical solutions
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]\
                and board[0][j] is not None:
            win_player = board[0][j]
            return win_player
    # Check for diagonal solutions
    if board[0][0] == board[1][1] == board[2][2]\
            and board[0][0] is not None:
        win_player = board[0][0]
        return win_player
    if board[0][2] == board[1][1] == board[2][0]\
            and board[0][0] is not None:
        win_player = board[0][2]
        return win_player


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        if actions(board) == set():
            return True
        else:
            return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def min_value(board):
    if terminal(board):
        return utility(board), None

    # Initialize maximum value for v. Then cycle
    v = float("inf")
    move = None
    for action in actions(board):
        test, act = max_value(result(board, action))
        # If current value is lower, choose that action
        if test < v:
            v = test
            move = action
            if v == -1:
                return v, move
    return v, move


def max_value(board):
    if terminal(board):
        return utility(board), None

    # initialize minimum value for v. Then cycle
    v = float("-inf")
    move = None
    for action in actions(board):
        test, act = min_value(result(board, action))
        # If current value is higher, choose that action
        if test > v:
            v = test
            move = action
            if v == 1:
                return v, move
    return v, move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move

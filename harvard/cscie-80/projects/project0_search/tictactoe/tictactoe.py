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
    # If the terminal board is provided as input, any return value is acceptible


    if terminal(board):
        return None

    # In the inital state, X starts the game
    if board == initial_state():
        return X
    
    # To determien the next player, if the number of X is greater than O, it is O's turn
    count_of_x = sum(1 for row in board for item in row if item == X)
    count_of_o = sum(1 for row in board for item in row if item == O)
    if count_of_x > count_of_o:
        return O
 
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # If the terminal board is provided as input, any return value is acceptible
    if terminal(board):
        return None
    possible_actions = []

    # Loop through the board, and add the coordinates of empty cells in to possible_actions
    
    
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # First determine whose turn it is
    current_player = player(board)

    # Ensure the action can be made by verifying the cell is empty
    i = action[0]
    j = action[1]
    if board[i][j] != EMPTY:
        raise ValueError("Invalid Move")    # as per spec

    # Before updating the state, make a deep copy of the board (as per spec)
    test_board = copy.deepcopy(board)

    test_board[i][j] = current_player

    return test_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # A winner is possible when 3 cells in a row are occupied by it (horizontal, vertical or diagnoal)

    # Horizontal
    for i in board:
        if i[0] == X and i[1] == X and i[2] == X:
            return X
        if i[0] == O and i[1] == O and i[2] == O:
            return O
        
    # Vertial
    for j in range(0,3):
        if board[0][j] == X and board[1][j] == X and board[2][j] == X:
            return X
        if board[0][j] == O and board[1][j] == O and board[2][j] == O:
            return O

    # Check for diagonal
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O

    # Check for diagonal
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # count the number of cells filled
    count_of_occupied_cells = sum(1 for row in board for item in row if item != EMPTY)

    # If there is a winner or if all cells are filed, return True
    if winner(board) != None or count_of_occupied_cells == 9:
        return True

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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal return None
    if terminal(board):
        return None
    
    # Find the next best move 
    if player(board) == X:  # Maximize the score
        optimal_action = None
        optimal_score = -math.inf
        for action in actions(board):
            v = min_score(result(board, action))
            if v > optimal_score:
                optimal_score = v
                optimal_action = action
        return optimal_action
    
    if player(board) == O:  # Minimize the score
        optimal_action = None
        optimal_score = math.inf
        for action in actions(board):
            v = max_score(result(board, action))
            if v < optimal_score:
                optimal_score = v
                optimal_action = action
        return optimal_action

# Function that recursively compuetes the scores

def min_score(board):
    if terminal(board):
        return utility((board))
    
    optimal_score = math.inf
    for action in actions(board):
        optimal_score = min(optimal_score, max_score(result(board, action)))
    return optimal_score


def max_score(board):
    if terminal(board):
        return utility((board))
    
    optimal_score = -math.inf
    for action in actions(board):
        optimal_score = max(optimal_score, min_score(result(board, action)))
    return optimal_score
    

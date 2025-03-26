"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from util import StackFrontier, tttNode

X = "X"
O = "O"
EMPTY = None
inf = 2


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
    noneCount = 0
    for i in board:
        for j in i:
            if j == EMPTY:
                noneCount += 1
    if (noneCount%2) == 0:
        return O
    else:
        return X
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allActions = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                allActions.add((i,j))

    return allActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Action is not a valid action")
    
    copyBoard = deepcopy(board)
    copyBoard[action[0]][action[1]] = player(board)

    return copyBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    hor = []; vert = []; diag = []
    
    for i in range(3):
        for j in range(3):
            hor.append(board[i][j])
            vert.append(board[j][i])
            if i == j or (i==2 and j==0) or (i==0 and j==2):
                diag.append(board[i][j])
        if hor == [X,X,X] or vert == [X,X,X]:
            return X
        elif hor == [O,O,O] or vert == [O,O,O]:
            return O
        hor = []; vert = []
    
    if diag[2] == X:
        if diag[0] == diag[4]:
            if diag[0] == X and diag[4] == X:
                return X
        if (diag[1] == diag[3]):
            if diag[1] == X and diag[3] == X:
                return X 
    elif diag[2] == O:
        if diag[0] == diag[4]:
            if diag[0] == O and diag[4] == O:
                return O
        if (diag[1] == diag[3]):
            if diag[1] == O and diag[3] == O:
                return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    emptyCount = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                emptyCount += 1
    if winner(board) == None and emptyCount != 0:
        return False
    else:
        return True


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


def switch(turn):
    """
    Switches turn of the player
    """
    if turn == X:
        return O
    if turn == O:
        return X                


def listChildren(node):
    """
    Finds set of all children of a given node, in this context a child representing a given board state, based off an action
    We have a set of all possible actions, given a node, we can create children for the frontier as such
    In minimax, we will prune the children, but first we need to identify a childs value

    Returns a list of children nodes to the node given as argument
    """
    
    state = node.state
    acts = list(actions(state))
    nextState = []
    nextValue = []

    if len(acts) == 0:
        return None

    elif len(acts) != 0:
        for act in acts:
            nextState.append(result(state, act))
            
            if terminal(nextState[-1]):
                print(nextState)
                nextValue.append(utility(nextState[-1]))

    childNode = []   
    
    
    if len(nextValue) != len(nextState):
        for _ in range(len(nextState)-len(nextValue)):
            nextValue.append(None)         
    
    for i in range(len(acts)):
        childNode.append(tttNode(state=nextState[i],
                                 parent=node,
                                 action=acts[i],
                                 value=nextValue[i],
                                 depth=1))

    return childNode


def alphabeta(node, alpha, beta):
    if terminal(node.state):
        return node.value if node.value is not None else 0

    turn = player(node.state)
    if turn == X:
        val = -inf
        for i in listChildren(node):
            child_value = alphabeta(i, alpha, beta) if i.value is None else i.value
            if child_value is not None:
                val = max(val, child_value)
                alpha = max(alpha, val)
                if val >= beta:
                    break
        return val
    else:
        val = inf
        for i in listChildren(node):
            child_value = alphabeta(i, alpha, beta) if i.value is None else i.value
            if child_value is not None:
                val = min(val, child_value)
                beta = min(beta, val)
                if val <= alpha:
                    break
        return val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Algo -> minimax w/ alpha beta pruning 

    """

    start = tttNode(state = board, parent = None, action = None, value = None, depth=1)
    frontier = StackFrontier()
    if listChildren(start) != None:
        for node in listChildren(start):
            frontier.add(node)
    bestNode = start
    bestValues = []

    alpha = -inf
    beta = inf
    
    while True:
        if frontier.empty() == True:
            if bestNode == start:
                return None
            else:
                bestNode = bestValues[0]
                for i in bestValues:
                    turn = player(start.state)
                    if turn == X:
                        if i.value > bestNode.value:
                            bestNode = i
                        else:
                            continue
                    elif turn == O:
                        if i.value < bestNode.value:
                            bestNode = i
                        else:
                            continue
                return bestNode.action
    
        expandedNode = frontier.remove()
        expandedNode.value = alphabeta(expandedNode, alpha, beta)
        bestValues.append(expandedNode)
        bestNode = expandedNode
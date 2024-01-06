import tictactoe as ttt
from util import tttNode

EMPTY = None
X = "X"
O = "O"

#print(ttt.result(ttt.initial_state(),(2,2)))

winX = [[X, O, X],
        [O, EMPTY, X],
        [EMPTY, EMPTY, O]] 
winO =  [[X, X, O],
        [EMPTY, X, O],
        [EMPTY, EMPTY, EMPTY]]
draw =  [[X, O, X],
        [O, O, X],
        [X, X, O]]


testBoard = [[X, O, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, X]]
testBoard2 = [[X, O, EMPTY],
             [EMPTY, O, EMPTY],
             [EMPTY, EMPTY, X]]
testBoard3 = [[X, O, EMPTY],
             [EMPTY, O, O],
             [X, EMPTY, X]]

emptyBoard = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

testingBoard = [[X, X, EMPTY],
                [O, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

#print(ttt.winner(winX))

#print(ttt.terminal(ttt.initial_state()))

#print(ttt.utility(draw))
# # print(ttt.initial_state())
# print(ttt.listChildren(tttNode(state = ttt.initial_state(), parent = None, action = None, value = None, depth=0)))

# print(list(ttt.actions(winX))[1])

# start = tttNode(state = testBoard, parent = None, action = None, value = None, depth=0)
# childs = (ttt.listChildren(start))
# # print(len(childs))

# childschid = childs[0]

# grandchildren = ttt.listChildren(childschid)
# gc = grandchildren[0]
# print(gc.state)

# print(childschid.depth)
# print(f"Return Value {ttt.minimax(winO), ttt.player(winO)}")
# newboard = ttt.result(start.state, ttt.minimax(start.state))
# n = ttt.tttNode(newboard, None, None, None, 0)
# n1 = ttt.tttNode(testBoard,None,None,None,1)
# n2 = ttt.tttNode(testBoard2,None,None,None,1)
# n3 = ttt.tttNode(testBoard3,None,None,None,1)

#print(ttt.alphabeta(ttt.tttNode(winO,None,None,None,1),-2,2))

#print(f"n1{ttt.alphabeta(n1,-2,2)}, n2{ttt.alphabeta(n2,-2,2)}, n3{ttt.alphabeta(n3,-2,2)}")
# print(f"board{newboard}, alpha-beta algo: {ttt.alphabeta(n, -2, 2)}, move: {ttt.minimax(n.state)}, result: {ttt.result(n.state, ttt.minimax(n.state))}")
# print(f"Return Value {ttt.minimax(winO), ttt.player(winO)}")
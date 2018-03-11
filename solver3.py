import numpy as np
import fileinput
import time
import sys

## Port from the dumb solver from blog.gamesolver.org

class Position(object) :
    HEIGHT = 6
    WIDTH = 7
    boardSize = HEIGHT*WIDTH

    ## isWinningMove is the most time consuming task right now
    # 24 horiz + 21 vert + 24 diag = 69 total positions --> 69 * 4 / 42 =~ 6.6 average positions per square
    ## The easiest way to check for winning moves is to catalog them by position and then check only the ones that might apply
    ## Additionally, we move away from numpy and back to a python list

    ################################
    ##  5  11  17  23  29  35  41 ##
    ##  4  10  16  22  28  34  40 ##
    ##  3   9  15  21  27  33  39 ##
    ##  2   8  14  20  26  32  38 ##
    ##  1   7  13  19  25  31  37 ##
    ##  0   6  12  18  24  30  36 ##
    ################################

    winningMovesArr = [0] * 42
    for i in range(42) : winningMovesArr[i] = []
    
    ## Horizontal
    for x in range(WIDTH-3) :
        for y in range(HEIGHT) :
            base = HEIGHT*x+y
            delta = HEIGHT
            hlist = [base, base+delta, base+2*delta, base+3*delta]
            winningMovesArr[hlist[0]].append([hlist[1],hlist[2],hlist[3]])
            winningMovesArr[hlist[1]].append([hlist[0],hlist[2],hlist[3]])
            winningMovesArr[hlist[2]].append([hlist[0],hlist[1],hlist[3]])
            winningMovesArr[hlist[3]].append([hlist[0],hlist[1],hlist[2]])                                    

    ## Vertical
    for x in range(WIDTH) :
        for y in range(HEIGHT-3) :
            base = HEIGHT*x+y
            delta = 1
            hlist = [base, base+delta, base+2*delta, base+3*delta]
            winningMovesArr[hlist[0]].append([hlist[1],hlist[2],hlist[3]])
            winningMovesArr[hlist[1]].append([hlist[0],hlist[2],hlist[3]])
            winningMovesArr[hlist[2]].append([hlist[0],hlist[1],hlist[3]])
            winningMovesArr[hlist[3]].append([hlist[0],hlist[1],hlist[2]])                                    

    ## Diag SW to NE
    for x in range(WIDTH-3) :
        for y in range(HEIGHT-3) :
            base = HEIGHT*x+y
            delta = HEIGHT+1
            hlist = [base, base+delta, base+2*delta, base+3*delta]
            winningMovesArr[hlist[0]].append([hlist[1],hlist[2],hlist[3]])
            winningMovesArr[hlist[1]].append([hlist[0],hlist[2],hlist[3]])
            winningMovesArr[hlist[2]].append([hlist[0],hlist[1],hlist[3]])
            winningMovesArr[hlist[3]].append([hlist[0],hlist[1],hlist[2]])                                    

    ## Diag NW to SE
    for x in range(WIDTH-3) :
        for y in range(3,HEIGHT) :
            base = HEIGHT*x+y
            delta = HEIGHT-1
            hlist = [base, base+delta, base+2*delta, base+3*delta]
            winningMovesArr[hlist[0]].append([hlist[1],hlist[2],hlist[3]])
            winningMovesArr[hlist[1]].append([hlist[0],hlist[2],hlist[3]])
            winningMovesArr[hlist[2]].append([hlist[0],hlist[1],hlist[3]])
            winningMovesArr[hlist[3]].append([hlist[0],hlist[1],hlist[2]])                                    

    def __init__(self,orig=None) :
        if orig is None :
            self.board = [0] * (Position.WIDTH * Position.HEIGHT)
            self.height = [0] * Position.WIDTH
            self.moves = 0
        else :
            self.board  = orig.board[:]
            self.height = orig.height[:]
            self.moves  = orig.moves

    def nbMoves(self) :
        return self.moves

    def canPlay(self,col) :
        return self.height[col] < Position.HEIGHT

    def play(self,col) :
        player = 1 + self.moves % 2
        idx = Position.HEIGHT*col+self.height[col]
        self.board[idx] = player
        self.height[col] += 1
        self.moves += 1

    def unplay(self,col) :
        idx = Position.HEIGHT*col+self.height[col]-1
        self.board[idx] = 0
        self.height[col] -= 1
        self.moves -= 1

    def playSeq(self,xarr) :
        for x in xarr : self.play(x)

    def isWinningMove(self,col) :
        if self.height[col] >= self.HEIGHT : return False
        currentPlayer = 1 + self.moves % 2
        idx = Position.HEIGHT*col+self.height[col]
        b = self.board
        for arr in Position.winningMovesArr[idx] :
            if b[arr[0]] == currentPlayer and b[arr[1]] == currentPlayer and b[arr[2]] == currentPlayer : return True
        return False

class Solver(object) :
    def __init__(self) :
        self.nodeCount = 0

    def negamax(self,p,alpha,beta) :
        self.nodeCount += 1
        if p.moves == Position.boardSize : return 0
        
        for x in range(Position.WIDTH) :
            if p.isWinningMove(x) :
                return (Position.boardSize + 1 - p.moves) // 2

        mymax = (Position.boardSize - 1 - p.moves) // 2
        if (beta > mymax) :
            beta = mymax
            if alpha >= beta : return beta  ## First opportunity to short circuit

        for x in range(Position.WIDTH) :
            if(p.canPlay(x)) :
                p.play(x)
                score = -self.negamax(p,-beta,-alpha)
                p.unplay(x)

                ##p2 = Position(p)
                ##p2.play(x)
                ##score = -self.negamax(p2)
                if score >= beta  : return score ## Second opportunity to short circuit
                if score >= alpha : alpha = score
        return alpha

    def solve(self,p,weak=False) :
        self.nodeCount = 0
        if(weak) : return self.negamax(p,-1,1)
        mymin = -Position.boardSize//2
        mymax =  Position.boardSize//2
        return self.negamax(p,mymin,mymax)

    def getnodeCount(self) :
        return self.nodeCount

if __name__ == "__main__" :
    ##lines = [x for x in fileinput.input()]
    fn = "Test_L3_R1.txt" if len(sys.argv) < 2 else sys.argv[1]
    f = open(fn)
    lines = f.readlines()
    solver = Solver()
    idx = 0
    totalevaluations = 0
    totaltime = 0
    for l in lines :
        idx += 1
        p = Position()
        (sval1,sval2) = tuple(l.rstrip().split())
        seq = [int(x)-1 for x in sval1]
        val = int(sval2)
        p.playSeq(seq)
        t0 = time.time()
        score = solver.solve(p)
        t1 = time.time()
        locevaluations = solver.getnodeCount()
        loctime = max(t1-t0,0.001)
        totalevaluations += locevaluations
        totaltime += loctime
        print("Idx: %6d   Score: %3d   Val: %3d   Evaluations: %10d   Time: %7.3f   Eval_per_second:%11.2f   Cumulative_Eval_per_second:%11.2f" % (idx, score, val, locevaluations, loctime, 1.0*locevaluations/loctime, 1.0*totalevaluations/totaltime))
        







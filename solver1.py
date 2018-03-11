import numpy as np
import fileinput
import time

## Port from the dumb solver from blog.gamesolver.org

class Position(object) :
    HEIGHT = 6
    WIDTH = 7
    def __init__(self,orig=None) :
        if orig is None :
            self.board = np.zeros((Position.WIDTH,Position.HEIGHT),dtype=np.int8)
            self.height = [0] * Position.WIDTH
            self.moves = 0
        else :
            self.board  = np.copy(orig.board)
            self.height = orig.height[:]
            self.moves  = orig.moves

    def nbMoves(self) :
        return self.moves

    def canPlay(self,col) :
        return self.height[col] < Position.HEIGHT

    def play(self,x,seq=False) :
        a = x if seq else (x,)
        for col in a :
            player = 1 + self.moves % 2
            self.board[col,self.height[col]] = player
            self.height[col] += 1
            self.moves += 1
        return len(a) 

    def isWinningMove(self,col) :
        if self.height[col] >= self.HEIGHT : return False
        currentPlayer = 1 + self.moves % 2

        ## Check for vertical alignments
        h = self.height[col]
        if (h >= 3 and self.board[col,h-1] == currentPlayer and self.board[col,h-2] == currentPlayer and self.board[col,h-3] == currentPlayer) : return True

        ##horizontal and 2 diagonals
        for dy in (-1,0,1) :
            cnt = 0
            for dx in range(1,4) :
                x,y = col-dx,h-dx*dy
                if x >= 0 and y >= 0 and x < Position.WIDTH and y < Position.HEIGHT and self.board[x,y]==currentPlayer: cnt += 1
                else : break
            for dx in range(1,4-cnt) :
                x,y = col+dx,h+dx*dy
                if x >= 0 and y >= 0 and x < Position.WIDTH and y < Position.HEIGHT and self.board[x,y]==currentPlayer: cnt += 1
                else : break
            if (cnt>=3) : return True
        return False

class Solver(object) :
    def __init__(self) :
        self.nodeCount = 0

    def negamax(self,p) :
        self.nodeCount += 1
        boardSize = Position.WIDTH * Position.HEIGHT
        if p.nbMoves() == boardSize : return 0
        
        for x in range(Position.WIDTH) :
            if p.canPlay(x) and p.isWinningMove(x) :
                return (boardSize + 1 - p.nbMoves()) // 2

        bestScore = -boardSize

        for x in range(Position.WIDTH) :
            if(p.canPlay(x)) :
                p2 = Position(p)
                p2.play(x)
                score = -self.negamax(p2)
                if (score > bestScore) : bestScore = score
        
        return bestScore

    def solve(self,p) :
        self.nodeCount = 0
        return self.negamax(p)

    def getnodeCount(self) :
        return self.nodeCount

if __name__ == "__main__" :
    ##lines = [x for x in fileinput.input()]
    f = open("Test_L3_R1.txt")
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
        p.play(seq,True)
        t0 = time.time()
        score = solver.solve(p)
        t1 = time.time()
        locevaluations = solver.getnodeCount()
        loctime = max(t1-t0,0.001)
        totalevaluations += locevaluations
        totaltime += loctime
        print("Idx: %6d   Score: %3d   Val: %3d   Evaluations: %10d   Time: %7.3f   Eval_per_second:%9.2f   Cumulative_Eval_per_second:%9.2f" % (idx, score, val, locevaluations, loctime, 1.0*locevaluations/loctime, 1.0*totalevaluations/totaltime))
        







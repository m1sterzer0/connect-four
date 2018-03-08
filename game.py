import numpy as np 
import scipy.signal

class board(object) :
    def __init__(self) : pass
    def __hash__(self) : pass
    def __eq__(self)   : pass
    def reset(self) :    pass
    def play(self,player,action) : pass

class player(object) :
    def __init__(self) : pass
    def playTurn(self, board) : pass
    def train(self) : pass

class game(object) :
    def __init__(self, board=None, player1=None, player2=None):
        self.board   = board
        self.player1 = player1
        self.player2 = player2
        self.turn    = 0
        self.player  = 1

    def playTurn(self) :
        player = self.player1 if self.player==1 else self.player2
        action = player.playTurn(self.player,board)
        done,winner = board.play(self.player,action)
        self.player = 2 if self.player==1 else 1
        return done,winner

    def playGame(self) :
        self.board.reset()
        done = False; winner=0
        while (not done) :
            done,winner = self.playTurn()
        return winner

class connect4board(board) :
    winCondition1 = np.array([[1,1,1,1]])
    winCondition2 = np.array([[1],[1],[1],[1]])
    winCondition3 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    winCondition4 = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]])

    def __init__(self,orig=None) :
        if orig is None :
            self.board = np.zeros((6,7),dtype=np.int8)
            self.numpieces = 0
        else :
            self.board = np.copy(orig.board)
            self.numpieces = orig.numpieces

    def reset(self) :
        self.board = np.zeros((6,7),dtype=np.int8)
        self.numpieces = 0

    def __hash__(self) :
        return hash(self.board.tostring())

    def __eq__(self,other) :
        if type(other) is type(self) :
            return np.array_equal(self.board,other.board)
        return False

    def __ne__(self,other) :
        return not self.__eq__(other)

    def play(self,player,action) :
        legal = self._move(player,action)
        if not legal:
            winner = 1 if player == 2 else 2
            return True, winner
        winner = self._winner(action)
        if winner != 0 : return True, winner
        done = self._full()
        return done,winner

    def _move(self,player,action) :
        if self.board[5,action] != 0 :
            return False
        token = 1 if player == 1 else -1
        ## TODO: optimize the search here beter
        for i in range(6) :
            if self.board[i,action] == 0 :
                self.board[i,action] = token
                self.numpieces += 1
                return True
        return False ## Shouldn't get here

    def _full(self) :
        return (self.numpieces == 42)

    def _winner(self) :
        c1 = scipy.signal.convolve2d(self.board,connect4board.winCondition1,'valid')
        c2 = scipy.signal.convolve2d(self.board,connect4board.winCondition2,'valid')
        c3 = scipy.signal.convolve2d(self.board,connect4board.winCondition3,'valid')
        c4 = scipy.signal.convolve2d(self.board,connect4board.winCondition4,'valid')
        for c in ((c1,c2,c3,c4)) :
            if np.amax(c)>3.99  : return 1
            if np.amax(c)<-3.99 : return 2
        return 0


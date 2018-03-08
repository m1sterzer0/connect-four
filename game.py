import numpy as np 

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
            done,winner self.playTurn()
        return winner

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

class connect4board(board) :
    def __init__(self) : pass
        self.board = np.zeros((6,7),dtype=np.int8)

    def reset(self) :
        self.board = np.zeros((6,7),dtype=np.int8)

    def __hash__(self) : pass
    def __eq__(self)   : pass
        
    def play(self,player,action) :   

    def _full(self) :







    









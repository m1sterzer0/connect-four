import numpy as np 
import scipy.signal
from game import player
from game import board
import random

class classicTreePlayer(player) :
    def __init__(self, orig=None, playernum=None, depth=None) :
        if orig is None :
            self.depth     = depth     if depth     is not None else 4
            self.playernum = playernum if playernum is not None else 1
        else :
            self.depth     = depth     if depth     is not None else orig.depth 
            self.playernum = playernum if playernum is not None else orig.playernum

    def playTurn(self, board) :
        mynode = node(board,0,self.depth,self.playernum,self.playernum)
        val,move = mynode.miniMaxSearch()
        return move

    def train(self) : pass


class node(object) :
    def __init__(self, board, depth, maxdepth, myplayernum, playerturn) :
        self.depth       = depth
        self.maxdepth    = maxdepth
        self.board       = board
        self.myplayernum = myplayernum
        self.playerturn  = playerturn

    def miniMaxSearch(self) :
        if depth == maxdepth : return self.evaluateBoard(),0  ## Move shouldn't matter at max depth
        myturn    = True if self.myplayernum == self.playerturn else False

        ## Special case the last move, since this can produce draws, and we need to search for the valid move
        if self.board.numpieces >= 41 :
            for i in xrange(7) :
               locboard = board(orig=self.board)
               done,winner = locboard.play(self.playerturn,i)
               if (myturn     and winner==self.playerturn) : return  1.0,i
               if (not myturn and winner==self.playerturn) : return -1.0,i
               if winner==0                                : return  0.0,i
            return 0.0,0 ## Shouldn't get here

        locboards = [0] * 7
        done      = [0] * 7
        winner    = [0] * 7
        for i in xrange(7) :
            locboard[i]       = board(orig=self.board)
            done[i],winner[i] = locboard[i].play(self.playerturn,i)
            if (myturn     and done[i] and winner==self.playerturn) : return  1.0,i
            if (not myturn and done[i] and winner==self.playerturn) : return -1.0,i ## Move shouldn't matter here

        ## Now we iterate through remaining plays that aren't done and return the max/min of the results depending on minimax of node
        newplayer = 2 if self.playerturn == 1 else 2
        maxval,minval = -1.0,1.0
        maxidx = 0
        for i in xrange(7) :
            if not done[i] :
                childnode = node(locboard[i],self.depth+1,self.maxdepth,myplayernum,newplayer)
                val = childnode.miniMaxSearch()
                if (myturn     and val==1.0)  : return  1.0
                if (not myturn and val==-1.0) : return -1.0
                if val > maxval : maxval = val
                if val < minval : minval = val
        return maxval if myturn else minval

    def evaluateBoard(self) :
        return random.uniform(-0.5,0.5)
        

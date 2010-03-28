'''
Created on Aug 27, 2009

@author: victorhg
'''

from MVC.EventManager import *
from gamexp.conway.Model import Board

class Pattern():
    def run(self):
        while True:
            self.board.newGeneration()
            print self.board


class BlinkerPattern(Pattern):

    def __init__(self):
       self.board = Board.new(5,5, EventManager())
       self.board.setCellAlive(1, 2)
       self.board.setCellAlive(2, 2)
       self.board.setCellAlive(3, 2)
       
        
class ToadPatern(Pattern):
    
    def __init__(self):
        boardPattern = """
                        . . . . . .
                        . . . . . .
                        . . # # # .
                        . # # # . .
                        . . . . . .
                        . . . . . .
                        """
        self.board = Board.setup(boardPattern, EventManager())
        
class PretoPattern(Pattern):
    def __init__(self):
        strPattern = """
                      . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                      . # # # # # # # # # # . # # # # # # # # . # # # . . . . . . . # # # # # # # # # # .
                      . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                    """
        self.board = Board.setup(strPattern, EventManager())
        print self.board
        self.board.newGeneration()
        print self.board


board = ToadPatern()
board.run()
    


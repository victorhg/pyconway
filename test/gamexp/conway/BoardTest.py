'''
Created on Aug 25, 2009

@author: victorhg
'''

from gamexp.conway.control.EventManager import *

import unittest

from gamexp.conway.core.Conway import Board,UpdateCellsEvent



class BoardTest(unittest.TestCase):
    

    def setUp(self):
        self.evManager = EventManager()
        self.board = Board.new(2, 2, self.evManager)

    def testNewBoardShouldCreateAllFields(self):
        self.assertEqual(4, len(self.board.fields))
        
    def testSingleLiveCellCantLiveNewGeneration(self):
        posX = 0; posY = 0;
        self.board.setCellAlive(posX, posY);
        self.board.newGeneration();
        self.assertFalse(self.board.isCellAlive(0, 0))
        
        
    def testACellShouldKnowSelfPosition(self):
        self.board = Board.new(4, 4, self.evManager)
        self.assertEquals(1, self.board.getCell(0, 1).index)
        
    
    def test2x2SquareFullOfLiveCellsSurviveNewGeneration(self):
        resultBoard = """
                    # # 
                    # # 
                
                    """
        self.board.setCellAlive(0, 0)
        self.board.setCellAlive(1, 0)
        self.board.setCellAlive(1, 1)
        self.board.setCellAlive(0, 1)
        self.assertEquals(Board.newFromStr(resultBoard, self.evManager), self.board)
        self.board.newGeneration()
        self.assertEquals(Board.newFromStr(resultBoard, self.evManager), self.board)
        
            
    def test2x2SquareWith2LiveCellsDiesInOneGeneration(self):
        self.board.setCellAlive(0, 0)
        self.board.setCellAlive(1, 0)
        self.board.newGeneration()
        self.assertFalse(self.board.isCellAlive(0, 0))
        self.assertFalse(self.board.isCellAlive(1, 0))
        self.assertFalse(self.board.isCellAlive(0, 1))
        self.assertFalse(self.board.isCellAlive(1, 1))
        
    def test4x4SquareWithe2LiveCellsBug(self):
        self.board = Board.new(4, 4, self.evManager)
        self.board.setCellAlive(1, 1)
        self.board.setCellAlive(2, 1)
        self.board.newGeneration()
        self.assertFalse(self.board.isCellAlive(1, 1))
        self.assertFalse(self.board.isCellAlive(2, 1))
        self.assertFalse(self.board.isCellAlive(1, 2))
        self.assertFalse(self.board.isCellAlive(2, 2))
        self.assertFalse(self.board.isCellAlive(0, 0))
        self.assertFalse(self.board.isCellAlive(1, 0))
        self.assertFalse(self.board.isCellAlive(2, 0))
        self.assertFalse(self.board.isCellAlive(0, 2))
        
    
        
    def testShouldBeAbleToInquireCellAlive(self):
        self.assertFalse(self.board.isCellAlive(0, 0))
        self.board.setCellAlive(0, 0)
        self.assertTrue(self.board.isCellAlive(0, 0))
        
    def testShouldBeAbleToDetermineNumerOfNeighbors2x2FullSquare(self):
        self.board.setCellAlive(0, 0)
        self.board.setCellAlive(1, 0)
        self.board.setCellAlive(1, 1)
        self.board.setCellAlive(0, 1)
        self.assertEquals(3, self.board.getNumLiveNeighbours(0, 0))
        
    def testShouldBeAbleToDetermineNumerOfNeighbors2x2SquareWith2CellsAlive(self):
        self.board.setCellAlive(0, 0)
        self.board.setCellAlive(1, 0)
        self.assertEquals(1, self.board.getNumLiveNeighbours(0, 0))
    
    def testShouldBeAbleToDetermineNumerOfNeighbors2x2SquareWith2AnotherCellsAlive(self):
        self.board.setCellAlive(1, 0)
        self.board.setCellAlive(1, 1)
        self.assertEquals(1, self.board.getNumLiveNeighbours(1, 0))
    
    def testShouldBeAbleToDetermineNumerOfNeighbors2x2SquareWith2YetAnotherCellsAlive(self):
        self.board.setCellAlive(0, 1)
        self.board.setCellAlive(1, 0)
        self.assertEquals(1, self.board.getNumLiveNeighbours(1, 0))    
    
    def test3x3SquareWith4Neighbors(self):
        self.board = Board.new(3, 3, self.evManager)
        self.board.setCellAlive(0, 0)
        self.board.setCellAlive(1, 1)
        self.board.setCellAlive(2, 1)
        self.board.setCellAlive(0, 1)
        self.board.setCellAlive(1, 2)
        self.assertEquals(4, self.board.getNumLiveNeighbours(1, 1))
        
    def testFirstRuleAnyLiveCellDiesWithLessThanTwoNeighbors(self):
        resultBoard = """
                    . . . . .
                    . . . . .
                    . . . . .
                    . . . . .
                    . . . . .
                
                    """
        self.board = Board.new(5, 5, self.evManager)
        self.board.setCellAlive(1, 2)
        self.board.setCellAlive(3, 2)
        self.board.setCellAlive(0, 4)
        self.board.setCellAlive(4, 4)
        self.board.newGeneration()
        self.assertEquals(Board.newFromStr(resultBoard, self.evManager), self.board)

        
    def testBornCellRule(self):
        self.board.setCellAlive(1, 0)
        self.board.setCellAlive(0, 1)
        self.board.setCellAlive(1, 1)
        self.board.newGeneration()
        self.assertTrue(self.board.isCellAlive(1, 0))
        self.assertTrue(self.board.isCellAlive(0, 1))
        self.assertTrue(self.board.isCellAlive(1, 1))
        self.assertTrue(self.board.isCellAlive(0, 0))
        
    def test3x3SquareBlinkerPatternOneGeneration(self):
        
        self.startBlinkerPattern()
        self.board.newGeneration()
        self.assertTrue(self.board.isCellAlive(2, 2))
        # Top and Botton cells die on the first generation
        self.assertFalse(self.board.isCellAlive(1, 2))
        self.assertFalse(self.board.isCellAlive(3, 2))
        # Left and Right cells came to life
        self.assertTrue(self.board.isCellAlive(2, 1))
        self.assertTrue(self.board.isCellAlive(2, 3))
        
    def test3x3SquareBlinkerPattern2Generations(self):
        self.startBlinkerPattern()
        self.board.newGeneration()
        self.board.newGeneration()
        
        self.assertTrue(self.board.isCellAlive(2, 2))
        
        self.assertTrue(self.board.isCellAlive(1, 2))
        self.assertTrue(self.board.isCellAlive(3, 2))
        
        self.assertFalse(self.board.isCellAlive(2, 1))
        self.assertFalse(self.board.isCellAlive(2, 3))
        
    def testGetFieldIJ(self):
        self.board.setCellAlive(0, 0)    
        self.board.setCellAlive(1, 0)   
        
        strBoard = """
                    # .
                    # .
                
                    """
        self.assertEquals(Board.newFromStr(strBoard, self.evManager), self.board)
        

    def startBlinkerPattern(self):
        self.board = Board.new(5, 5, self.evManager)
        self.board.setCellAlive(1, 2)
        self.board.setCellAlive(2, 2)
        self.board.setCellAlive(3, 2)
    
    def startBlinkerPatternWithStrDefinition(self):
        strBoard = """
                    . . . . .
                    . . # . .
                    . . # . .
                    . . # . .
                    . . . . .
                
                    """
        self.board = Board.newFromStr(strBoard)
        self.board.setCellAlive(1, 2)
        self.board.setCellAlive(2, 2)
        self.board.setCellAlive(3, 2)
        
    def testShouldBeAbleToDefineBoardWithString(self):
        strBoard = """
                    . .
                    . .
                
                    """
        self.board = Board.newFromStr(strBoard, self.evManager)
        self.assertEquals(4, len(self.board.fields))
        
    def testShouldBeAbleToDetermineLiveCellsWithString(self):
        strBoard = """
                    . .
                    . #
                
                    """
        self.board = Board.newFromStr(strBoard, self.evManager)
        self.assertEquals(4, len(self.board.fields))
        self.assertTrue(self.board.isCellAlive(1, 1))
        
    def testEquals(self):
        strBoard1 = """
                    . .
                    . #
                
                    """
        
        strBoard2 = """
                    . #
                    . #
                
                    """
        board1 = Board.newFromStr(strBoard1, self.evManager)
        board2 = Board.newFromStr(strBoard1, self.evManager)
        self.assertTrue(board1 == board2)
        board3 = Board.newFromStr(strBoard2, self.evManager)
        self.assertFalse(board1 == board3)
    
    def testEquals2x2OnGeneration(self):
        strBoard1 = """
                    . #
                    # #
                
                    """
        
        strBoard2 = """
                    # #
                    # #
                
                    """
        
        board1 = Board.newFromStr(strBoard1, self.evManager)
        board1.newGeneration()
        board2 = Board.newFromStr(strBoard2, self.evManager)
        self.assertTrue(board1 == board2)
        
    def testBlinkerPaternWithStrBoardAsResult(self):
        resultBoard = """
                    . . . . .
                    . . . . .
                    . # # # .
                    . . . . .
                    . . . . .
                  """
        self.board = Board.new(5, 5, self.evManager)
        self.board.setCellAlive(1, 2)
        self.board.setCellAlive(2, 2)
        self.board.setCellAlive(3, 2)
        
        self.board.newGeneration()
        self.assertTrue(Board.newFromStr(resultBoard, self.evManager) == self.board)
    
    def testLiveCellWithFourNeighboursDies(self):
        resultBoard = """
                    . . . . 
                    . . . # 
                    . # . # 
                    . # # # 
                  """
        startBoard = """
                    . . . . 
                    . . . # 
                    . # # # 
                    . . # . 
                  """
        self.board = Board.newFromStr(startBoard, self.evManager)
        self.board.newGeneration()
        self.assertTrue(Board.newFromStr(resultBoard, self.evManager) == self.board)
    

    def testEventCell(self):
        
        class FakeListener():
            arrived = False
            def __init__(self, evManager):
                self.evManager = evManager
                self.evManager.RegisterListener(self)
            
            
            def Notify(self, event):
                if isinstance(event, UpdateCellsEvent):
                    self.arrived = True


        listener = FakeListener(self.evManager)
        self.board.setCellAlive(1, 1)
        self.board.newGeneration()
        self.assertTrue(listener.arrived) 
        
     
        
        
        

if __name__ == "__main__":
    unittest.main() 

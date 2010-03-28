'''
Created on Aug 31, 2009

@author: victorhg
'''
from gamexp.conway.control.Events import *
from gamexp.conway.core.Conway import *

class ConwayController:
    def __init__(self, evManager, window):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.window = window
        
    def Notify(self, event):
        if isinstance(event, CellEvent):
            self.window.updateSquareStatus(event.cellIndex, event.cellAlive)
            self.board.updateCellStatus(event.cellIndex, event.cellAlive)
            
            
        elif isinstance(event, NewGameEvent):
            self.board = Board.new(event.numRows, event.numColumns, self.evManager)

        elif isinstance(event, NewGenerationEvent):
            self.board.newGeneration()
            
        elif isinstance(event, UpdateCellsEvent):
            for cell in event.cells:
                self.window.updateSquareStatus(cell.index, cell.alive)
        
        self.window.updateBoard()
            

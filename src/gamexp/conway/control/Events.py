'''
Created on Aug 31, 2009

@author: victorhg
'''


class Event:
    '''
    this is a superclass for any events that might be generated by an object
    and sent to the EventManager
    '''
    def __init__(selfparams):
        '''
        Constructor
        '''
        self.name = 'Generic Event'

class CellEvent(Event):
    def __init__(self, cellIndex, cellAlive):
        self.name = 'Cell Event'
        self.cellIndex = cellIndex
        self.cellAlive = cellAlive
        
class UpdateCellsEvent(Event):
    def __init__(self, cells):
        self.name = 'Update cells event'
        self.cells = cells
        
class RessurectCellEvent(Event):
    def __init(self, cellIndex):
        self.name = 'Alive!! It is Alive!!'
        self.cellIndex = cellIndex
        
class NewGameEvent(Event):
    def __init__(self, numRows, numColumns):
        self.name = 'New Game Event'
        self.numRows = numRows
        self.numColumns = numColumns
        
class NewGenerationEvent(Event):
    def __init__(self):
        self.name = 'NewGenerationEvent - Let the life make its path'
        

'''
Created on Aug 25, 2009

@author: victorhg
'''

from Model import *
from gamexp.conway.control.Events import *


class Board(object):
    # Maps the number of neighbors to final state (True = must live, False = must die)
    def buildConwayLiveCellRulesMap(self):
        rules = dict.fromkeys(range(0, 9), False)
        rules.update(dict.fromkeys([2, 3], True))
        return rules
    def buildConwayDeadCellRulesMap(self):
        rules = dict.fromkeys(range(0, 9), False)
        rules[3] = True
        return rules
    
    
    @staticmethod
    def new(rows, columns, evManager):
        board = Board(evManager, rows, columns)
        return board
    
    @staticmethod
    def newFromStr(strBoard, evManager):    
        board = Board(evManager)
        board.setupFromStr(strBoard)
        return board
        
    def __init__ (self, evManager, rows = 0, columns = 0):
        self.conwayLiveCellRules = self.buildConwayLiveCellRulesMap()
        self.conwayDeadCellRules = self.buildConwayDeadCellRulesMap()
   
        self.numRows = rows
        self.numColumns = columns
        self.evManager = evManager
        self.fields = []
        
        for index in range(0, (self.numRows * self.numColumns)):
            row, col = self.toRowColumn(index)
            cell = Cell(index, row, col, False)
            self.fields.append(cell)

    def __eq__(self, other):
        if len(self.fields) != len(other.fields):
            return False
        
        for cell1 in self.fields:
            if not (cell1.alive == other.fields[cell1.index].alive):
                return False             
        return True
    
    def setupFromStr(self, str):
        strBoard = str.strip()
        cells = []
        index = 0
        columnsCount = 0
        firstRow = True
        for char in strBoard:
            if firstRow and char == '\n':
                columnsCount = index    
                firstRow = False
                
            if char in ('.', '#'):
                cells.append(Cell(index, -1, -1,  (char == '#')))
                index += 1
        self.numRows = index / columnsCount
        self.numColumns = columnsCount
        for cell in cells:
            cell.row, cell.column = self.toRowColumn(cell.index)
        self.fields = cells
    
    def __str__(self):
        strPrint = ""
        for cell in self.fields:
            if not cell.alive:
                alive = '.'
            else:
                alive = '#'
            
            value = self.getColumnIndex(cell.index)
            if value == (self.numColumns - 1):
                alive += '\n' 
            else:
                alive += ' '
                
            strPrint += alive
        strPrint += '\n'         
        return strPrint
    
    
    
    def newGeneration(self):
        deathList = []
        aliveList = []
        
        def findNeighbors(cell):
            liveNeighbours = self.getNumLiveNeighbours(cell.row, cell.column)
            if cell.alive:
                if not self.conwayLiveCellRules[liveNeighbours]:
                    deathList.append(cell)
            else:
                if self.conwayDeadCellRules[liveNeighbours]:
                    aliveList.append(cell)
            
        map(findNeighbors, self.fields)
                    
        self.ressurect(aliveList)
        self.killThemAll(deathList)
        allChanged = []
        allChanged.extend(aliveList)
        allChanged.extend(deathList)
        self.evManager.Post(UpdateCellsEvent(allChanged))

    def ressurect(self, alive):
        for cell in alive:
            cell.alive = True
        
    def killThemAll(self, deathList):
        for cell in deathList:
            cell.alive = False
    
    def setCellAlive(self, row, column):
        cell = self.getCell(row, column)
        cell.alive = True
#        self.evManager.Post(CellEvent(cell.index, True))
        
        
    def updateCellStatus(self, index, setCellAlive):
        self.fields[index].alive = setCellAlive
        
            
    def firstRule(self, cell):
        return self.getNumLiveNeighbours(self.getRowIndex(cell.index), self.getColumnIndex(cell.index)) < 2
    
    def secondRule(self, cell):
        return self.getNumLiveNeighbours(self.getRowIndex(cell.index), self.getColumnIndex(cell.index)) > 3
    
    
    def fourthRule(self, field):
        return self.getNumLiveNeighbours(self.getRowIndex(field.index), self.getColumnIndex(field.index)) == 3
        
        
    def isCellAlive(self, row, column):    
        return self.getCell(row, column).alive
    
        
    def getNumLiveNeighbours(self, row, column):
        """Much better now..."""
        numNeighbours = 0
        
        rowPositionMask = [1, 1, 1, -1, -1, -1, 0, 0]
        columnPositionMask = [1, -1, 0, 1, -1, 0, 1, -1]
        
        for p in range(0, len(rowPositionMask)):
            neighbourRowPosition = row + rowPositionMask[p]
            neighbourColumnPosition = column + columnPositionMask[p]
            if self.neighbourExists(neighbourRowPosition, neighbourColumnPosition):
                numNeighbours += 1
        
        return numNeighbours


    def neighbourExists(self, row, column):
        if row in range(0, self.numRows) and column in range(0, self.numColumns):
            return self.isCellAlive(row, column)
        
        return False
           
    def getCell(self, row, column):
       index = (row * self.numColumns) + column
       return self.fields[index]

    def toRowColumn(self, index):
        rowIndex = index / self.numColumns
        columnIndex = index % self.numColumns
        return rowIndex, columnIndex
        
    
    def getRowIndex(self, position):
        rowIndex = position / self.numColumns
        return rowIndex

    def getColumnIndex(self, position):
        columnIndex = position % self.numColumns
        
        return columnIndex


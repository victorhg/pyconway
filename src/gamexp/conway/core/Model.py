'''
Created on Aug 28, 2009

@author: victorhg
'''

class Cell:
    def __init__(self, index, row, column, alive=False):
        self.index = index
        self.row = row
        self.column = column
        self.alive = alive
        
    def __str__(self):
        return str(self.index) + '| '+ str(self.alive)
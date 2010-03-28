'''
Created on Aug 31, 2009

@author: victorhg
'''

import pygame

from pygame.locals import *
from gamexp.conway.control.EventManager import EventManager
from gamexp.conway.control.Controller import *

from time import time 

class Square():
    squareSize = 10
    def __init__(self, xPosition, yPosition, color):
        self.xPosition = xPosition
        self.yPosition= yPosition
        self.color = color
        self.representation = [xPosition, yPosition, self.squareSize, self.squareSize]
        

#---[ MENU CLASS]---------
from menu import *
        
class ConwayMenu:
    SHOW_MENU = 0
    START_GAME = 1
    EXIT_GAME = 2
    PLAYING = 3
    def __init__(self, screen):
        self.menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
               [('Start Game', self.START_GAME, None),
                ('Exit',       self.EXIT_GAME, None)])
        
        self.menu.set_center(True, True)
        self.menu.set_alignment('center', 'center')
    def update(self, event, state):
        return self.menu.update(event, state)
    
    

#---[INTERFACE]---------
class ConwayWindow():
    windowHeightSize = 640
    windowWidthSize = 480
    BLACK_COLOR = (0,0,0)
    GREEN_COLOR = (60,200,100)

    def __init__(self, evManager):
        self.numRows = self.windowHeightSize / Square.squareSize
        self.numColumns = self.windowWidthSize / Square.squareSize
        self.evManager = evManager


    def getIndex(self, xPosition, yPosition):
        column = xPosition / Square.squareSize
        row = yPosition / Square.squareSize
        index = row*self.numColumns + column 
        return index


    def getYWindowCoordinate(self, index):
        return (index / self.numColumns) * Square.squareSize

    
    def getXWindowCoordinate(self, index):
        return  (index % self.numColumns) * Square.squareSize
    

    def drawBoard(self):
        self.screenBoard = []
        for index in range(0, self.numColumns*self.numRows):
            xPosition = self.getXWindowCoordinate(index)
            yPosition = self.getYWindowCoordinate(index)
            square = Square(xPosition,  yPosition, self.BLACK_COLOR)
            self.screenBoard.append(square)
            self.screen.fill(self.BLACK_COLOR, square.representation)
           
       
            
            
        
    def magic(self):    
        pygame.init()
        self.screen = pygame.display.set_mode((self.windowWidthSize,self.windowHeightSize), HWSURFACE)

        self.drawBoard()
        
        self.menu = ConwayMenu(self.screen)
         
        state = ConwayMenu.SHOW_MENU
        prev_state = -1
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        # The main while loop
        while 1:
        # Check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
            if prev_state != state:
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                prev_state = state
        
        # Get the next event
            event = pygame.event.wait()
            
            if event.type == pygame.QUIT:
                 pygame.quit()
                 return
            
            if event.type == KEYDOWN or event.type == EVENT_CHANGE_STATE:
               
                state = self.handleMenuState(state, event)
                    
                if event.key == K_SPACE:
                        self.evManager.Post(NewGenerationEvent())
                        
                elif event.key == K_RETURN and state == ConwayMenu.PLAYING: #ENTER KEY
                        for int in range(0, 20):
                            self.evManager.Post(NewGenerationEvent())
            
            
            elif event.type == MOUSEBUTTONDOWN:
                    xPos = event.pos[0] 
                    yPos = event.pos[1] 
                    index = self.getIndex(xPos,  yPos)
                    square = self.screenBoard[index]
                    paintSquare = square.color != self.GREEN_COLOR
                    self.evManager.Post(CellEvent(index, paintSquare ))
                    #pygame.display.flip()
                    
            
                
    def handleMenuState(self, state, event):
        rect_list = []
        if state == ConwayMenu.SHOW_MENU:
            rect_list, state = self.menu.update(event, state)   
        elif state == ConwayMenu.START_GAME:
            self.startGame()
            state = ConwayMenu.PLAYING
        elif state == ConwayMenu.EXIT_GAME:
            pygame.quit()
            return
        elif event.key == K_ESCAPE:
            state = ConwayMenu.SHOW_MENU
            
        pygame.display.update(rect_list)
        return state
                
    def startGame(self):
        self.drawBoard()
        self.evManager.Post(NewGameEvent(self.numRows, self.numColumns))
        pygame.event.set_allowed(pygame.MOUSEMOTION)
        

    def updateBoard(self):
        pygame.display.flip()
        
    def updateSquareStatus(self, cellIndex, paintSquare):
        square = self.screenBoard[cellIndex]
        if(paintSquare):
            square.color = self.GREEN_COLOR
        else:
            square.color = self.BLACK_COLOR
        self.screen.fill(square.color, square.representation )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
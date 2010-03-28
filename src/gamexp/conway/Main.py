'''
Created on Aug 31, 2009

@author: victorhg
'''

from gamexp.conway.control.Controller import *
from gamexp.conway.control.EventManager import *
from gamexp.conway.gui.View import *



def main():
    evManager = EventManager()    
    g = ConwayWindow(evManager)
    conwayGame = ConwayController(evManager, g)
    g.magic()

if __name__ == '__main__': main()

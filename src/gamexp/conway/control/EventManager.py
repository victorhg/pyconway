'''
Created on Aug 27, 2009

@author: victorhg
'''

from weakref import WeakKeyDictionary

class EventManager:
   '''
   this class is responsible for coordinating most communication between
   the Model, View and Controller.
   I use WeakKeyDictionary to keep track of the registered listeners. From the 
   python documentation:
   
   Mapping class that references keys weakly. Entries in the dictionary will 
   be discarded when there is no longer a strong reference to the key.
   
   Using this dictionary takes care of object scope, avoiding dispatching to
   a non existing listener.
   
   @todo: I need to implement event categories, avoiding spamming notifies for
   events that only matters for some listeners.
   '''
   
   def __init__(self):
       self.listeners = WeakKeyDictionary()
       
   def RegisterListener(self, listener):
       self.listeners[ listener ] = 1
       
   def UnregisterListener(self, listener):
       if listener in self.listeners.keys():
           del self.listeners[ listener ]
           
   def Post(self, event):
       for listener in self.listeners.keys():
           listener.Notify( event )
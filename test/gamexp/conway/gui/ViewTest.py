'''
Created on Aug 31, 2009

@author: victorhg
'''
import unittest


from gamexp.conway.gui.View import ConwayWindow

class ViewTest(unittest.TestCase):

    def setUp(self):
        self.window = ConwayWindow()
        

    def testTransformationWindowCoordinatesToIndex(self):
        x = 3
        y = 9
        index = self.window.getIndex(x, y)
        self.assertEquals(0, index)
        
    def testTransformationWindowCoordinatesToIndexLastItemInARow(self):
        x = 8
        y = 475
        index = self.window.getIndex(x, y)
        self.assertEquals(47, index)
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
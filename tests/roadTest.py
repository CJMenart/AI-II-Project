# this file tests the road class                                                 
import unittest
import sys
# fix the path in order to import player class                                           
#originalPath = sys.path[0]                                                                         
sys.path[0] += '/../model'
from player import Player
from player import ResourceType
from GameState import GameState
from road import *
from point import Point
from settlement import Settlement

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.r = Road(Point(1,2), Point(2,2), 1)

    def test_adjacentRoads_1_2_and_2_1(self):
        self.r = Road(Point(1,2), Point(2,1), 1)
        adjRoads = self.r.adjacentRoads()
        #for r in adjRoads: 
        #    print(r)
        self.assertIn(Road(Point(1,2), Point(1,1), -1), adjRoads)
        self.assertIn(Road(Point(2,1), Point(1,1), -1), adjRoads)
        self.assertIn(Road(Point(1,2), Point(2,2), -1), adjRoads)
        self.assertIn(Road(Point(2,1), Point(2,2), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)

    def test_adjacentRoads_1_2_and_2_2(self):
        self.r = Road(Point(1,2), Point(2,2), 1)
        adjRoads = self.r.adjacentRoads()
                                                       
        self.assertIn(Road(Point(1,2), Point(1,3), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(1,3), -1), adjRoads)
        self.assertIn(Road(Point(1,2), Point(2,1), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(2,1), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)

    def test_adjacentRoads_2_2_and_2_3(self):
        self.r = Road(Point(2,2), Point(2,3), 1)
        adjRoads = self.r.adjacentRoads()
        
        self.assertIn(Road(Point(2,2), Point(1,3), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(1,3), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(3,2), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(3,2), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)
    
    def test_setOwner_22_23(self):
        self.r = Road(Point(2,2), Point(2,3), -1)
        setId = 1
        #self.r.setOwner(setId)
        expectedRoad = Road(Point(2,2), Point(2,3), setId)
        self.assertEqual(expectedRoad, self.r.getRoadWithOwner(setId))
'''
    def test_adjacentSettlements_10_11(self):
        self.r = Road(Point(1,0), Point(1,1), 1)
        self.s = Settlement(Point(0,1), Point(1,0), Point(1,1), -1)
        adjSettlements = self.r.adjacentSettlements()
        #self.s = Settlement(Point(0,1), Point(1,0), Point(1,1), -1)
        for s in adjSettlements:
            print(s)
        self.assertIn(Settlement(Point(0,1), Point(1,0), Point(1,1), -1), adjSettlements)
        self.assertIn(Settlement(Point(2,0), Point(1,0), Point(1,1), -1), adjSettlements)
        self.assertEqual(len(adjSettlements), 0)
'''

if __name__ == '__main__':
    unittest.main()

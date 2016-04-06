# this file tests the settlement class                                                 
import unittest
import sys
# fix the path in order to import player class                                           
#originalPath = sys.path[0]                                                                         
sys.path[0] += '/../model'
from player import Player
from player import ResourceType
from GameState import GameState
from road import Road
from point import Point
from settlement import Settlement


class TestSettlement(unittest.TestCase):

    def setUp(self):
        self.s = Settlement(Point(1,1), Point(2,2), Point(2,1), 1)

    def test_adjacentRoads_1_1_and_2_2_and_2_1(self):
        self.s = Settlement(Point(1,1), Point(2,2), Point(2,1), 1)
        adjRoads = self.s.adjacentRoads()
        self.assertIn(Road(Point(1,1), Point(2,2), -1), adjRoads)
        self.assertIn(Road(Point(1,1), Point(2,1), -1),adjRoads)
        self.assertIn(Road(Point(2,1), Point(2,2), -1),adjRoads)
        self.assertEqual(3, len(adjRoads))

    def test_adjacentRoads_1_1_and_2_2_and_1_2(self):
        self.s = Settlement(Point(1,1), Point(2,2), Point(1,2), 1)
        adjRoads = self.s.adjacentRoads()
        self.assertIn(Road(Point(1,1), Point(2,2), -1), adjRoads)
        self.assertIn(Road(Point(1,1), Point(1,2), -1),adjRoads)
        self.assertIn(Road(Point(1,2), Point(2,2), -1),adjRoads)
        self.assertEqual(3, len(adjRoads))

    def test_adjacentSettlementsByRoad_10_11(self): 
        r = Road(Point(1,0), Point(1,1), 1)   
        adjSettlements = Settlement.adjacentSettlementsByRoad(r)   
        self.assertIn(Settlement(Point(0,1), Point(1,0), Point(1,1), -1), \
                          adjSettlements)  
        self.assertIn(Settlement(Point(2,0), Point(1,0), Point(1,1), -1), \
                          adjSettlements)   
        self.assertEqual(len(adjSettlements), 2)

    def test_adjacentSettlementsByRoad_11_21(self):
        r = Road(Point(1,1), Point(2,1), 1)
        adjSettlements = Settlement.adjacentSettlementsByRoad(r)
        self.assertIn(Settlement(Point(1,1), Point(2,1), Point(1,2), -1), \
                          adjSettlements)
        self.assertIn(Settlement(Point(1,1), Point(2,1), Point(2,0), -1), \
                          adjSettlements)
        self.assertEqual(len(adjSettlements), 2)

    def test_adjacentSettlements_11_20_21(self):
        s = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        adjSettlements = s.adjacentSettlements()
        self.assertIn(Settlement(Point(1,1), Point(2,0), Point(1,0), -1), \
                          adjSettlements)
        self.assertIn(Settlement(Point(1,1), Point(2,1), Point(1,2), -1), \
                          adjSettlements)
        self.assertIn(Settlement(Point(2,0), Point(2,1), Point(3,0), -1), \
                          adjSettlements)
        self.assertEqual(len(adjSettlements), 3)

    def test_getSettlementWithOwner(self):
        s = Settlement(Point(1,1), Point(2,0), Point(2,1), -1)
        newOwnerId = 1
        expectedResult = Settlement(Point(1,1), Point(2,0), Point(2,1), newOwnerId)
        self.assertEqual(s.getSettlementWithOwner(newOwnerId), expectedResult)

if __name__ == '__main__':
    unittest.main()

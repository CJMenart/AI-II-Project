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

if __name__ == '__main__':
    unittest.main()

# this file tests the road class                                                 
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

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.r = Road(Point(1,2), Point(2,2), 1)

    def test_adjacentRoads_1_2_and_2_2(self):
        self.r = Road(Point(1,2), Point(2,2), 1)
        adjRoads = self.r.adjacentRoads()
        #for r in adjRoads: 
        #    print(r)
        self.assertIn(Road(Point(1,2), Point(1,1), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(1,1), -1), adjRoads)
        self.assertIn(Road(Point(1,2), Point(2,3), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(2,3), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)

    def test_adjacentRoads_1_2_and_2_3(self):
        self.r = Road(Point(1,2), Point(2,3), 1)
        adjRoads = self.r.adjacentRoads()
                                                       
        self.assertIn(Road(Point(1,2), Point(2,2), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(1,3), -1), adjRoads)
        self.assertIn(Road(Point(1,2), Point(2,2), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(1,3), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)

    def test_adjacentRoads_2_2_and_2_3(self):
        self.r = Road(Point(2,2), Point(2,3), 1)
        adjRoads = self.r.adjacentRoads()
        
        self.assertIn(Road(Point(2,2), Point(1,2), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(3,2), -1), adjRoads)
        self.assertIn(Road(Point(2,2), Point(1,2), -1), adjRoads)
        self.assertIn(Road(Point(2,3), Point(3,2), -1), adjRoads)
        self.assertEqual(len(adjRoads), 4)

if __name__ == '__main__':
    unittest.main()

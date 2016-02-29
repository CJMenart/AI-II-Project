# this file tests the player class                                                 
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
        self.player = Player(1)
    def test_initial_nGrain(self):
        self.assertEqual(self.player.resources[ResourceType.GRAIN], 0)
    def test_add_1_grain_nGrain(self):
        self.player.addResource(ResourceType.GRAIN,1)
        self.assertEqual(self.player.resources[ResourceType.GRAIN], 1)
    def test_add_2_wool_nWool(self):
        self.player.addResource(ResourceType.WOOL,2)
        self.assertEqual(self.player.resources[ResourceType.WOOL], 2)
    def test_add_1_grain_add_2_brick_nResources(self):
        self.player.addResource(ResourceType.GRAIN,1)
        self.player.addResource(ResourceType.BRICK,2)
        self.assertEqual(self.player.nResources(), 3)
    def test_has_2_wool_remove_1_wool_nWool(self):
        self.player.addResource(ResourceType.WOOL,2)
        self.player.rmvResource(ResourceType.WOOL, 1)
        self.assertEqual(self.player.resources[ResourceType.WOOL], 1)
    def test_has_2_wool_remove_2_wool_nWool(self):
        self.player.addResource(ResourceType.WOOL,2)
        self.player.rmvResource(ResourceType.WOOL, 2)
        self.assertEqual(self.player.resources[ResourceType.WOOL], 0)
    def test_has_2_wool_remove_3_wool_nWool(self):
        self.player.addResource(ResourceType.WOOL,2)
        # should return 1 (error) when try to remove 3 wool
        self.assertEqual(self.player.rmvResource(ResourceType.WOOL, 3), 1)
    def test_initial_empty_roads(self):
        gameState = GameState([],  [], [], [], [], [])
        self.assertEqual(self.player.roads(gameState), [])
    def test_only_player2_has_road_see_player1_roads(self):
        gameState = GameState([], [], [Road(Point(1,1),Point(1,2),2)], [], [], [])
        self.assertEqual(self.player.roads(gameState), [])
    def test_player1_player2_both_has_one_road_see_player1_roads(self):
        gameState = GameState([], [], [Road(Point(1,0),Point(1,1),1), Road(Point(1,1),Point(1,2),2)], [], [], [])
        self.assertEqual(self.player.roads(gameState)[0], Road(Point(1,0),Point(1,1),1))
    def test_player1_has_two_road_see_player1_roads(self):
        gameState = GameState([], [], [Road(Point(1,0),Point(1,1),1), Road(Point(1,1),Point(1,2),1)], [], [], [])
        self.assertEqual(self.player.roads(gameState)[0], Road(Point(1,0),Point(1,1),1))
        self.assertEqual(self.player.roads(gameState)[1], Road(Point(1,1),Point(1,2),1))
    def test_initial_empty_settlements(self):
        gameState = GameState([], [], [], [], [], [])
        self.assertEqual(self.player.settlements(gameState), [])
    def test_only_player2_has_settlement_see_player1_settlements(self):
        gameState = GameState([], [], [], [Settlement(Point(0,0), Point(0,1), Point(1,0), 2)], [], [])
        self.assertEqual(self.player.settlements(gameState), [])
    def test_player1_has_1_settlement_player_2_has_1_settlement_see_player1_settlement(self):
        gameState = GameState([], [], [], [Settlement(Point(0,0), Point(0,1), Point(1,0), 1), \
                                           Settlement(Point(0,1), Point(1,1), Point(0,2), 2)],\
                                  [], [])
        self.assertEqual(self.player.settlements(gameState)[0], \
                             Settlement(Point(0,0), Point(0,1), Point(1,0), 1))


if __name__ == '__main__':
    unittest.main()


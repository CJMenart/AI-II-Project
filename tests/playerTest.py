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
        self.player = Player(1, {ResourceType.WOOL: 0 , ResourceType.BRICK:0,ResourceType.\
ORE:0, ResourceType.LUMBER:0, ResourceType.GRAIN:0} )
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
    def test_add_1_grain_GameState_change(self):
        gameState = GameState([], [Player(1)],[],[],[],[])
        self.assertEqual(gameState.players[0].resources[ResourceType.GRAIN], 0)
        gameState.players[0].addResource(ResourceType.GRAIN,1)
        self.assertEqual(gameState.players[0].resources[ResourceType.GRAIN], 1)
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

    def test_one_corner_settlement_available_roads_1_0_and_2_0_and_1_1(self):
        gameState = GameState([], [Player(1)], [], [Settlement(Point(1,0), Point(2,0),\
                               Point(1,1), 1)], [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(1,0),Point(1,1),-1 ), availableRoads)
        self.assertIn(Road(Point(1,0),Point(2,0),-1 ), availableRoads)
        self.assertIn(Road(Point(1,1),Point(2,0),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 3)

    def test_one_corner_settlement_available_roads_1_0_and_0_1_and_1_1(self):
        gameState = GameState([], [Player(1)], [], [Settlement(Point(1,0), Point(0,1),\
                               Point(1,1), 1)], [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(1,0),Point(1,1),-1 ), availableRoads)
        self.assertIn(Road(Point(1,0),Point(1,1),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 2)

    def test_one_corner_settlement_available_roads_1_1_and_0_1_and_1_0(self):
        gameState = GameState([], [Player(1)], [], [Settlement(Point(1,1), Point(0,1),\
                               Point(1,0), 1)], [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(1,1),Point(0,1),-1 ), availableRoads)
        self.assertIn(Road(Point(1,1),Point(1,0),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 2)

    def test_one_settlement_available_roads_2_2_and_2_1_and_1_2(self):
        gameState = GameState([], [Player(1)], [], [Settlement(Point(2,2), Point(2,1),\
                               Point(1,2), 1)], [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(2,2),Point(2,1),-1 ), availableRoads)
        self.assertIn(Road(Point(2,2),Point(1,2),-1 ), availableRoads)
        self.assertIn(Road(Point(1,2),Point(2,1),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 3)

    def test_one_settlement_available_roads_2_2_and_2_1_and_1_2_built_road_22_and_21(self):
        gameState = GameState([], [Player(1)], [Road(Point(2,2),Point(2,1), 1 )],\
                                  [Settlement(Point(2,2), Point(2,1),\
                               Point(1,2), 1)], [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        #self.assertIn(Road(Point(2,2),Point(2,1),-1 ), availableRoads)
        self.assertIn(Road(Point(2,2),Point(1,2),-1 ), availableRoads)
        self.assertIn(Road(Point(1,2),Point(2,1),-1 ), availableRoads)
        self.assertIn(Road(Point(2,1),Point(3,1),-1 ), availableRoads)
        self.assertIn(Road(Point(2,2),Point(3,1),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 4)

    def test_one_settlement_available_roads_2_2_and_2_1_and_1_2_built_all_roads(self):
        setupRoads = [Road(Point(2,2),Point(2,1), 1 ), \
                          Road(Point(2,2),Point(1,2),1 ), \
                          Road(Point(1,2),Point(2,1),1 )]
        gameState = GameState([], [Player(1)], setupRoads,\
                                  [Settlement(Point(2,2), Point(2,1),\
                               Point(1,2), 1)], [], [])
        #print('gameState len of setupRoads is {0} '.format(len(gameState.roads)))
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(1,1),Point(1,2),-1 ), availableRoads)                   
        self.assertIn(Road(Point(1,1),Point(2,1),-1 ), availableRoads)
        self.assertIn(Road(Point(1,3),Point(1,2),-1 ), availableRoads)
        self.assertIn(Road(Point(1,3),Point(2,2),-1 ), availableRoads)
        self.assertIn(Road(Point(3,1),Point(2,1),-1 ), availableRoads)
        self.assertIn(Road(Point(3,1),Point(2,2),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 6)

    def test_two_settlement_available_roads(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1), \
                               Settlement(Point(2,3), Point(3,3), Point(2,4), 1)]
        gameState = GameState([], [Player(1)], [], setupSettlement, [], [])
        availableRoads = gameState.players[0].availableRoads(gameState)
        self.assertIn(Road(Point(1,0),Point(2,0),-1 ), availableRoads)
        self.assertIn(Road(Point(1,0),Point(1,1),-1 ), availableRoads)
        self.assertIn(Road(Point(1,1),Point(2,0),-1 ), availableRoads)
        
        self.assertIn(Road(Point(2,3),Point(3,3),-1 ), availableRoads)
        self.assertIn(Road(Point(2,3),Point(2,4),-1 ), availableRoads)
        self.assertIn(Road(Point(3,3),Point(2,4),-1 ), availableRoads)
        self.assertEqual(len(availableRoads), 6)

    def test_one_settlement_10_11_20_no_road_available_settlements(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1)]
        gameState = GameState([], [Player(1)], [], setupSettlement, [], [])
        availableSettlements = gameState.players[0].availableSettlements(gameState)
        self.assertEqual(len(availableSettlements), 0)

    def test_one_settlement_10_11_20_one_road_11_20_available_settlements(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1)]
        setupRoad = [Road(Point(1,1), Point(2,0), 1)]
        gameState = GameState([], [Player(1)], setupRoad, setupSettlement, [], [])
        availableSettlements = gameState.players[0].availableSettlements(gameState)
        self.assertEqual(len(availableSettlements), 0)

    def test_one_settlement_10_11_20_two_road_11_20_and_20_21_available_settlements(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1)]
        setupRoad = [Road(Point(1,1), Point(2,0), 1), Road(Point(2,1), Point(2,0), 1)] 
        gameState = GameState([], [Player(1)], setupRoad, setupSettlement, [], [])
        availableSettlements = gameState.players[0].availableSettlements(gameState)
        self.assertIn(Settlement(Point(2,0), Point(2,1), Point(3,0), -1), availableSettlements)
        self.assertEqual(len(availableSettlements), 1)

    def test_two_settlement_10_11_20_two_road_11_20_and_20_21_available_settlements(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1), \
                               Settlement(Point(2,0), Point(2,1), Point(3,0), 2)]
        setupRoad = [Road(Point(1,1), Point(2,0), 1), Road(Point(2,1), Point(2,0), 1)]
        gameState = GameState([], [Player(1)], setupRoad, setupSettlement, [], [])
        availableSettlements = gameState.players[0].availableSettlements(gameState)
        #self.assertIn(Settlement(Point(2,0), Point(2,1), Point(3,0), -1), availableSettlements)
        self.assertEqual(len(availableSettlements), 0)

    def test_two_settlement2_10_11_20_two_road_11_20_and_20_21_available_settlements(self):
        setupSettlement = [Settlement(Point(1,0), Point(1,1), Point(2,0), 1), \
                               Settlement(Point(2,1), Point(3,0), Point(3,1), 2)]
        setupRoad = [Road(Point(1,1), Point(2,0), 1), Road(Point(2,1), Point(2,0), 1)]
        gameState = GameState([], [Player(1)], setupRoad, setupSettlement, [], [])
        availableSettlements = gameState.players[0].availableSettlements(gameState)
        #self.assertIn(Settlement(Point(2,0), Point(2,1), Point(3,0), -1), availableSettlements)
        self.assertEqual(len(availableSettlements), 0)

    def test_DFS_base_case(self): 
        setupAddingRoad = Road(Point(1,1), Point(2,0), 1) 
        setupExistingRoad = []  
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        self.assertEqual(DFSresult[0], 0)
        self.assertEqual(DFSresult[1], [])

    def test_DFS_base_case_add_one(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,1), Point(2,1), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        self.assertEqual(DFSresult[0], 1)
        self.assertEqual(DFSresult[1], [Road(Point(1,1), Point(2,1), 1)])

    def test_DFS_direction_with_2_branch(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,1), Point(2,1), 1), \
                                 Road(Point(2,0), Point(2,1), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        self.assertEqual(DFSresult[0], 1)
        self.assertEqual(DFSresult[1], [Road(Point(1,1), Point(2,1), 1)])

    def test_DFS_direction_with_one_road_that_has_two_branches(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,1), Point(2,1), 1), \
                                 Road(Point(1,1), Point(1,2), 1), \
                                 Road(Point(2,1), Point(1,2), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        self.assertEqual(DFSresult[0], 2)
        self.assertEqual(DFSresult[1], [Road(Point(1,1), Point(1,2), 1), \
                                            Road(Point(1,1), Point(2,1), 1)])

    def test_DFS_cycle(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(0,1), Point(1,1), 1), \
                                 Road(Point(0,2), Point(1,1), 1), \
                                 Road(Point(1,2), Point(1,1), 1), \
                                 Road(Point(2,1), Point(1,1), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        self.assertEqual(DFSresult[0], 5)
        #for r in DFSresult[1] :
        #    print(r)
        #self.assertEqual(DFSresult[1], [Road(Point(1,1), Point(1,2), 1), \
        #                                    Road(Point(1,1), Point(2,1), 1)])

    def test_DFS_cycle_with_one_extra(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,0), Point(2,0), 1), \
                                 Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(0,1), Point(1,1), 1), \
                                 Road(Point(0,2), Point(1,1), 1), \
                                 Road(Point(1,2), Point(1,1), 1), \
                                 Road(Point(2,1), Point(1,1), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        #for r in DFSresult[1] :
        #    print(r)
        self.assertEqual(DFSresult[0], 6)

    def test_DFS_cycle_with_one_extra_reverse_direction(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,0), Point(2,0), 1), \
                                 Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(0,1), Point(1,1), 1), \
                                 Road(Point(0,2), Point(1,1), 1), \
                                 Road(Point(1,2), Point(1,1), 1), \
                                 Road(Point(2,1), Point(1,1), 1)]
        direction = Settlement(Point(1,1), Point(2,0), Point(1,0), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        #for r in DFSresult[1] :                                         
        #    print(r)                                                         
        self.assertEqual(DFSresult[0], 5)

    def test_DFS_cycle_with_one_extra_branch(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [ \
                                 Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(0,1), Point(1,1), 1), \
                                 Road(Point(0,2), Point(1,1), 1), \
                                 Road(Point(1,2), Point(1,1), 1), \
                                 Road(Point(2,1), Point(1,1), 1), \
                                 Road(Point(1,2), Point(2,1), 1) ]
        direction = Settlement(Point(1,1), Point(2,0), Point(2,1), 1)
        player = Player(1)
        DFSresult = player.DFS(setupAddingRoad, setupExistingRoad, direction)
        #for r in DFSresult[1] :                                            
        #    print(r)                                                          
        self.assertEqual(DFSresult[0], 5)

    def test_possibleLongestRoadLength_base_case(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), 1)
        setupExistingRoad = []
        player = Player(1)
        result = player.possibleLongestRoadLength(setupAddingRoad, setupExistingRoad)
        self.assertEqual(result, 1)
    
    def test_possibleLongestRoadLength_base_case_add_one(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), 1)
        setupExistingRoad = [Road(Point(1,1), Point(2,1), 1)]
        player = Player(1)
        result = player.possibleLongestRoadLength(setupAddingRoad, setupExistingRoad)
        self.assertEqual(result, 2)

    def test_possibleLongestRoadLength_direction_with_2_branch(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,1), Point(2,1), 1), \
                                 Road(Point(2,0), Point(2,1), 1)]
        player = Player(1)
        result = player.possibleLongestRoadLength(setupAddingRoad,\
                         setupExistingRoad)
        self.assertEqual(result, 2)

    def test_possibleLongestRoadLength_cycle(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(0,1), Point(1,1), 1), \
                                 Road(Point(0,2), Point(1,1), 1), \
                                 Road(Point(1,2), Point(1,1), 1), \
                                 Road(Point(2,1), Point(1,1), 1)]
        player = Player(1)
        result = player.possibleLongestRoadLength(setupAddingRoad,\
                             setupExistingRoad)
        self.assertEqual(result, 6)

    def test_possibleLongestRoadLength_one_road_in_each_direction(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), -1)
        setupExistingRoad = [Road(Point(1,0), Point(1,1), 1), \
                                 Road(Point(2,0), Point(2,1), 1)]
        player = Player(1)
        result = player.possibleLongestRoadLength(setupAddingRoad,\
                             setupExistingRoad)
        self.assertEqual(result, 3)

'''
    def test_possibleLongestRoadLen_base_case(self):
        setupAddingRoad = Road(Point(1,1), Point(2,0), 1)
        setupExistingRoad = []
        player = Player(1)
        result = player.possibleLongestRoadLen(addingRoad, existingRoad)
        self.assertEqual(1, result)
'''
if __name__ == '__main__':
    unittest.main()


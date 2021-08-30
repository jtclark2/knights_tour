import unittest
import copy

# Test target
from src.knights_tour.knight import Knight

# Additional resources
from src.knights_tour.grid_pos import GridPos
from src.knights_tour.gameengine import GameEngine
from src.knights_tour.board import Board
from src.knights_tour.user_interface import UI

class KnightTester(unittest.TestCase):
    """
    Let the knight's gauntlet commence!
    """

    def setUp(self):
        """
        Setup the board, and place the knight
        """
        self.k = Knight(GameEngine(Board("Boards/8x8_board.txt")))

    # TODO: Really should have an assert...ensures the methods run, but not how they run
    def test_reconstruct_path_32x32(self):

        self.k = Knight(
            GameEngine(Board("Boards/32x32_board.txt")),
            start_pos=GridPos(0, 0),
            end_pos=GridPos(31, 31),
        )

        self.k.plan_path()

        path = self.k.reconstruct_path()
        UI.display_path_as_list(path, self.k.cost_map)

        journey = {}
        journey_cost = {}
        for step_num, step_node in enumerate(path):
            journey[step_node] = step_num
            journey_cost[step_node] = self.k.cost_map.get_value(step_node)

        print("Cost:/n")
        UI.display_board(self.k.game_engine.board, pieces = journey)
        print("Journey:/n")
        pieces = {pos:f"█{val}█" for pos,val in journey.items()}
        UI.display_board(self.k.journey_map, pieces = pieces, value_width=5)

        UI.display_board(self.k.journey_map, pieces = journey, value_width=5)
        UI.display_board(self.k.journey_map, pieces = journey_cost, value_width=5)

    def test_explore_moves__single_step(self):
        """
        A few extra checks, since python list copies tend to do everything by reference.
        """
        board_path = "Boards/8x8_board.txt"
        start_pos = GridPos(1, 1)
        self.k = Knight(GameEngine(Board(board_path)), start_pos)

        self.k.journey_map = copy.deepcopy(self.k.game_engine.board)
        self.k.cost_map = copy.deepcopy(self.k.game_engine.board)
        self.k.cost_map.reset_board()
        self.k.journey_map.reset_board()

        self.k.cost_map.set_element(start_pos, 0)

        # make sure the appropriate nodes are found
        nodes = self.k._explore_moves(start_pos)

        expected_valid_nodes = [
            GridPos(0, 3),
            GridPos(3, 0),
            GridPos(2, 3),
            GridPos(3, 2),
        ]
        # These 4 nodes are expected, though order is not guaranteed
        for node in nodes:
            self.assertTrue(node in expected_valid_nodes)

        expected_omitted_node = [
            GridPos(0, 0),
            GridPos(3, -1),
            GridPos(2, -1),
            GridPos(-1, 2),
            GridPos(-1, 0),
        ]
        for node in nodes:
            self.assertFalse(node in expected_omitted_node)

        # make sure the cost_map updates
        expected_cost_map = [
            [None, None, None, 1, None, None, None, None],
            [None, 0, None, None, None, None, None, None],
            [None, None, None, 1, None, None, None, None],
            [1, None, 1, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]

        self.assertEqual(self.k.cost_map._board_grid, expected_cost_map)

        expected_journey_map = [
            [None, None, None, GridPos(1, 1), None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, GridPos(1, 1), None, None, None, None],
            [GridPos(1, 1), None, GridPos(1, 1), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]

        self.assertEqual(self.k.journey_map._board_grid, expected_journey_map)

    # TODO: figure out what this really tests
    def test_plan_path(self):
        self.k.plan_path()

    # TODO: figure out what this really tests...doesn't seem to do much
    def test_reconstruct_path_8x8(self):
        self.k.plan_path()
        # path = self.k.reconstruct_path()
        # for step in path:
        #     my_str = "Cost: %i \t" % self.k.cost_map.get_piece(step)
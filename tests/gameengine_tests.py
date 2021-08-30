import unittest

from src.knights_tour.board import Board
from src.knights_tour.gameengine import GameEngine
from src.knights_tour.grid_pos import GridPos
from src.knights_tour.pieces import Pieces

class GameEngineTester(unittest.TestCase):
    def setUp(self):
        """
        Setup the board, and place the knight
        """
        self.game_engine = GameEngine(Board("Boards/8x8_board.txt"))

    def test_validate_node_sequence__pass(self):
        """
        Tests basic moves, including 0,0 edge case.
        """
        positions = [
            GridPos(0, 0),
            GridPos(2, 1),
            GridPos(4, 0),
            GridPos(3, 2),
            GridPos(4, 4),
            GridPos(6, 5),
        ]

        valid = self.game_engine.validate_pos_sequence(positions)
        self.assertTrue(valid)

    def test_validate_node_sequence__fail_move_off_board(self):
        """
        Tests failure by falling off of the board
        """
        positions = [GridPos(0, 0), GridPos(2, 1), GridPos(1, -1)]

        self.assertFalse(self.game_engine.validate_pos_sequence(positions))

    def test_validate_node_sequence__fail_not_valid_for_knight(self):
        """
        Tests failure by falling off of the board
        """
        positions = [GridPos(0, 0), GridPos(2, 1), GridPos(4, 4)]
        self.assertFalse(self.game_engine.validate_pos_sequence(positions))

    def test_teleport__pass(self):
        """
        Verify that teleport is able to find both locations, and return the
        correct exit locations.
        """
        teleport_in = GridPos(11, 26)
        teleport_out = GridPos(23, 27)
        self.game_engine = GameEngine(Board("Boards/32x32_board.txt"))
        out_pos = self.game_engine.teleport(teleport_in)
        self.assertEqual(out_pos, teleport_out)

    def test_teleport__no_tele_access(self):
        """
        Verify that teleport is able to find both locations, and return the
        correct exit locations.
        """
        start_pos = GridPos(15, 20)
        self.game_engine = GameEngine(Board("Boards/32x32_board.txt"))
        out_pos = self.game_engine.teleport(start_pos)
        self.assertEqual(out_pos, None)

    def test_teleport__fail_too_many_tp(self):
        """
        Verify that a poorly formed board is detected.
        """
        teleport_in = [11, 26]
        self.game_engine = GameEngine(Board("Boards/32x32_board.txt"))
        self.game_engine.board._board_grid[15][20] = Pieces.TELEPORT.value
        with self.assertRaises(Exception):
            self.game_engine.teleport(teleport_in)

    def test_validate_within_bounds(self):
        self.assertTrue(self.game_engine.validate_within_bounds(GridPos(0, 0)))
        self.assertTrue(self.game_engine.validate_within_bounds(GridPos(0, 1)))
        self.assertTrue(self.game_engine.validate_within_bounds(GridPos(4, 5)))
        self.assertFalse(self.game_engine.validate_within_bounds(GridPos(-1, 0)))
        self.assertFalse(self.game_engine.validate_within_bounds(GridPos(-2, -5)))

    def test_get_possible_nodes(self):
        """
        Verify that the correct nodes are returned.
        """
        curr_node = GridPos(1, 1)
        nodes = self.game_engine.get_possible_moves(curr_node)
        expected_valid_nodes = [
            GridPos(0, 3),
            GridPos(3, 0),
            GridPos(2, 3),
            GridPos(3, 2),
        ]

        # These 4 nodes are expected, though order is not gauranteed
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

    def test_validate_barrier_clear__pass(self):
        """
        Test that barriers can be detected appropriately.
        """
        self.game_engine = GameEngine(Board("Boards/32x32_board.txt"))

        curr_node = GridPos(0, 7)
        next_node = GridPos(1, 9)
        valid = self.game_engine.validate_barrier_clear(curr_node, next_node)
        self.assertFalse(valid)

        curr_node = GridPos(0, 7)
        next_node = GridPos(1, 5)
        valid = self.game_engine.validate_barrier_clear(curr_node, next_node)
        self.assertTrue(valid)

        # negative dx and dy cases (reverse the nodes)
        curr_node = GridPos(1, 9)
        next_node = GridPos(0, 7)
        valid = self.game_engine.validate_barrier_clear(curr_node, next_node)
        self.assertFalse(valid)

        curr_node = GridPos(1, 5)
        next_node = GridPos(0, 7)
        valid = self.game_engine.validate_barrier_clear(curr_node, next_node)
        self.assertTrue(valid)
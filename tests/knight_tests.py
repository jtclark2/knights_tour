import unittest

# Test target
from src.knights_tour.knight import Knight

# Additional resources
from src.knights_tour.user_interface import *
from src.knights_tour.grid_pos import GridPos
from src.knights_tour.board import Board

class KnightTester(unittest.TestCase):
    """
    Let the knight's gauntlet commence!
    """

    def setUp(self):
        """
        Setup the board, and place the knight
        """
        self.k = Knight(Board("Boards/8x8_board.txt"))
        self.str_board_truth = self.k.board

    def test_display_knight__pass(self):
        """
        Verify that display displays the board with the knight properly placed.
        """
        import sys
        from io import StringIO

        str_board_ground_truth = (
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". K . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . ."
        )

        print_buffer = StringIO()
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            self.k.display_knight()
        finally:
            sys.stdout = default_output

        # Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(print_buffer.getvalue(), "\n" + str_board_ground_truth + "\n")

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

        valid = self.k.validate_pos_sequence(positions)
        # print self.k.error_context
        self.assertTrue(valid)

    def test_validate_node_sequence__rich_print(self):
        """
        ###Problem 1: Board print between moves activated
        Tests basic moves, including 0,0 edge case.
        """
        from io import StringIO
        import sys

        positions = [
            GridPos(0, 0),
            GridPos(2, 1),
            GridPos(4, 0),
            GridPos(3, 2),
            GridPos(4, 4),
            GridPos(6, 5),
        ]

        print_buffer = StringIO()
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            valid = self.k.validate_pos_sequence(positions, rich_print=True)
        finally:
            sys.stdout = default_output

        self.assertTrue(valid)

        expected_output = (
            "\nK . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". K . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . . . . . . .\n"
            "K . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . K . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . K E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            "\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . K . .\n"
            ". . . . . . . .\n"
        )

        self.assertEqual(print_buffer.getvalue(), expected_output)

    def test_validate_node_sequence__fail_move_off_board(self):
        """
        Tests failure by falling off of the board
        """
        positions = [GridPos(0, 0), GridPos(2, 1), GridPos(1, -1)]

        self.assertFalse(self.k.validate_pos_sequence(positions))
        self.assertEqual(self.k.error_context, "Moves are not contained on the board")

    def test_validate_node_sequence__fail_not_valid_for_knight(self):
        """
        Tests failure by falling off of the board
        """
        positions = [GridPos(0, 0), GridPos(2, 1), GridPos(4, 4)]

        self.assertFalse(self.k.validate_pos_sequence(positions))

        error_phrase = (
            "2 adjascent positions represent a move that a"
            "knight is not permitted to make."
        )
        self.assertRegex(self.k.error_context, error_phrase)

    def test_teleport__pass(self):
        """
        Verify that teleport is able to find both locations, and return the
        correct exit locations.
        """
        teleport_in = GridPos(11, 26)
        teleport_out = GridPos(23, 27)
        self.k = Knight(Board("Boards/32x32_board.txt"), teleport_in)
        # print '\n'
        # self.k.display_knight()
        out_pos = self.k.teleport(teleport_in)
        self.assertEqual(out_pos, teleport_out)

    def test_teleport__no_tele_access(self):
        """
        Verify that teleport is able to find both locations, and return the
        correct exit locations.
        """
        start_pos = GridPos(15, 20)
        self.k = Knight(Board("Boards/32x32_board.txt"), start_pos)
        out_pos = self.k.teleport(start_pos)
        self.assertEqual(out_pos, None)

    def test_teleport__fail_too_many_tp(self):
        """
        Verify that a poorly formed board is detected.
        """
        teleport_in = [11, 26]
        # teleport_out = [23, 27]
        self.k = Knight(Board("Boards/32x32_board.txt"), teleport_in)
        self.k.board._board_grid[15][20] = "T"
        with self.assertRaises(Exception):
            self.k.teleport(teleport_in)

    def test_validate_within_bounds(self):
        self.assertTrue(self.k.validate_within_bounds(GridPos(0, 0)))
        self.assertTrue(self.k.validate_within_bounds(GridPos(0, 1)))
        self.assertTrue(self.k.validate_within_bounds(GridPos(4, 5)))
        self.assertFalse(self.k.validate_within_bounds(GridPos(-1, 0)))
        self.assertFalse(self.k.validate_within_bounds(GridPos(-2, -5)))

    def test_get_possible_nodes(self):
        """
        Verify that the correct nodes are returned.
        """
        curr_node = GridPos(1, 1)
        nodes = self.k.get_possible_moves(curr_node)
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

    def test_explore_moves__single_step(self):
        """
        A few extra checks, since python list copies tend to do everything by reference.
        """
        board_path = "Boards/8x8_board.txt"
        start_pos = GridPos(1, 1)
        self.k = Knight(Board(board_path), start_pos)

        self.k.journey_map = Board(board_path)
        self.k.cost_map = Board(board_path)
        self.k.cost_map.reset_board()
        self.k.journey_map.reset_board()

        self.k.cost_map.set_element(start_pos, 0)

        # make sure the appropriate nodes are found
        nodes = self.k.explore_moves(start_pos)

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

        self.assertEqual(self.k.cost_map.grid, expected_cost_map)

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

        self.assertEqual(self.k.journey_map.grid, expected_journey_map)

    # TODO: figure out what this really tests
    def test_plan_path(self):
        self.k.plan_path()

    # TODO: figure out what this really tests...doesn't seem to do much
    def test_reconstruct_path_8x8(self):
        self.k.plan_path()
        # path = self.k.reconstruct_path()
        # for step in path:
        #     my_str = "Cost: %i \t" % self.k.cost_map.get_piece(step)

    def test_reconstruct_path_32x32(self):

        self.k = Knight(
            Board("Boards/32x32_board.txt"),
            start_pos=GridPos(0, 0),
            target_pos=GridPos(31, 31),
        )
        self.k.board.set_element(GridPos(5,8), ".")
        self.k.plan_path()

        # Show Journey
        path = self.k.reconstruct_path()
        print_str = ""
        for step in path:
            my_str = "Cost: %i \t" % self.k.cost_map.get_value(step)
            print_str = print_str + my_str + "Node: " + str(step) + " -->\n"

        journey = {}
        journey_cost = {}
        for step in enumerate(path):
            step_num = step[0]
            step_node = step[1]
            journey[step_num] = step_node
            journey_cost[self.k.cost_map.get_value(step_node)] = step_node

        print(print_str)
        # self.k.cost_map.display_board(pieces = journey)
        self.k.board.display_board(pieces=journey)
        self.k.board.display_board(pieces=journey_cost)

    def test_validate_barrier_clear__pass(self):
        """
        Test that barriers can be detected appropriately.
        """
        self.k = Knight(
            Board("Boards/32x32_board.txt"),
            start_pos=GridPos(0, 0),
            target_pos=GridPos(31, 31),
        )

        curr_node = GridPos(0, 7)
        next_node = GridPos(1, 9)
        valid = self.k.validate_barrier_clear(curr_node, next_node)
        self.assertFalse(valid)

        curr_node = GridPos(0, 7)
        next_node = GridPos(1, 5)
        valid = self.k.validate_barrier_clear(curr_node, next_node)
        self.assertTrue(valid)

        # negative dx and dy cases (reverse the nodes)
        curr_node = GridPos(1, 9)
        next_node = GridPos(0, 7)
        valid = self.k.validate_barrier_clear(curr_node, next_node)
        self.assertFalse(valid)

        curr_node = GridPos(1, 5)
        next_node = GridPos(0, 7)
        valid = self.k.validate_barrier_clear(curr_node, next_node)
        self.assertTrue(valid)


if __name__ == "__main__":
    k = Knight(Board("Boards/8x8_board.txt"))
    unittest.main()

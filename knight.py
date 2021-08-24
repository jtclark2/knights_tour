"""
Assumptions:
    a) Board is rectangular. I anticipate other cases would work with minor
       tweaks, notably Board.read_board() and Knight.validate_within_bounds()
    b) The 32x32 board starts are passed in, since 'S' and 'E' were not
       pre-populated. 

Level 1: Call Knight().validate_pos_sequence(node_sequence, rich_print)
    Note that while this method fulfills the objective, a generator proved
    more useful than a validator throughout the problem.
Level 2: Call Knight().plan_path()
    Note that Knight().reconstruct_path() is useful for viewing the results.
Level 3: Same as 2. Now we just excplicitly assume all inputs must be 1.
    If your data_set wasn't already curated, then we'd convert each node
    value to '.' As it stands, problem 3 applies to a board that has only
    '.', 'S', & 'E', and the cost function I've used holds true.
Level 4: Again, same as 2,3. It's just a matter of swapping the cost function.
    In the Rock case, I chose to implement a absurdly high cost, rather than 
    adding an explicit filter.
    In the special cases of teleportation, and barriers, I chose to modify
    the legal moves that were generated. It just made more logical sense
    updating the node_generation method.
Level 5:
    Just a thought, but...plan the plan with a heuristic that iterates,
    using the last map as the heuristic for the next. It would be slow,
    but might get the job done.

Major Assumption: This space is fully searchable, since the board is 32x32,
meaning that 1024 positions exist, each with 8 possible moves. This is well
within our computational capbability. For a larger problem, we'd have to use
a more efficient approach with a goal heuristic, such as A-star.

Created by: Trevor Clark

Custom Dependencies:
    board.py
"""


import unittest
import board
from grid_pos import GridPos


class Knight:
    def __init__(self, board_path=None, start_pos=None, target_pos=None):
        """
        Initialize the knight on the board.
        Inputs:
            board_path:
            knight_start_pos: Expects input [row,col].
                              Finds 'S' on the board by default.
        """

        self.board_path = board_path
        self.board = board.Board(self.board_path)
        if start_pos is None:
            try:
                self.start_pos = self.board.find_element("S")[0]  # assuming only 1
            except:
                self.start_pos = None
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if target_pos is None:
            try:
                self.target_pos = self.board.find_element("E")[0]  # assuming only 1
            except:
                self.target_pos = None
        else:
            self.target_pos = target_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

    def reconstruct_path(self):
        optimal_path = []
        current_node = self.target_pos
        while True:
            optimal_path.append(current_node)
            current_node = self.journey_map.get_piece(current_node)
            if current_node is None:
                break

        return list(reversed(optimal_path))

    def plan_path(self):
        """
        Plans a path for the knight to take. Optimizes according to cost function
        defined by self.get_cost().

        Inputs:
            None

        Outputs:
            None

        Side-Effects:
            self.cost_map: a board whose values represent the lowest discovered cost
                of achieving that position.
            self.journey_map: A map of reference coordinates to the last point. This
                can be used to reconstruct the optimal path.
        """
        active_list = [self.knight_pos]  # Init list with a start pos

        # Initialize map of journey costs
        start_pos = self.knight_pos

        self.journey_map = board.Board(self.board_path)
        self.cost_map = board.Board(self.board_path)
        self.cost_map.reset_board()
        self.journey_map.reset_board()

        self.cost_map.set_element(start_pos, 0)

        while True:
            # Rational moves are allowed for a knight, land on the board, and land
            # upon unexplored spaces
            exploratory_node = active_list.pop(0)
            # print "Update:"
            # self.display_knight(exploratory_node)
            new_nodes = self.explore_moves(exploratory_node)

            # conservative finish condition
            # if active_list == []:
            #     # report()
            #     return

            for new_node in new_nodes:
                active_list.append(new_node)
            # Quick Finish condition (holds true in simple case)
            if active_list == []:
                # if self.target_pos in new_nodes:
                # report()

                # print "Journey:"
                # self.journey_map.display_board()
                # print "Cost Map:"
                # self.cost_map.display_board()
                # print "Minimum Cost:\t%i" % self.cost_map.get_element(self.target_pos)
                return

    def explore_moves(self, curr_node, move_heuristic=None):
        """
        Explores the map by making each available rational move.

        Inputs:
            curr_pos = (y,x), node we're exploring from
            move_heuristic: nothing yet, may help in the next step
                Function which determines which moves make sense.
                1) In the simplest case, knight moves on the board
                2) Could also limit to unexplored space
                3) Could limit to only low cost heuristics
        Outputs:
            positions: list of new position nodes for continued exploration.

        Side-Effects:
            self.path_map = Board() in which each value is a pos pointing to
            node that it came from. This tracking data will allow us to reverse
            engineer the path after finding the minimal cost route.
        """

        # find all desirable nodes to move to
        new_nodes = []
        for node in self.get_possible_nodes(curr_node):
            try:
                move_cost = self.get_cost(self.board.get_piece(node))
            except:
                print(node)
                print(len(self.board.get_board()))
                print(len(self.board.get_board()[0]))
                raise
            path_cost = self.cost_map.get_piece(curr_node)
            extended_path_cost = path_cost + move_cost
            last_node_cost = self.cost_map.get_piece(node)
            if self.cost_map.get_piece(
                node
            ) == None or extended_path_cost < self.cost_map.get_piece(node):

                self.cost_map.set_element(node, extended_path_cost)

                self.journey_map.set_element(node, curr_node)
                new_nodes.append(node)

        return new_nodes

        # else:
        #     if self.journey_map[node[0]][node[1]] >

    def move_heuristic(self):
        """
        Provide heuristic of distance remaining.
        """
        raise NotImplementedError

    @staticmethod
    def validate_L_move(delta):
        if (abs(delta.x) == 2 and abs(delta.y) == 1) or (abs(delta.x) == 1 and abs(delta.y) == 2):
            return True
        else:
            return False

    def validate_within_bounds(self, node):
        """
        Check if a particular falls within bound.
        Input: node = [y,x]
        Output: True if in bounds, False if outside
        """
        y_on_board = (node.x >= 0) and (node.x < self.board.get_height())
        x_on_board = (node.y >= 0) and (node.y < self.board.get_width())
        if x_on_board and y_on_board:
            return True
        else:
            self.error_context = "Moves are not contained on the board"
            return False

    def is_horizontal_motion_clear_of_barriers(self, start_x, stop_x, y, sign):
        """
        Checks if jogging horizontal will collide with barrier.
        """
        travel_pos = GridPos(start_x, y)  # create copy, rather than reference
        horizontal_path_clear = True
        while (travel_pos.x != stop_x): # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(sign, 0)  # take one step in horizontal direction
            if self.board.get_piece(travel_pos) == "B":
                horizontal_path_clear = False

        return horizontal_path_clear

    def is_vertical_motion_clear_of_barriers(self, start_y, stop_y, x, sign):
        """
        Checks if jogging vertical will collide with barrier
        """
        travel_pos = GridPos(x, start_y)  # create copy, rather than reference
        vertical_path_clear = True
        while (travel_pos.y != stop_y): # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(0, sign)  # take one step in horizontal direction
            if self.board.get_piece(travel_pos) == "B":
                vertical_path_clear = False

        return vertical_path_clear

    def validate_barrier_clear(self, curr_node, next_node, aggressive=False):
        """
        Check if a particular falls within bound.
        Input: node = [y,x]
        Output:
            True if path is clear of barriers
            False if barriers invalidate move
        Assumptions: Input moves are properly formatted (L-shaped and in-bounds).
        """
        delta = next_node - curr_node
        if self.validate_L_move(delta) == False:
            return  # the move is not valid (probably a teleport, so return without throwing an exception)

        sign = delta // abs(delta)

        # Horizontal first --> then vertical
        # S 1 2
        # . . 3
        horizontal_first_clear = self.is_horizontal_motion_clear_of_barriers(start_x=curr_node.x,
                                                                             stop_x=next_node.x,
                                                                             y=curr_node.y,
                                                                             sign=sign.x) and \
                                 self.is_vertical_motion_clear_of_barriers(start_y=curr_node.y,
                                                                           stop_y=next_node.y,
                                                                           x=next_node.x,
                                                                           sign=sign.y)


        # Vertical first --> then horizontal
        # S . .
        # 1 2 3
        vertical_first_clear = self.is_vertical_motion_clear_of_barriers(start_y=curr_node.y,
                                                                         stop_y=next_node.y,
                                                                         x=curr_node.x,
                                                                         sign=sign.y) and \
                               self.is_horizontal_motion_clear_of_barriers(start_x=curr_node.x,
                                                                           stop_x=next_node.x,
                                                                           y=next_node.y,
                                                                           sign=sign.x)

        return horizontal_first_clear or vertical_first_clear


        # # Horizontal first --> then vertical
        # # S 1 2
        # # . . 3
        # x_travel = 0
        # y_travel = 0
        # x_first_path = []
        # for x_travel in range(1, abs(delta.x) + 1):
        #     x_first_path.append( GridPos(curr_node.x, curr_node.y + x_travel * sign.x) )
        # for y_travel in range(1, abs(delta.y) + 1):
        #     # TODO: might be fine, but looks confusing...why x in the y loop?
        #     x_first_path.append(
        #         GridPos( curr_node.x + y_travel * sign.y, curr_node.y + x_travel * sign.x)
        #     )
        #
        # x_clear = True
        # for node in x_first_path:
        #     # print node
        #     # print self.board.get_element(node)
        #     if self.board.get_piece(node) == "B":
        #         x_clear = False
        # #         print "XPATH FAIL!!!"
        #
        #
        # # Vertical first --> then horizontal
        # # S . .
        # # 1 2 3
        # x_travel = 0
        # y_travel = 0
        # y_first_path = []
        # for y_travel in range(1, abs(delta.y) + 1):
        #     y_first_path.append(
        #         GridPos( curr_node.x + y_travel * sign.y, curr_node.y + x_travel * sign.x)
        #     )
        # for x_travel in range(1, abs(delta.x) + 1):
        #     y_first_path.append(
        #         GridPos( curr_node.x + y_travel * sign.y, curr_node.y + x_travel * sign.x)
        #     )
        #
        # y_clear = True
        # for node in y_first_path:
        #     # print node
        #     # print repr(self.board.get_element(node))
        #     if self.board.get_piece(node) == "B":
        #         y_clear = False
        #         # print "PATH FAIL!!!"
        #
        # if aggressive == True:
        #     # Absolutely no obstructions! Both must be clear
        #     return x_clear and y_clear
        # else:
        #     # or either path is open, we're clear
        #     return x_clear or y_clear

    def get_possible_nodes(self, curr_node):
        delta_moves = [
            GridPos(-2, -1),
            GridPos(-2, 1),
            GridPos(-1, -2),
            GridPos(-1, 2),
            GridPos(1, -2),
            GridPos(1, 2),
            GridPos(2, -1),
            GridPos(2, 1),
        ]

        new_nodes = []
        # TODO: looks like it's being initialized outside the loop...don't think that's needed though
        new_node = GridPos(-1,-1) # initialize to invalid value
        for move in delta_moves:
            # for i in range(len(curr_node)):  # loop over [y,x]
            #     new_node[i] = curr_node[i] + move[i]
            new_node = curr_node + move
            if self.validate_within_bounds(new_node) and self.validate_barrier_clear(curr_node, new_node):
                new_nodes.append(new_node)

        # TODO: Filter for going over barriers

        teleport = self.teleport(curr_node)
        if self.teleport(curr_node) is not None:
            new_nodes.append(teleport)

        return new_nodes

    def set_cost(self):
        """
        Might help for problem 5, when the objective changes
        """
        pass

    def get_cost(self, value):
        """
        Return cost for a move to a specific destination.
        """
        value_lookup = {
            "B": 100000,
            ".": 1,
            "W": 2,
            "R": 100000,  # infinite, if you want
            "T": 1,
            "L": 5,
            "S": 0,  # mute point, since costs acrue upon landing
            "E": 1,
        }  # Assuming 'E' is still '.' underneath
        return value_lookup[value]

    def teleport(self, curr_pos):
        """
        Returns the coupled teleport position.
        Assumes there are only 2 teleport positions.
        Input: None, assumes board is populated already.
        Output: The location [y,x] of the exit teleport.
        """
        tele = self.board.find_element("T")

        if curr_pos not in tele:
            return None  # No teleportation avaiable from here

        # TODO - this check should be upon board init - better to find out sooner
        if len(tele) != 2:
            raise Exception(
                "Incorrect number of teleporters discovered. Expected 2, found %i"
                % len(tele)
            )

        if tele[0] == curr_pos:
            return tele[1]
        if tele[1] == curr_pos:
            return tele[0]

    def display_knight(self, pos=None):
        """
        Displays the location of the knight on the board.
        """
        display_character = "K"
        if pos is None:
            pos = self.knight_pos
        pieces = {display_character: pos}
        self.board.display_board(pieces=pieces)

    def validate_pos_sequence(self, pos_sequence, rich_print=False):
        """
        Note: Problem 1 from the prompt

        Purpose:
            Validates that a sequence of moves is valid for the knight to make:
                - 2 spaces in a direction(x,y), 1 space in the other direction.
                - Remains in bounds


        Assumptions:
            Board exists: checked explicitly.
            Board is rectangular: assumed as property of a board.

        Inputs:
            move_sequence: A list of absolute positions, representing the target position after each move

        Output:
            bool: Whether the sequence of moves is valid
        """

        # Apply board conditions, if they exist
        if self.board is None:
            raise Exception(
                "Error: No board loaded. Load a board before moving your pieces."
            )

        first_iteration = True
        for pos in pos_sequence:
            if not self.validate_within_bounds(pos):
                return False

            # First iteration, we have no previous pos to compare against
            if first_iteration:
                first_iteration = False
            else:
                delta = pos_prev - pos

                if self.validate_L_move(delta):
                    pass
                else:
                    self.error_context = (
                        "2 adjascent positions represent a move that a"
                        "knight is not permitted to make."
                        "Last valid position:" + str(pos_prev)
                    )
                    return False

            if rich_print:
                self.display_knight(pos)
            pos_prev = pos

        return True


class KnightTester(unittest.TestCase):
    """
    Let the knight's gauntlet commence!
    """

    def setUp(self):
        """
        Setup the board, and place the knight
        """
        self.k = Knight("Boards/8x8_board.txt")
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
        positions = [GridPos(0, 0),
                     GridPos(2, 1),
                     GridPos(4, 0),
                     GridPos(3, 2),
                     GridPos(4, 4),
                     GridPos(6, 5)]

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

        positions = [GridPos(0, 0),
                     GridPos(2, 1),
                     GridPos(4, 0),
                     GridPos(3, 2),
                     GridPos(4, 4),
                     GridPos(6, 5)]

        print_buffer = StringIO()
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            valid = self.k.validate_pos_sequence(positions, rich_print=True)
        finally:
            sys.stdout = default_output
        # print self.k.error_context
        self.assertTrue(valid)
        # print print_buffer.getvalue()
        # It's not elegant, but it's the most direct
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
        positions = [
            GridPos(0, 0),
            GridPos(2, 1),
            GridPos(1, -1)]

        self.assertFalse(self.k.validate_pos_sequence(positions))
        self.assertEqual(self.k.error_context, "Moves are not contained on the board")

    def test_validate_node_sequence__fail_not_valid_for_knight(self):
        """
        Tests failure by falling off of the board
        """
        positions = [
            GridPos(0, 0),
            GridPos(2, 1),
            GridPos(4, 4)]

        self.assertFalse(self.k.validate_pos_sequence(positions))

        error_phrase = (
            "2 adjascent positions represent a move that a"
            "knight is not permitted to make."
        )
        self.assertRegex(self.k.error_context, error_phrase)

    @unittest.skip(
        "Never used this - didn't make sense to create methods "
        "for a specific instance."
    )
    def test_create_cost_board__pass(self):
        self.k.create_cost_board(self.k.board)
        self.assertEqual(self.k.cost_board.get_board()[0][0], 1)
        self.assertEqual(self.k.cost_board.get_board()[2][1], 0)

    def test_teleport__pass(self):
        """
        Verify that teleport is able to find both locations, and return the
        correct exit locations.
        """
        teleport_in = GridPos(11, 26)
        teleport_out = GridPos(23, 27)
        self.k = Knight("Boards/32x32_board.txt", teleport_in)
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
        # teleport_in = [11,26]
        # teleport_out = [23,27]
        self.k = Knight("Boards/32x32_board.txt", start_pos)
        out_pos = self.k.teleport(start_pos)
        self.assertEqual(out_pos, None)

    def test_teleport__fail_too_many_tp(self):
        """
        Verify that a poorly formed board is detected.
        """
        teleport_in = [11, 26]
        teleport_out = [23, 27]
        self.k = Knight("Boards/32x32_board.txt", teleport_in)
        self.k.board._board[15][20] = "T"
        with self.assertRaises(Exception):
            out_pos = self.k.teleport(teleport_in)

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
        nodes = self.k.get_possible_nodes(curr_node)
        expected_valid_nodes = [GridPos(0, 3),
                                GridPos(3, 0),
                                GridPos(2, 3),
                                GridPos(3, 2)]
        # These 4 nodes are expected, though order is not gauranteed
        for node in nodes:
            self.assertTrue(node in expected_valid_nodes)

        expected_omitted_node = [GridPos(0, 0),
                                 GridPos(3, -1),
                                 GridPos(2, -1),
                                 GridPos(-1, 2),
                                 GridPos(-1, 0)]
        for node in nodes:
            self.assertFalse(node in expected_omitted_node)

    def test_explore_moves__single_step(self):
        """
        A few extra checks, since python list copies tend to do everything by reference.
        """
        board_template = "Boards/8x8_board.txt"
        start_pos = GridPos(1, 1)
        self.k = Knight(board_template, start_pos)

        self.k.journey_map = board.Board(board_template)
        self.k.cost_map = board.Board(board_template)
        self.k.cost_map.reset_board()
        self.k.journey_map.reset_board()

        self.k.cost_map.set_element(start_pos, 0)

        # make sure the appropriate nodes are found
        nodes = self.k.explore_moves(start_pos)

        expected_valid_nodes = [GridPos(0, 3),
                                GridPos(3, 0),
                                GridPos(2, 3),
                                GridPos(3, 2)]
        # These 4 nodes are expected, though order is not guaranteed
        for node in nodes:
            self.assertTrue(node in expected_valid_nodes)

        expected_omitted_node = [GridPos(0, 0),
                                 GridPos(3, -1),
                                 GridPos(2, -1),
                                 GridPos(-1, 2),
                                 GridPos(-1, 0)]
        for node in nodes:
            self.assertFalse(node in expected_omitted_node)

        ###make sure the cost_map updates
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

        self.assertEqual(self.k.cost_map.get_board(), expected_cost_map)

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

        self.assertEqual(self.k.journey_map.get_board(), expected_journey_map)

    # TODO: figure out what this really tests
    def test_plan_path(self):
        """ """
        self.k.plan_path()

    # TODO: figure out what this really tests
    def test_reconstruct_path_8x8(self):
        self.k.plan_path()
        # print "*"*40
        path = self.k.reconstruct_path()
        for step in path:
            # print self.k.cost_map.get_element(step)
            my_str = "Cost: %i \t" % self.k.cost_map.get_piece(step)
            # print my_str + "Node: " + str(step)

    def test_reconstruct_path_32x32(self):

        self.k = Knight("Boards/32x32_board.txt", start_pos=GridPos(0, 0), target_pos=GridPos(31, 31))
        self.k.board.get_board()[5][8] = "."
        self.k.plan_path()

        # Show Journey
        path = self.k.reconstruct_path()
        print_str = ""
        for step in path:
            my_str = "Cost: %i \t" % self.k.cost_map.get_piece(step)
            print_str = print_str + my_str + "Node: " + str(step)

        journey = {}
        journey_cost = {}
        for step in enumerate(path):
            step_num = step[0]
            step_node = step[1]
            journey[step_num] = step_node
            journey_cost[self.k.cost_map.get_piece(step_node)] = step_node

        print(print_str)
        # self.k.cost_map.display_board(pieces = journey)
        self.k.board.display_board(pieces=journey)
        self.k.board.display_board(pieces=journey_cost)

    def test_validate_barrier_clear__pass(self):
        """
        Test that barriers can be detected appropriately.
        """
        self.k = Knight("Boards/32x32_board.txt", start_pos=GridPos(0, 0), target_pos=GridPos(31, 31))

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

    @unittest.skip("Deprecated: This is not what the prompt was asking, and I see no added value")
    def test_validate_barrier_clear__aggressive_corner(self):
        self.k = Knight("Boards/32x32_board.txt", start_pos=[0, 0], target_pos=[31, 31])

        curr_node = GridPos(6, 7)
        next_node = GridPos(8, 8)
        valid = self.k.validate_barrier_clear(curr_node, next_node, aggressive=True)
        self.assertFalse(valid)

        valid = self.k.validate_barrier_clear(curr_node, next_node, aggressive=False)
        self.assertTrue(valid)


if __name__ == "__main__":
    k = Knight("Boards/8x8_board.txt")
    unittest.main()
    # k.display_knight()
    # k.create_cost_board(k.board)

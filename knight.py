"""
Level 1: Call instantiate Knight(), and call self.validate_node_sequence
Level 2-4:

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


class Knight():



    def __init__(self, board_path, start_pos = None, target_pos = None):
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
                self.start_pos = self.board.find_element('S')[0] #assuming only 1
            except:
                self.start_pos = None
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if target_pos is None:
            try:
                self.target_pos = self.board.find_element('E')[0] #assuming only 1
            except:
                self.target_pos = None
        else:
            self.target_pos = target_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

    def review_path(self):
        raise NotImplementedError

    def plan_path(self):
        """
        """
        active_list  = [self.knight_pos] #Init list with a start pos

        #Initialize map of journey costs 
        start_pos = self.knight_pos
        self = Knight(self.board_path, start_pos)

        self.journey_map = board.Board(self.board_path)
        self.cost_map = board.Board(self.board_path)
        self.cost_map.reset_board()
        self.journey_map.reset_board()

        self.cost_map.set_element(start_pos,0)

        while True:
            # Rational moves are allowed for a knight, land on the board, and land
            # upon unexplored spaces
            exploratory_node = active_list.pop(0)
            print "Update:"
            self.display_knight(exploratory_node)
            new_nodes = self.explore_moves(exploratory_node)
            
            #conservative finish condition
            # if active_list == []:
            #     # report()
            #     return

            # Quick Finish condition (holds true in simple case)
            if self.target_pos in new_nodes:
                # report()

                print "Journey:"
                self.journey_map.display_board()
                print "Cost Map:"
                self.cost_map.display_board()
                print "Minimum Cost:\t%i" % self.cost_map.get_element(self.target_pos)
                return
            for new_node in new_nodes:
                active_list.append(new_node)

    def explore_moves(self, curr_node, move_heuristic = None):
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

        #find all desirable nodes to move to
        new_nodes = []
        for node in self.get_possible_nodes(curr_node):
            move_cost = self.get_cost(self.board.get_element(node))
            path_cost = self.cost_map.get_element(curr_node)
            extended_path_cost = path_cost + move_cost
            last_node_cost = self.cost_map.get_element(node)
            if ( self.cost_map.get_element(node) == None or
                 extended_path_cost < self.cost_map.get_element(node) ):
                    print '*'*30 
                    print node
                    print "path_cost:%i\tmove_cost:%i\textended_cost:%i\t" % (path_cost, move_cost,extended_path_cost)
                    self.cost_map.set_element(node,extended_path_cost)
                    self.journey_map.get_board()[node[0]][node[1]] = curr_node
                    new_nodes.append(node)

        return new_nodes

        # else:
        #     if self.journey_map[node[0]][node[1]] >

    def move_heuristic():
        """
        Provide heurist of distance remaining.
        """
        raise NotImplementedError

    def located_within_board(self, pos):
        y_on_board = (pos[0] >= 0) and (pos[0] <= self.board.get_height())
        x_on_board = (pos[1] >= 0) and (pos[1] <= self.board.get_width())
        if (x_on_board and y_on_board):
            return True
        else:
            self.error_context = "Moves are not contained on the board"
            return False

    def get_possible_nodes(self, curr_node):
        delta_moves = [[-2,-1],
                       [-2,1],
                       [-1,-2],
                       [-1,2],
                       [1,-2],
                       [1,2],
                       [2,-1],
                       [2,1]]

        new_nodes = []
        new_node = [None, None]
        for move in delta_moves:
            for i in range(len(curr_node)): #loop over [y,x]
                new_node[i] = curr_node[i] + move[i]
            if self.located_within_board(new_node):
                new_nodes.append(list(new_node))

        teleport = self.teleport(curr_node)
        if self.teleport(curr_node) is not None:
            new_nodes.append(teleport)

        return new_nodes

    def get_cost(self, value):
        """
        Return cost for a move to a specific destination.
        """
        value_lookup =  {'.':1,
                         'W':2,
                         'R':None, #infinite, if you want
                         'T':1,
                         'L':5,
                         'S':0, #mute point, since costs acrue upon landing
                         'E':1} #Assuming 'E' is still '.' underneath
        return value_lookup[value]

    def teleport(self, curr_pos):
        """
        Returns the coupled teleport position.
        Assumes there are only 2 teleport positions.
        Input: None, assumes board is populated already.
        Output: The location [y,x] of the exit teleport. 
        """
        tele = self.board.find_element('T')

        if curr_pos not in tele:
            return None #No teleportation avaiable from here

        #TODO - this check should be upon board init - better to find out sooner
        if len(tele) != 2:
            raise Exception("Incorrect number of teleporters discovered. Expected 2, found %i" % len(tele))

        if tele[0] == curr_pos:
            return tele[1]
        if tele[1] == curr_pos:
            return tele[0]

    def create_cost_board(self, board):
        """
        May have jumped the gun here...doesn't seem to be needed.
        """
        self.cost_board = self.board
        cost_board = self.cost_board.get_board()
        for row in enumerate(self.cost_board.get_board()):
            for element in enumerate(row[1]):
                value = element[1]
                cost_board[row[0]][element[0]] = self.get_cost(value)

        # self.cost_board.display_board()

    def display_knight(self, pos = None):
        """
        Displays the location of the knight on the board.
        """
        display_character = 'K'
        if pos == None:
            pos = self.knight_pos
        pieces = {display_character: pos}
        self.board.display_board(display_character, pieces = pieces)

    def validate_node_sequence(self, node_sequence, rich_print = False):
        """
        Note: Problem 1

        Purpose:
            Validate moves to be of the format allowable by a knight...
            2 spaces in a direction(x,y), 1 space in the other direction.

        Assumptions:
            Board exists: checked explicitly.
            Board is rectangular: assumed as property of a board.

        Inputs:
            move_sequence: A list of positions of the form [x,y]

        Outputs:
            True/False validity of move
        """

        #Apply board conditions, if they exist
        if self.board is None:
            raise Exception("Error: No board loaded. Load a board before moving your pieces.")

        width = self.board.get_width()
        height = self.board.get_height()
        first_iteration = True
        for pos in node_sequence:
            if self.located_within_board(pos):
                pass
            else:
                return False

            #First iteration, we have no previous pos to compare against
            if first_iteration:
                first_iteration = False
            else:
                dx = pos_prev[0] - pos[0]
                dy = pos_prev[1] - pos[1]
            

                #Is the delta-pos an L-shaped knight move?
                if (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2):
                    pass
                else:
                    self.error_context = ("2 adjascent positions represent a move that a"
                                          "knight is not permitted to make."
                                           "Last valid position:" + str(pos_prev))
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
        self.k = Knight('8x8_board.txt')
        self.str_board_truth = self.k.board

    def test_display_knight__pass(self):
        """
        Verify that display displays the board with the knight properly placed.
        """
        import sys
        import StringIO

        str_board_ground_truth = ( ". . . . . . . .\n"
                                   ". . . . . . . .\n"
                                   ". K . . . . . .\n"
                                   ". . . . . . . .\n"
                                   ". . . . . E . .\n"
                                   ". . . . . . . .\n"
                                   ". . . . . . . .\n"
                                   ". . . . . . . .")

        print_buffer = StringIO.StringIO()
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            self.k.display_knight()
        finally:    
            sys.stdout = default_output


        #Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(print_buffer.getvalue(), '\n' + str_board_ground_truth + '\n' )

    def test_validate_node_sequence__pass(self):
        """
        Tests basic moves, including 0,0 edge case.
        """
        positions = [[0,0],
                     [2,1],
                     [4,0],
                     [3,2],
                     [4,4],
                     [6,5]]

        valid = self.k.validate_node_sequence(positions)
        # print self.k.error_context
        self.assertTrue(valid)

    def test_validate_node_sequence__rich_print(self):
        """
        Tests basic moves, including 0,0 edge case.
        """
        import StringIO
        import sys
        positions = [[0,0],
                     [2,1],
                     [4,0],
                     [3,2],
                     [4,4],
                     [6,5]]

        print_buffer = StringIO.StringIO()
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            valid = self.k.validate_node_sequence(positions, rich_print = True)
        finally:    
            sys.stdout = default_output
        # print self.k.error_context
        self.assertTrue(valid)
        # print print_buffer.getvalue()
        #It's not elegant, but it's the most direct
        expected_output =  ("\nK . . . . . . .\n"
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
                            ". . . . . . . .\n")

        self.assertEqual(print_buffer.getvalue(), expected_output)

    def test_validate_node_sequence__fail_move_off_board(self):
        """
        Tests failure by falling off of the board
        """
        positions = [[0,0],
                     [2,1],
                     [1,-1]]

        self.assertFalse(self.k.validate_node_sequence(positions))
        self.assertEqual(self.k.error_context,
                         "Moves are not contained on the board")

    def test_validate_node_sequence__fail_not_valid_for_knight(self):
        """
        Tests failure by falling off of the board
        """
        positions = [[0,0],
                     [2,1],
                     [4,4]]

        self.assertFalse(self.k.validate_node_sequence(positions))

        error_phrase = ("2 adjascent positions represent a move that a"
                        "knight is not permitted to make.")
        self.assertRegexpMatches(self.k.error_context, error_phrase)

    def test_create_cost_board__pass(self):
        self.k.create_cost_board(self.k.board)
        print "!@#$%^"*10
        self.k.cost_board.display_board()
        self.assertEqual(self.k.cost_board.get_board()[0][0], 1)
        self.assertEqual(self.k.cost_board.get_board()[2][1], 0)
        
    def test_teleport__pass(self):
        """
        Verify that teleport is able to find both locations, and return the 
        correct exit locations.
        """
        teleport_in = [11,26]
        teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', teleport_in)
        # print '\n'
        # self.k.display_knight()
        out_pos = self.k.teleport(teleport_in)
        self.assertEqual(out_pos, teleport_out)

    def test_teleport__no_tele_access(self):
        """
        Verify that teleport is able to find both locations, and return the 
        correct exit locations.
        """
        start_pos = [15,20]
        # teleport_in = [11,26]
        # teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', start_pos)
        out_pos = self.k.teleport(start_pos)
        self.assertEqual(out_pos, None)

    def test_teleport__fail_too_many_tp(self):
        """
        Verify that a poorly formed board is detected.
        """
        teleport_in = [11,26]
        teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', teleport_in)
        self.k.board.board[15][20] = 'T'
        with self.assertRaises(Exception):
            out_pos = self.k.teleport(teleport_in)

    def test_located_within_board(self):
        self.assertTrue(self.k.located_within_board([0,0]))
        self.assertTrue(self.k.located_within_board([0,1]))
        self.assertTrue(self.k.located_within_board([4,5]))
        self.assertFalse(self.k.located_within_board([-1,0]))
        self.assertFalse(self.k.located_within_board([-2,-5]))

    def test_get_possible_nodes(self):
        """
        Verify that the correct nodes are returned.
        """
        curr_node = [1,1]
        nodes = self.k.get_possible_nodes(curr_node)
        expected_valid_nodes = [[0,3],[3,0],[2,3],[3,2]]
        #These 4 nodes are expected, though order is not gauranteed
        for node in nodes:
            self.assertTrue(node in expected_valid_nodes)


        expected_omitted_node = [[0,0],[3,-1],[2,-1],[-1,2],[-1,0]]
        for node in nodes:
            self.assertFalse(node in expected_omitted_node)

    def test_explore_moves__single_step(self):
        """
        A few extra checks, since python list copies tend to do everything by reference.
        Future cleanup: Probably should have started with NumPy.
        """
        board_template = '8x8_board.txt'
        start_pos = [1,1]
        self.k = Knight(board_template, start_pos)

        self.k.journey_map = board.Board(board_template)
        self.k.cost_map = board.Board(board_template)
        self.k.cost_map.reset_board()
        self.k.journey_map.reset_board()

        self.k.cost_map.set_element(start_pos,0)

        ###make sure the appropriate nodes are found
        nodes = self.k.explore_moves(start_pos)

        expected_valid_nodes = [[0,3],[3,0],[2,3],[3,2]]
        #These 4 nodes are expected, though order is not gauranteed
        for node in nodes:
            self.assertTrue(node in expected_valid_nodes)

        expected_omitted_node = [[0,0],[3,-1],[2,-1],[-1,2],[-1,0]]
        for node in nodes:
            self.assertFalse(node in expected_omitted_node)

        ###make sure the cost_map updates
        # self.k.cost_map.display_board()
        expected_cost_map = [[None,None,None,1,None,None,None,None],
                             [None,0,None,None,None,None,None,None],
                             [None,None,None,1,None,None,None,None],
                             [1,None,1,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None]]

        self.assertEqual(self.k.cost_map.get_board(), expected_cost_map)

        ###make sure the journey_map updates
        # self.k.journey_map.display_board()

        expected_journey_map = [[None,None,None,[1,1],None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,[1,1],None,None,None,None],
                             [[1,1],None,[1,1],None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None]]

        self.assertEqual(self.k.journey_map.get_board(), expected_journey_map)

    def test_plan_path(self):
        self.k.plan_path()


if __name__ == '__main__':
    k = Knight('8x8_board.txt')
    # k.display_knight()
    k.create_cost_board(k.board)
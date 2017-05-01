"""
Level 1: Call instantiate Knight(), and call self.validate_pos_sequence
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



    def __init__(self, board_path, knight_start_pos = None):
        """
        Initialize the knight on the board.
        Inputs:
            board_path:
            knight_start_pos: Expects input [row,col].
                              Finds 'S' on the board by default.
        """

        self.board = board.Board(board_path)
        if knight_start_pos is None:
            self.knight_pos = self.board.find_element('S')[0] #assuming only 1
        else:
            self.knight_pos = knight_start_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

    def plan_path():
        raise NotImplementedError

    def move(self):
        raise NotImplementedError
        self.actions = [[-2,-1],
                       [-2,1],
                       [-1,-2],
                       [-1,2],
                       [1,-2],
                       [1,2],
                       [2,-1],
                       [2,1],
                       self.teleport()]

    def get_cost(self, value):
        """
        Return cost for a move to a specific destination.
        """
        value_lookup =  {'.':1,
                         'W':2,
                         'R':None, #infinite, if you want
                         'T':1,
                         'L':5,
                         'S':1, #Assuming 'S' is still '.' underneath
                         'E':0}
        return value_lookup[value]

    def teleport(self):
        """
        Returns the coupled teleport position.
        Assumes there are only 2 teleport positions.
        Input: None, assumes board is populated already.
        Output: The location [y,x] of the exit teleport. 
        """
        tele = self.board.find_element('T')

        if self.knight_pos not in tele:
            return None #No teleportation avaiable from here

        if len(tele) != 2:
            raise Exception("Incorrect number of teleporters discovered. Expected 2, found %i" % len(tele))

        if tele[0] == self.knight_pos:
            return tele[1]
        if tele[1] == self.knight_pos:
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

    def display_knight(self):
        """
        Displays the location of the knight on the board.
        """
        display_character = 'K'
        pieces = {display_character: self.knight_pos}
        self.board.display_board(display_character, pieces)

    def validate_pos_sequence(self, pos_sequence, print_states = False):
        """
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
        for pos in pos_sequence:
            y_on_board = (pos[0] >= 0) and (pos[0] <= height)
            x_on_board = (pos[1] >= 0) and (pos[1] <= width)
            if not (x_on_board and y_on_board):
                self.error_context = "Moves are not contained on the board"
                return False

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

            pos_prev = pos

        return True

    def create_heuristic():
        """
        Provide crude estimate of distance remaining.
        """
        pass


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
        self.assertEqual(print_buffer.getvalue(), str_board_ground_truth + '\n' )

    def test_validate_move__pass(self):
        """
        Tests basic moves, including 0,0 edge case.
        """
        positions = [[0,0],
                     [2,1],
                     [4,0],
                     [3,2],
                     [4,4],
                     [6,5]]

        valid = self.k.validate_pos_sequence(positions)
        # print self.k.error_context
        self.assertTrue(valid)

    def test_validate_pos_sequence__fail_move_off_board(self):
        """
        Tests failure by falling off of the board
        """
        positions = [[0,0],
                     [2,1],
                     [1,-1]]

        self.assertFalse(self.k.validate_pos_sequence(positions))
        self.assertEqual(self.k.error_context,
                         "Moves are not contained on the board")

    def test_validate_pos_sequence__fail_not_valid_for_knight(self):
        """
        Tests failure by falling off of the board
        """
        positions = [[0,0],
                     [2,1],
                     [4,4]]

        self.assertFalse(self.k.validate_pos_sequence(positions))

        error_phrase = ("2 adjascent positions represent a move that a"
                        "knight is not permitted to make.")
        self.assertRegexpMatches(self.k.error_context, error_phrase)

    def test_create_cost_board__pass(self):
        self.k.create_cost_board(self.k.board)
        self.assertEqual(self.k.cost_board.get_board()[0][0], 1)
        self.assertEqual(self.k.cost_board.get_board()[4][5], 0)
        
    def test_teleport__pass(self):
        """
        Verify that teleport is able to find both locations, and return the 
        correct exit locations.
        """
        teleport_in = [11,26]
        teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', knight_start_pos = teleport_in)
        # print '\n'
        # self.k.display_knight()
        out_pos = self.k.teleport()
        self.assertEqual(out_pos, teleport_out)

    def test_teleport__no_tele_access(self):
        """
        Verify that teleport is able to find both locations, and return the 
        correct exit locations.
        """
        start_pos = [15,20]
        # teleport_in = [11,26]
        # teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', knight_start_pos = start_pos)
        # print '\n'
        # self.k.display_knight()
        out_pos = self.k.teleport()
        self.assertEqual(out_pos, None)

    def test_teleport__fail_too_many_tp(self):
        """
        Verify that a poorly formed board is detected.
        """
        teleport_in = [11,26]
        teleport_out = [23,27]
        self.k = Knight('32x32_board.txt', knight_start_pos = teleport_in)
        self.k.board.board[15][20] = 'T'
        # print '\n'
        # self.k.display_knight()
        with self.assertRaises(Exception):
            out_pos = self.k.teleport()

if __name__ == '__main__':
    k = Knight('8x8_board.txt')
    # k.display_knight()
    k.create_cost_board(k.board)
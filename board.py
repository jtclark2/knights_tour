"""
Created by: Trevor Clark
Created on: 4/27/2017
Future Improvements: 
"""

import unittest

class Board():

    def __init__(self, board_path = None):
        if board_path is None:
            self.board = None
        else:
            self.read_board(board_path)

    def _board_as_str(self, board=None):
        """
        Purpose: Take the 2D board and turn it into a str
        Inputs: board
        Outputs: str representation of board (matches file and convenient display)

        Note: While board is intrinsic to this class, the str repr is not. It 
            may require alteration to show pieces overlaid on the board, so we
            allow board as an explicit input arg, with self.board as the
            default.
        """
        if board is None:
            assert(self.board is not None)
            board = [row for row in self.board]

        board_str = ''
        for row in board: 
            for element in row:
                board_str = board_str + ("%s " % element )
            board_str = board_str[:-1]  #remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  #remove trailing '\n'
        return board_str

    def reset_board(self, value = None):
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                self.set_element([i,j], value)

    def get_board(self):
        return self.board

    def get_element(self, pos):
        """
        Retrieve an element by index.
        Input: Index ([y,x])
        Output: Element Value (assumed to be a char)
        """
        return self.board[pos[0]][pos[1]]

    def set_element(self,pos,value):
        self.board[pos[0]][pos[1]] = value


    def find_element(self, search_value):
        """
        Finds a specific element on the board. Finds only the first, 
        and returns its location.
        Inputs: The element value to search for.
        Outputs: List of element locations [y, x]
        """
        matches = []
        for row in enumerate(self.board):
            for element in enumerate(row[1]):
                if element[1] == search_value:
                    matches.append([row[0], element[0]])
        return matches

    def get_width(self):
        """
        Calculate and return the width, or number of columns.
        """
        assert(self.board)
        return len(self.board[0])

    def get_height(self):
        """
        Calculate and return the height, or number of rows.
        """
        assert(self.board)
        return len(self.board)

    def read_board(self,file_path):
        """
        Reads the board and loads into a list of lists.
        File Format: ' ' delimits elements in a row, and '\n' delimits between rows
        Assumptions/Limitations: Does not handle/pad non-rectangular boards.
        """
        with open(file_path,"r") as file:
            raw_board = file.read()

        rows = raw_board.split('\n')
        self.board = []
        for row in rows:
            self.board.append(row.split(' '))
        # return self.boards

    def write_board(self, board = None, write_path = "./temp_board"):
        """
        Writes a copy of the boards current state as a txt file.

        Inputs:
            board: python list of lists, where element = board[row][col].

            write_path: path that file will be written to
                File Format: grid delimited by ' ' between elements and '\n' between rows.

        Outputs: None

        """

        # construct string for file write
        board_str = self._board_as_str(board)

        with open(write_path,"w") as file:
            file.write(board_str)

    def display_board(self, board = None, pieces = None):
        """
        Prints a repr of the board to the screen.

        Inputs:
            board: python list of lists, where element = board[row][col].
            pieces: Optional
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        #Clean copy, so python doesn't pass the reference
        board_copy = [row[:] for row in self.board] 
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece][0]][pieces[piece][1]] = piece

        print '\n' + self._board_as_str(board_copy)

class BoardTester(unittest.TestCase):

    def setUp(self):
        """
        Init board for each test.
        """
        self.B = Board()
        self.board_ground_truth =  [['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','S','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','E','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.']]

        self.str_board_ground_truth = ( ". . . . . . . .\n"
                                        ". . . . . . . .\n"
                                        ". S . . . . . .\n"
                                        ". . . . . . . .\n"
                                        ". . . . . E . .\n"
                                        ". . . . . . . .\n"
                                        ". . . . . . . .\n"
                                        ". . . . . . . .")

    def test_get_element_pass(self):
        self.B.board = self.board_ground_truth
        element = self.B.get_element([2,1])
        self.assertEqual(element, 'S')

    @unittest.skip("Seemed excessive for such a simple func..."
                   "could add for increased throughness.")
    def test_get_element_fail(self):
        pass

    def test_get_board(self):
        """
        Grabs the actual grid, list of lists, in the board object.
        """
        self.assertEqual(self.B.board, self.B.get_board())

    def test_get_width(self):
        self.B.board = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_width(), 8)

    def test_get_height(self):
        self.B.board = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_height(), 7)

    def test_read_board_data_verification(self):
        """
        Purpose: Verify that values are read into each position correctly
        """             
        self.B.read_board("./8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board):
            for element_ground, element_read in zip(row_ground, row_read):
                self.assertEqual(element_ground, element_read)

    def test_read_board_data_verification_fail(self):
        """
        Purpose: Verify that values are read into each position correctly.
        Note: A negative case on a literal match is probably overkill, but
              quick enough to implement, so...
        """

        self.board_ground_truth[5][3] = 'S'  #Overwrite the correct data

        match = True
        self.B.read_board("./8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board):
            for element_ground, element_read in zip(row_ground, row_read):
                if element_ground != element_read:
                    match = False
        self.assertFalse(match)

    def test_read_board__dimension_match(self):
        """
        Purpose: Verify that the board dimensions match the .txt file
        Assumptions: 8x8_board.txt is well formatted, and represents an 8x8
        """
        self.B.read_board("./8x8_board.txt")
        self.assertEqual(len(self.B.board), 8) #column count
        self.assertEqual(len(self.B.board[0]), 8) #row count

    def test_write_board__pass(self):
        """
        Purpose: Verify that data structure is written correctly.
                 Correctly is defined as a grid, with elements in a row separated
                 by ' ', and rows separated by '\n'
        Assumptions: read_board() is also operating correctly. 
                     Technically bad practice for a 'unit' test, but
                     low risk and pragmatic in this simple case.
        """

        self.B.write_board(self.board_ground_truth)

        #Read test data
        with open("8x8_board.txt","r") as file:
            raw_board_ground_truth = file.read()
        with open("temp_board","r") as file:
            raw_board_written = file.read()

        self.assertEqual(raw_board_ground_truth, raw_board_written)

    def test_display_board__pass(self):
        """
        Purpose: Verify that base case of board display works
        """
        import sys
        import StringIO

        print_buffer = StringIO.StringIO()
        self.B.board = self.board_ground_truth
        
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            self.B.display_board(self.board_ground_truth)
        finally:    
            sys.stdout = default_output


        #Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(print_buffer.getvalue(), '\n' + self.str_board_ground_truth + '\n' )

    def test_display_board__input_pieces(self):
        """
        Purpose: Verify board display works when passing in chars.
        """
        import sys
        import StringIO

        print_buffer = StringIO.StringIO()
        self.B.board = self.board_ground_truth
        str_board = ('A' + self.str_board_ground_truth[1:])
        str_board = (str_board[:34]+'K'
                    +str_board[34+1:])
        pieces = {'A': [0,0], 'K': [2,1]}
        
        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            self.B.display_board(self.board_ground_truth, pieces)
        finally:    
            sys.stdout = default_output


        # print print_buffer.getvalue()
        # print "Truth:"
        # print str_board + '\n'
        #Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(print_buffer.getvalue(), '\n'+ str_board + '\n' )

    def test_find_element__pass_single_element(self):
        self.B.board = self.board_ground_truth
        pos = self.B.find_element('S')[0]
        self.assertEqual(pos, [2,1])

    def test_find_element__element_DNE(self):
        self.B.board = self.board_ground_truth
        pos = self.B.find_element(5)
        self.assertEqual(pos, [])

    def test_reset_board(self):
        self.B.board = self.board_ground_truth
        self.B.reset_board()
        self.assertEqual(self.B.get_board(),[[None]*8]*8)

    def test_set_element(self):
        pos = [2,7]
        value = 5

        self.board_ground_truth =  [['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','S','.','.','.','.','.',5],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','E','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.'],
                                   ['.','.','.','.','.','.','.','.']]

        self.B.board = self.board_ground_truth
        self.B.set_element(pos, value)
        self.assertEqual(self.board_ground_truth, self.B.board)

    @unittest.skip("Just Experimenting.")
    def test_print_intercept(self):
        import sys
        import StringIO
        print_buffer = StringIO.StringIO()
        sys.stdout = print_buffer
        print "intercepted?"
        sys.stdout = sys.__stdout__
        print print_buffer.getvalue()

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoardTester)
    unittest.TextTestRunner().run(suite)

"""
Created by: Trevor Clark
Created on: 4/27/2017
"""
from .grid_pos import GridPos
from .user_interface import TextUI


class GameMechanics:
    """
    Manages the "board", simple object in that stores the state of the board in memory.
        - Stores the object
        - read/write capabilities
        - find/read value of pieces on various spaces in the grid
    Decoupled from any gameplay.
    """

    def __init__(self, board_path=None, UI=TextUI):
        if board_path is None:
            # TODO: Rename to board_array (so as not to be confused with the class and module)
            self._board_grid = None
        else:
            self.load_board(board_path)

        self.UI = UI

    ################ Validation of compliance with game rules ##################

    @staticmethod
    def validate_L_move(delta):
        """
        Return whether a move is valid for a knight. Does it move 2 spaces in one direction, and 1 in the other.
        Does NOT check boundaries or Barriers.
        """
        if (abs(delta.x) == 2 and abs(delta.y) == 1) or (
            abs(delta.x) == 1 and abs(delta.y) == 2
        ):
            return True
        else:
            return False

    def validate_within_bounds(self, target_pos):
        """
        Check if a particular position is in bounds. Barriers are considered out-of-bounds.
        Input: Target position
        Output: True if in bounds, False if outside
        """
        y_on_board = (target_pos.x >= 0) and (target_pos.x < self.get_height())
        x_on_board = (target_pos.y >= 0) and (target_pos.y < self.get_width())


        if x_on_board and y_on_board:
            value = self.get_value(target_pos)
            if value == "B" or value == "R":
                return False
            else:
                return True
        else:
            # Not really an error...just answering no to the queston, "are you in bounds?"
            # raise(IndexError("Moves are not contained on the board"))
            return False

    # TODO
    def _is_horizontal_motion_clear_of_barriers(self, start_x, stop_x, y, sign):
        """
        Checks if jogging horizontal will collide with barrier.
        """
        travel_pos = GridPos(start_x, y)  # create copy, rather than reference
        horizontal_path_clear = True
        while travel_pos.x != stop_x:  # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(sign, 0)  # take one step in horizontal direction
            if self.get_value(travel_pos) == "B":
                horizontal_path_clear = False

        return horizontal_path_clear

    # TODO
    def _is_vertical_motion_clear_of_barriers(self, start_y, stop_y, x, sign):
        """
        Checks if jogging vertical will collide with barrier
        """
        travel_pos = GridPos(x, start_y)  # create copy, rather than reference
        vertical_path_clear = True
        while travel_pos.y != stop_y:  # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(0, sign)  # take one step in horizontal direction
            if self.get_value(travel_pos) == "B":
                vertical_path_clear = False

        return vertical_path_clear

    # TODO: rewrite to add the 3rd case...not sure if I delete what's there, or build on it
    def validate_barrier_clear(self, curr_node, next_node):
        """
        Check if a knight's movement will collide with a barrier.
        The knight's movement only defines an endpoint, not a path. This method recognizes 3 different paths are
        possible. Consider the 2 move direction to be "long", and the 1 move driection to be "short".
        There are 8 possible moves a knight can make, but they are all symmetrical. For each move, there are 3
        theoretical routes that could be taken, each taking 3 steps:
            - long, long, short
            - long, short long
            - short, long, long
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

        # long, long, short

        # Horizontal first --> then vertical
        # S 1 2
        # . . 3
        horizontal_first_clear = self._is_horizontal_motion_clear_of_barriers(
            start_x=curr_node.x, stop_x=next_node.x, y=curr_node.y, sign=sign.x
        ) and self._is_vertical_motion_clear_of_barriers(
            start_y=curr_node.y, stop_y=next_node.y, x=next_node.x, sign=sign.y
        )

        # Vertical first --> then horizontal
        # S . .
        # 1 2 3
        vertical_first_clear = self._is_vertical_motion_clear_of_barriers(
            start_y=curr_node.y, stop_y=next_node.y, x=curr_node.x, sign=sign.y
        ) and self._is_horizontal_motion_clear_of_barriers(
            start_x=curr_node.x, stop_x=next_node.x, y=next_node.y, sign=sign.x
        )

        return horizontal_first_clear or vertical_first_clear

    def get_possible_moves(self, curr_pos):
        """
        From any position, return a list of all valid moves. That includes any knight's move that would stay on the
        board, and any teleports.
        """
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

        new_positions = []
        for move in delta_moves:
            new_pos = curr_pos + move
            if self.validate_within_bounds(new_pos) and \
               self.validate_barrier_clear(curr_pos, new_pos):
                new_positions.append(new_pos)

        teleport = self.teleport(curr_pos)
        if self.teleport(curr_pos) is not None:
            new_positions.append(teleport)

        return new_positions

    def get_cost(self, value):
        """
        Return cost for landing on a specific location (ie: the cost of the move).
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
        }  # We assume 'E' is still '.' underneath
        return value_lookup[value]

    def teleport(self, curr_pos):
        """
        Returns the coupled teleport position.
        Assumptions:
            There are only 2 teleport positions (for more, we'd need to start adding IDs)
        Input: None
        Output: The location [y,x] of the exit teleport.
        """

        # TODO: Consider 2 generalizations
        #  1) multiple sets of teleport networks
        #       mark as "T[id]", and then find_all_elements with that id, rather than all teleports
        #  2) teleport networks with >= 2 nodes
        #       return all teleport locations that are not self

        # No teleportation available from here
        if self.get_value(curr_pos) != "T":
            return None

        teleports = self.find_all_elements("T")

        if len(teleports) != 2:
            print("Board does not have 2 teleports. Don't know where it leads, and I was always told not to venture through mystery portals.")
            return None

        # If there are 2, they connect, so just return the other
        if teleports[0] == curr_pos:
            return teleports[1]
        if teleports[1] == curr_pos:
            return teleports[0]

    def validate_pos_sequence(self, pos_sequence):
        """
        Note: Addresses prompt: problem 1

        Purpose:
            Validates that a sequence of moves is valid for the knight to make:
                - 2 spaces in a direction(x,y), 1 space in the other direction.
                - Remains in bounds

        Assumptions:
            Board has been defined: checked explicitly.

        Inputs:
            move_sequence: A list of absolute positions, representing the target position after each move

        Output:
            bool: Whether the sequence of moves is valid
        """
        pos_prev = pos_sequence[0]

        for pos in pos_sequence[1:]:
            if not self.validate_within_bounds(pos):
                return False

            # First iteration, we have no previous pos to compare against
            delta = pos_prev - pos

            if self.validate_L_move(delta):
                pass
            else:
                return False

            pos_prev = pos

        return True

    ################# Manipulation of the board (this will be gutted when we switch to numpy) ############

    # TODO: Consider using kwargs
    def display_board(self, pieces=None, value_width=1):
        """
        Displays a copy of the board.

        Inputs:
            board: Board object
            pieces (Optional):
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        TextUI.display_board(self._board_grid, pieces, value_width=value_width)

    def reset_board(self, value=None):
        """
        Set all spoces on the board to a specific value
        """
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                self.set_element(GridPos(i, j), value)

    # TODO: Consider removing this entirely...only needs to be exposed for testing
    @property
    def grid(self):
        """
        Getter for the main data object of this class, a grid representing a board
        """
        #TODO: make sense when board was a property for backing var _board...not sure now
        return self._board_grid

    def get_value(self, pos):
        """
        Retrieve an element by index.
        Input: Index pos
        Output: Element/piece Value
        """
        return self._board_grid[pos.x][pos.y]

    def set_element(self, pos, value):
        self._board_grid[pos.x][pos.y] = value

    def find_all_elements(self, search_value):
        """
        Finds all locations of a specific element on the board.
        Inputs: The element value to search for.
        Outputs: List of element locations [y, x]
        """
        matches = []
        for row in enumerate(self._board_grid):
            for element in enumerate(row[1]):
                if element[1] == search_value:
                    matches.append(GridPos(row[0], element[0]))
        return matches

    def get_width(self):
        """
        Get the width, or number of columns of the board.
        """
        assert self._board_grid
        return len(self._board_grid[0])

    def get_height(self):
        """
        Get the height, or number of rows of the board.
        """
        assert self._board_grid
        return len(self._board_grid)

    def load_board(self, file_path):
        """
        TODO: should probably just use 2D numpy array
        Reads the board from a text file, parsing and loading into memory
        File Format: ' ' delimits elements in a row, and '\n' delimits between rows
        Assumptions/Limitations: All boards must be rectangular, though not rectangular problems can be formatted
        by adding Barriers ("B") to the unavailable space.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            board_str = file.read()

        rows = board_str.split("\n")
        self._board_grid = []
        for row in rows:
            self._board_grid.append(row.split(" "))

    def write_board(self, board=None, write_path="Boards/temp_board.txt"):
        """
        Writes a copy of the boards current state as a txt file.
        Inputs:
            board: python list of lists, where element = board[row][col].

            write_path: path that file will be written to
                File Format: grid delimited by ' ' between elements and '\n' between rows.

        Outputs: None

        Side Effects: Writes the board
        """
        board_str = self.board_to_str(board)
        with open(write_path, "w", encoding="utf-8") as file:
            file.write(board_str)

    @staticmethod
    def board_to_str(board):
        """
        Purpose: Take the 2D board and turn it into a str
        Inputs: board
        Outputs: str representation of board (matches file and convenient display)

        Note: While board is intrinsic to this class, the str repr is not. It
            may require alteration to show pieces overlaid on the board, so we
            allow board as an explicit input arg, with self.board as the
            default.
        """
        board_str = ""
        for row in board:
            for element in row:
                board_str = board_str + ("%s " % element)
            board_str = board_str[:-1]  # remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  # remove trailing '\n'
        return board_str


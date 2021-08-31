"""
Purpose: Provide the rules of the game, governing legal moves and cost of those moves

Created by: Trevor Clark
Created on: 4/27/2017
"""
from .grid_pos import GridPos
from .user_interface import TextUI
from .pieces import Pieces


class GameEngine:
    """
    Manages the "board", simple object in that stores the state of the board in memory.
        - Stores the object
        - read/write capabilities
        - find/read value of pieces on various spaces in the grid
    Decoupled from any gameplay.
    """

    def __init__(self, board, UI=TextUI):
        self.board = board
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
        y_on_board = (target_pos.x >= 0) and (target_pos.x < self.board.get_height())
        x_on_board = (target_pos.y >= 0) and (target_pos.y < self.board.get_width())


        if x_on_board and y_on_board:
            value = self.board.get_value(target_pos)
            if value == Pieces.BARRIER.value or value == Pieces.ROCK.value:
                return False
            else:
                return True
        else:
            # Not really an error...just answering no to the queston, "are you in bounds?"
            # raise(IndexError("Moves are not contained on the board"))
            return False

    def _is_horizontal_motion_clear_of_barriers(self, start_x, stop_x, y, sign):
        """
        Checks if jogging horizontal will collide with barrier.
        """
        travel_pos = GridPos(start_x, y)  # create copy, rather than reference
        horizontal_path_clear = True
        while travel_pos.x != stop_x:  # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(sign, 0)  # take one step in horizontal direction
            if self.board.get_value(travel_pos) == Pieces.BARRIER.value:
                horizontal_path_clear = False

        return horizontal_path_clear

    def _is_vertical_motion_clear_of_barriers(self, start_y, stop_y, x, sign):
        """
        Checks if jogging vertical will collide with barrier
        """
        travel_pos = GridPos(x, start_y)  # create copy, rather than reference
        vertical_path_clear = True
        while travel_pos.y != stop_y:  # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(0, sign)  # take one step in horizontal direction
            if self.board.get_value(travel_pos) == Pieces.BARRIER.value:
                vertical_path_clear = False

        return vertical_path_clear

    def validate_barrier_clear(self, curr_node, next_node):
        """
        Check if a knight's movement will collide with a barrier.
        The knight's movement only defines an endpoint, not a path. This method recognizes 2 different paths that are
        possible, which are the 2 ways you could imagine the 'L' shape being laid onto the board. Technically, a third
        pattern is possible (a staircase shape through the middle), but was not explicit about what it means for a
        barrier to lie in the path, so I decided a knight's path is to move in an 'L' shape.

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
        try:
            value_lookup = {
                Pieces.BARRIER.value: None, # Can't visit this space
                Pieces.EMPTY.value: 1,
                Pieces.WATER.value: 2,
                Pieces.ROCK.value: None, # Can't visit this space
                Pieces.TELEPORT.value: 1,
                Pieces.LAVA.value: 5,
                Pieces.START.value: 0,  # mute point, since costs acrue upon landing
                Pieces.END.value: 1,
            }  # 'E' is empty (eg: don't allow it to be water, lava, teleport, etc.)
            return value_lookup[value]
        except KeyError as err:
            raise KeyError(f"KeyError: Could not lookup value for {type(value)}: {value}") from err

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
        if self.board.get_value(curr_pos) != Pieces.TELEPORT.value:
            return None

        teleports = self.board.find_all_elements(Pieces.TELEPORT.value)

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

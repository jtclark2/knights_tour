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
import copy

from .grid_pos import GridPos

class Knight:
    # ***
    def __init__(self, board, start_pos=None, target_pos=None):
        """
        Initialize the knight on the board.
        Inputs:
            board_path:
            knight_start_pos: Expects input [row,col].
                              Finds 'S' on the board by default.
        """

        self.board = board
        if start_pos is None:
            try:
                self.start_pos = self.board.find_all_elements("S")[0]
            except IndexError:
                self.start_pos = None
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if target_pos is None:
            try:
                self.target_pos = self.board.find_all_elements("E")[0]  # assuming only 1
            except IndexError:
                self.target_pos = None
        else:
            self.target_pos = target_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

        self.journey_map = copy.deepcopy(board)
        self.cost_map = copy.deepcopy(board)

        self.error_context = "Unexpected error. Context unknown."

    # ***
    def reconstruct_path(self):
        """
        Builds a path from starting point to target.

        Assumptions:
            self.journey_map has already been populated correctly (via plan_path)

        return: List of positions the knight travels through on it's path

        """
        optimal_path = []
        current_node = self.target_pos
        while True:
            optimal_path.append(current_node)
            current_node = self.journey_map.get_value(current_node)
            if current_node is None:  # start_pos has value None
                break

        return list(reversed(optimal_path))

    def plan_path(self):
        """
        Plans a path for the knight to take. Optimizes according to cost function
        defined by self.get_cost().

        Side-Effects:
            Populates self.cost_map: a board that represents the lowest discovered cost
                for all positions.
            self.journey_map: A board in which each value is a reference to the previous position. This
                can be used to reconstruct the optimal path.
        """
        active_list = [self.knight_pos]  # Init list with a start pos

        # Initialize map of journey costs
        start_pos = self.knight_pos

        self.cost_map.reset_board()
        self.journey_map.reset_board()

        self.cost_map.set_element(start_pos, 0)

        while True:
            # Rational moves are allowed for a knight, land on the board, and land
            # upon unexplored spaces
            exploratory_node = active_list.pop(0)

            new_nodes = self.explore_moves(exploratory_node)

            for new_node in new_nodes:
                active_list.append(new_node)
            # Quick Finish condition (holds true in simple case)
            if active_list == []:
                return

    # ***
    def explore_moves(self, curr_pos):
        """
        Consider all valid moves from a given position. Each move would land in a new position, with a specific total
        cost (cost to reach curr_pos + move_cost). If the new cost is better/lower than the previously recorded value
        at that location on self.cost_map, then the cost map value is replaced, and the corresponding journey_map is
        updated so that the new position references curr_pos, since that is the path it took to get here.

        Inputs:
            curr_pos: current position, from which all available moves are explored

        return:
            positions: List of good moves

        Side-Effects:
            For each new target position in good_moves:
                - self.cost_map is updated with the NEW lowest cost
                - self.journey_map is updated with the current_position (where it moved from)
        """
        better_moves = [] # moves that are better (lower cost than previously encountered)
        for new_pos in self.get_possible_moves(curr_pos):
            try:
                move_cost = self.get_cost(self.board.get_value(new_pos))
            except:
                print(new_pos)
                raise
            path_cost = self.cost_map.get_value(curr_pos)
            total_cost = path_cost + move_cost

            # Save lowest cost
            if self.cost_map.get_value(new_pos) is None or total_cost < self.cost_map.get_value(new_pos):
                self.cost_map.set_element(new_pos, total_cost)
                self.journey_map.set_element(new_pos, curr_pos)
                better_moves.append(new_pos)

        return better_moves

    def move_heuristic(self):
        """
        Provide heuristic of distance remaining.
        This could help find more effective routes, by biasing the search.
        """
        raise NotImplementedError

    # ***
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

    # ***
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
            if value == "B" or value == "R":
                return False
            else:
                return True
        else:
            self.error_context = "Moves are not contained on the board"
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
            if self.board.get_value(travel_pos) == "B":
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
            if self.board.get_value(travel_pos) == "B":
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

    # ***
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

    # ***
    def teleport(self, curr_pos):
        """
        Returns the coupled teleport position.
        Assumptions:
            There are only 2 teleport positions (for more, we'd need to start adding IDs)
        Input: None
        Output: The location [y,x] of the exit teleport.
        """

        # No teleportation available from here
        if self.board.get_value(curr_pos) != "T":
            return None

        teleports = self.board.find_all_elements("T")

        # TODO - this check should be upon board init - better to find out sooner
        if len(teleports) != 2:
            print("Board does not have 2 teleports. Don't know where it leads, and I was always told not to venture through mystery portals.")
            return None

        # If there are 2, they connect, so just return the other
        if teleports[0] == curr_pos:
            return teleports[1]
        if teleports[1] == curr_pos:
            return teleports[0]

    def display_knight(self, pos=None):
        """
        Displays the board with the knight's current position overlaid.
        """
        display_character = "K"
        if pos is None:
            pos = self.knight_pos
        pieces = {display_character: pos}
        self.board.display_board(pieces=pieces, value_width=1)

    def validate_pos_sequence(self, pos_sequence, rich_print=False):
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

        # Apply board conditions, if they exist
        if self.board is None:
            raise Exception(
                "Error: No board loaded. Load a board before moving your pieces."
            )

        # print starting state
        if rich_print:
            self.display_knight(pos_sequence[0])

        pos_prev = pos_sequence[0]

        for pos in pos_sequence[1:]:
            if not self.validate_within_bounds(pos):
                return False

            # First iteration, we have no previous pos to compare against
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

    def problem1(self, pos_sequence):
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
                print(
                    "2 adjascent positions represent a move that a"
                    "knight is not permitted to make."
                    "Invalid move:" + str(pos_prev) + "-->" + str(pos)
                )
                return False

            pos_prev = pos

        return True


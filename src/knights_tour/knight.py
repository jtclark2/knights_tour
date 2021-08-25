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
                self.start_pos = self.board.find_element("S")[0]
            except IndexError:
                self.start_pos = None
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if target_pos is None:
            try:
                self.target_pos = self.board.find_element("E")[0]  # assuming only 1
            except IndexError:
                self.target_pos = None
        else:
            self.target_pos = target_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

        self.journey_map = copy.deepcopy(board)
        self.cost_map = copy.deepcopy(board)

        self.error_context = "Unexpected error. Context unknown."

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

    def explore_moves(self, curr_node):
        """
        Explores the map by making each available rational move.

        Inputs:
            curr_pos = (y,x), node we're exploring from
        Outputs:
            positions: list of new position nodes for continued exploration.

        Side-Effects:
            self.path_map = Board() in which each value is a pos pointing to
            node that it came from. This tracking data will allow us to reverse
            engineer the path after finding the minimal cost route.
        """
        new_nodes = []
        for node in self.get_possible_moves(curr_node):
            try:
                move_cost = self.get_cost(self.board.get_piece(node))
            except:
                print(node)
                raise
            path_cost = self.cost_map.get_piece(curr_node)
            extended_path_cost = path_cost + move_cost

            if self.cost_map.get_piece(
                node
            ) == None or extended_path_cost < self.cost_map.get_piece(node):
                self.cost_map.set_element(node, extended_path_cost)
                self.journey_map.set_element(node, curr_node)
                new_nodes.append(node)

        return new_nodes

    def move_heuristic(self):
        """
        Provide heuristic of distance remaining.
        """
        raise NotImplementedError

    @staticmethod
    def validate_L_move(delta):
        if (abs(delta.x) == 2 and abs(delta.y) == 1) or (
            abs(delta.x) == 1 and abs(delta.y) == 2
        ):
            return True
        else:
            return False

    def validate_within_bounds(self, node):
        """
        Check if a particular position is in bound.
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
        while travel_pos.x != stop_x:  # take 1 or 2 steps (depending on the move)
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
        while travel_pos.y != stop_y:  # take 1 or 2 steps (depending on the move)
            travel_pos += GridPos(0, sign)  # take one step in horizontal direction
            if self.board.get_piece(travel_pos) == "B":
                vertical_path_clear = False

        return vertical_path_clear

    def validate_barrier_clear(self, curr_node, next_node):
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
        horizontal_first_clear = self.is_horizontal_motion_clear_of_barriers(
            start_x=curr_node.x, stop_x=next_node.x, y=curr_node.y, sign=sign.x
        ) and self.is_vertical_motion_clear_of_barriers(
            start_y=curr_node.y, stop_y=next_node.y, x=next_node.x, sign=sign.y
        )

        # Vertical first --> then horizontal
        # S . .
        # 1 2 3
        vertical_first_clear = self.is_vertical_motion_clear_of_barriers(
            start_y=curr_node.y, stop_y=next_node.y, x=curr_node.x, sign=sign.y
        ) and self.is_horizontal_motion_clear_of_barriers(
            start_x=curr_node.x, stop_x=next_node.x, y=next_node.y, sign=sign.x
        )

        return horizontal_first_clear or vertical_first_clear

    def get_possible_moves(self, curr_pos):
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
        # TODO: looks like it's being initialized outside the loop...don't think that's needed though
        new_node = GridPos(-1, -1)  # initialize to invalid value
        for move in delta_moves:
            new_node = curr_pos + move
            if self.validate_within_bounds(new_node) and self.validate_barrier_clear(
                curr_pos, new_node
            ):
                new_positions.append(new_node)

        # TODO: Filter for going over barriers

        teleport = self.teleport(curr_pos)
        if self.teleport(curr_pos) is not None:
            new_positions.append(teleport)

        return new_positions

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
        Displays the board with the knight's current position overlaid.
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

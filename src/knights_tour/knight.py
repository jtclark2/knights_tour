"""
Assumptions:
    a) Board is rectangular. I anticipate other cases would work with minor
       tweaks, notably Board.read_board() and Knight.validate_within_bounds()
    b) The 32x32 board starts are passed in, since 'S' and 'E' were not
       pre-populated. 



Major Assumption: This space is fully searchable, since the board is 32x32,
meaning that 1024 positions exist, each with 8 possible moves. This is well
within our computational capbability. For a larger problem, we'd have to use
a more efficient approach with a goal heuristic, such as A-star.

Created by: Trevor Clark

Custom Dependencies:
    board.py
"""
import copy

# TODO: cost_map and journey_map are NOT game_mechanics objects. Just use numpy arrays instead

class Knight:
    # ***
    def __init__(self, game_mechanics, start_pos=None, target_pos=None):
        """
        Initialize the knight on the board.
        Inputs:
            board_path:
            knight_start_pos: Expects input [row,col].
                              Finds 'S' on the board by default.
        """

        self.game_mechanics = game_mechanics
        if start_pos is None:
            try:
                self.start_pos = self.game_mechanics.find_all_elements("S")[0]
            except IndexError:
                self.start_pos = None
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if target_pos is None:
            try:
                self.target_pos = self.game_mechanics.find_all_elements("E")[0]  # assuming only 1
            except IndexError:
                self.target_pos = None
        else:
            self.target_pos = target_pos

        if self.knight_pos is None:
            raise Exception("Input Error: No knight start position provided.")

        self.journey_map = copy.deepcopy(game_mechanics)
        self.cost_map = copy.deepcopy(game_mechanics)

        self.error_context = "Unexpected error. Context unknown."

    ################## Solver ##################


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
        for new_pos in self.game_mechanics.get_possible_moves(curr_pos):
            try:
                move_cost = self.game_mechanics.get_cost(self.game_mechanics.get_value(new_pos))
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

    ##################### Display ####################
    # using underlying display object to display about the planned path

    def display_path_as_list(self, path):
        """
        Pretty print for the list of positions in the path.
        """
        print("\nList of steps in path")
        print_str = ""
        for step_count, step in enumerate(path):
            my_str = f"Step: {step_count}\t\t"+ "Path cost: %i \t" % self.cost_map.get_value(step)
            print_str = print_str + my_str + "Position: " + str(step) + " -->\n"

        print(print_str)

    def display_path_as_grid(self, path):
        print("\nPath (values indicate steps taken)")
        journey = {}
        # journey_cost = {}
        for step_num, step_node in enumerate(path):
            journey[step_num] = step_node

            # This line would map the total cost at each step, instead of the count
            # journey_cost[self.cost_map.get_value(step_node)] = step_node

        self.game_mechanics.display_board(pieces=journey)

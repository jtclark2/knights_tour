import copy
import time

from .pieces import Pieces
from .grid_pos import GridPos
from .gameengine import GameEngine
from .user_interface import UI
from .heuristics import LongestPathSearchHeuristics as Heuristics


class Knight:
    # ***
    def __init__(self, game_engine: GameEngine, start_pos: GridPos=None, end_pos: GridPos=None):
        """
        Initialize the knight on the board.
        Inputs:
            board_path:
            knight_start_pos: Expects input [row,col].
                              Finds 'S' on the board by default.
        """
        self.game_engine = game_engine

        if start_pos is None:
            try:
                self.start_pos = self.game_engine.board.find_all_elements(Pieces.START.value)[0]
            except IndexError as err:
                raise NameError("start_pos not provided, and no valid 'S'tart element found on board.") from err
        else:
            self.start_pos = start_pos
        self.knight_pos = self.start_pos

        if end_pos is None:
            try:
                self.end_pos = self.game_engine.board.find_all_elements(Pieces.END.value)[0]  # assuming only 1
            except IndexError as err:
                raise NameError("end_pos not provided, and no valid 'E'nd element found on board.") from err
        else:
            self.end_pos = end_pos

        # Initialize maps for the travel cost and path of journey (empty except for 0 cost at start)
        self.journey_map = copy.deepcopy(self.game_engine.board)
        self.journey_map.reset_board()
        self.cost_map = copy.deepcopy(self.game_engine.board)
        self.cost_map.reset_board()

        # Initialize general parameters for longest_path
        self.available_moves_map = None
        self.start_time = None
        self.optimal_cost = 0
        self.optimal_path = [self.start_pos]

        # Config for longest path
        self.time_allowed = 10 # time allowed to explore (in seconds)
        self.heuristic = Heuristics().dense_search_heuristic

        # This would be every step on the board (so no obstructions, and a perfect score)
        self.cost_acceptance_thresh = self.game_engine.board.get_height() * self.game_engine.board.get_width() - 1

    ################## Solver ##################
    def reconstruct_path(self):
        """
        Builds a path from starting point to target.

        Assumptions:
            self.journey_map has already been populated correctly (via plan_path)

        return: List of positions the knight travels through on it's path

        """
        optimal_path = []
        current_node = self.end_pos
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
        This problem breaks down to dynamic programming, if you store a map of costs, and best paths to that cost,
        rather than storing every path to every space.

        Side-Effects:
            Populates self.cost_map: a board that represents the lowest discovered cost
                for all positions.
            self.journey_map: A board in which each value is a reference to the previous position. This
                can be used to reconstruct the optimal path.

        Assumptions:
            costs are all >= 0. Otherwise, we would get stuck in search cycles in which the cost would drop infinitely.
        """
        active_list = [self.start_pos]  # Init list with a start pos

        # Initialize maps for the travel cost and path of journey (empty except for 0 cost at start)
        self.journey_map = copy.deepcopy(self.game_engine.board)
        self.journey_map.reset_board()
        self.cost_map = copy.deepcopy(self.game_engine.board)
        self.cost_map.reset_board()
        self.cost_map.set_element(self.start_pos, 0)

        while True:
            # Rational moves are allowed for a knight, land on the board, and land
            # upon unexplored spaces
            exploratory_node = active_list.pop(0)

            new_nodes = self._explore_moves(exploratory_node)

            for new_node in new_nodes:
                active_list.append(new_node)

            # Quick Finish condition (holds true in simple case)
            if active_list == []:
                return

    def _explore_moves(self, curr_pos):
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
        better_moves = []  # moves that are better (lower cost than previously encountered)
        for new_pos in self.game_engine.get_possible_moves(curr_pos):
            try:
                move_cost = self.game_engine.get_cost(self.game_engine.board.get_value(new_pos))
            except:
                print(new_pos)
                raise
            path_cost = self.cost_map.get_value(curr_pos)
            total_cost = path_cost + move_cost

            # Save lowest cost
            recorded_total_cost = self.cost_map.get_value(new_pos)
            if recorded_total_cost is None or total_cost < recorded_total_cost:
                self.cost_map.set_element(new_pos, total_cost)
                self.journey_map.set_element(new_pos, curr_pos)
                better_moves.append(new_pos)

        return better_moves


    def find_longest_path_entry(self,
                                time_allowed = 10,
                                heuristic = Heuristics().identity_heuristic,
                                cost_acceptance_thresh=None):
        """
        This is the entry point for a depth first search, seeking the highest cost path. Heuristics can be used to
        determine the order of the nodes it seeks out, but it will still fundamentally be depth-first.

        This is intended to pseudo-solve problem 5. The full optimal solution is NP-complete, but we can still create
        paths with good results.

        Configuration:
            Rather than adding numerous inputs, or making a knight_config data type, I just got lazy, and put
            all the config in the init.

        inputs:
            path: The sequence of nodes that the knight traveled through to arrive at it's destination.
            cost: The total cost accrued while traveling the path

        outputs:
            None; however, see side-effects for member variables that get updated

        Side-effects:
            Solutions will will be load into: self.optimal_path and self.optimal_cost


        Find longest path by exploring ALL paths, according to a heuristic.

        This is an NP-complete problem, so the 32x32 has no known GUARANTEED solution (to my knowledge). However,
        we can use heuristics to explore in a smart way. This still doesn't guarantee success, but it improves our odds.


        """
        if cost_acceptance_thresh is not None:
            self.cost_acceptance_thresh = cost_acceptance_thresh
        self.time_allowed = time_allowed
        self.heuristic = heuristic

        # Initialize total available moves
        self.available_moves_map = copy.deepcopy(self.game_engine.board)
        for row in range(self.available_moves_map.get_height()):
            for col in range(self.available_moves_map.get_width()):
                pos = GridPos(row, col)
                if not self.game_engine.board.get_value(pos) in (Pieces.ROCK.value, Pieces.BARRIER.value):
                    moves = self.game_engine.get_possible_moves(pos)
                    self.available_moves_map.set_element(pos, len(moves))

        self.start_time = time.time()

        self.find_longest_path_recursive(path=[self.start_pos], cost=0)  # storing in self.journey_map

    def find_longest_path_recursive(self, path, cost):
        """
        This performs a depth first search, seeking the highest cost path. Heuristics can be used to determine the
        order of the nodes it seeks out, but it will still fundamentally be depth-first.

        Configuration:
            Rather than adding numerous inputs, or making a knight_config data type, I just got lazy, and put
            all the config in the init.

        inputs:
            path: The path
            cost:

        outputs:
            None; however, see side-effects for member variables that get updated

        Side-effects:
            Solutions will will be load into: self.optimal_path and self.optimal_cost

        """


        # End condition: either timer or missing define an acceptable score or number of non-visited spaces
        if time.time() - self.start_time > self.time_allowed:
            return
        if self.optimal_cost >= self.cost_acceptance_thresh:
            return

        # ### Setup (find next moves)
        curr_pos = path[-1]

        moves = self.game_engine.get_possible_moves(curr_pos)
        degree_move_tuples = [(self.available_moves_map.get_value(move), move) for move in moves]
        sorted_move_tuples = self.heuristic(degree_move_tuples)
        moves = [move[1] for move in sorted_move_tuples]

        # ### Prepare for move

        # Decrement all neighbors on available_moves_map:
        # more efficient than calling get_possible_moves on each possible move
        for move in moves:
            self.available_moves_map.set_element(move, self.available_moves_map.get_value(move) - 1)

        element = self.game_engine.board.get_value(curr_pos)
        move_cost = self.game_engine.get_cost(element)
        cost += move_cost

        # Fill current location with an obstacle and store nominal value in case we backtrack
        nominal_value = self.game_engine.board.get_value(curr_pos)
        self.game_engine.board.set_element(curr_pos, Pieces.ROCK.value)


        # ### Record score (if it's a new 'best')
        if cost > self.optimal_cost:
            self.optimal_path = copy.deepcopy(path)
            self.optimal_cost = cost

            if(time.time() - self.start_time > 1): # just reducing the initial flood
                # self.print_longest_path()
                pass


        # ### Take the next move (recursively)
        for next_move in moves:
            self.find_longest_path_recursive(path + [next_move], cost)

        # ### Backtrack and cleanup


        # increment neighbors on available_moves_map
        for move in moves:
            self.available_moves_map.set_element(move, self.available_moves_map.get_value(move) + 1)

        # replace barrier with nominal value
        self.game_engine.board.set_element(curr_pos, nominal_value)


    def print_longest_path(self):
        print("Highest cost path found...")
        print(f"Highest Cost: {self.optimal_cost}")
        print(f"Steps in path: {len(self.optimal_path)}")
        # print(f"Path: {self.optimal_path}")
        pieces = {pos: f"{val}" for val,pos in enumerate(self.optimal_path)}
        UI.display_board(self.game_engine.board, pieces=pieces, value_width=3)

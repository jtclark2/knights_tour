"""
Display module.
Currently contains TextUI, which just prints to stdout.

Future Improvements:
    - Add GUI
    - Formalize interface (or ABC)
"""
import copy
import abc

from .grid_pos import GridPos

class AbstractUI(metaclass=abc.ABCMeta):

    @classmethod
    def display_board(cls, board, pieces=None, value_width = 2):
        raise NotImplementedError

    @classmethod
    def display_path_as_list(cls, path, cost_map):
        raise NotImplementedError

    @classmethod
    def display_path_as_grid(cls, board, path, cost_map):
        raise NotImplementedError

class TextUI(AbstractUI):
    def __init__(self):
        pass

    @classmethod
    def display_board(cls, board, pieces=None, value_width = 2):
        """
        Displays a copy of the board.

        Note: I've chosen not to expose the underlying data structure (numpy arrays at the time of writing this).
        It makes me a little sad, since np arrays are written to be so efficient when vectorized, and this approach is
        comparatively slow since I use separate calls for every element. That said, print() is slow anyways itself,
        and I'm primarily working with smallish (~1000-2000) element boards, since they need to fit on-screen.
        This trade-off is worth it for the added encapsulation.

        Inputs:
            board: indexable 2D map
            pieces (Optional):
                Dictionary -  {piece:position}
            value_width: Largest value allowed per space. Anything large will be truncated to value_width.
                Too large a value may cause print to start wrapping.
        """

        # build a new one, so we don't just create a reference and muck up the original
        board = copy.deepcopy(board)
        if pieces is not None:
            for pos, val in pieces.items():
                board.set_element(pos, val)

        board_str = ""
        for row_index in range(board.get_height()):
            for col_index in range(board.get_width()):
                element = board.get_value(GridPos(row_index, col_index))
                board_str += '{:{width}}'.format(str(element)[:value_width], width=str(value_width+1))

            board_str = board_str[:-1]  # remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  # remove trailing '\n'

        print("\n" + board_str)

    @classmethod
    def display_path_as_list(cls, path, cost_map):
        """
        Helper for printing pretty, and with costs.

        Inputs:
            path: a list of GridPos, representing the path an agent has taken.
            cost_map: a Board, representing the costs to get to available spaces on the map. All path positions
            must be populated.
        """
        print("\nList of steps in path")
        print_str = ""
        for step_count, step in enumerate(path):
            my_str = f"Step: {step_count}\t\t"+ "Path cost: %i \t" % cost_map.get_value(step)
            print_str = print_str + my_str + "Position: " + str(step) + " -->\n"

        print(print_str)

    @classmethod
    def display_path_as_grid(cls, board, path, cost_map):
        """
        Helper method for show the path traveled spatially.

        Inputs:
            path: a list of GridPos, representing the path an agent has taken.
            cost_map: a Board, representing the costs to get to available spaces on the map. All path positions
            must be populated.
        """
        print("\nPath (values indicate cost of most efficient journey)")
        # journey = {}
        journey_cost = {}
        for _, step_node in enumerate(path):
            # This line would print total cost, instead of step count
            journey_cost[step_node] = cost_map.get_value(step_node)

        cls.display_board(board, pieces=journey_cost, value_width=2)


# Configuration
UI = TextUI
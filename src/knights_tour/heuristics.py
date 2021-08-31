import random

class LongestPathSearchHeuristics:
    """
    These heuristics are used to determine the order of in which to navigate through the search space.
    This space can be thought of as spacial positions on a game board, or as nodes in an undirected graph.

    Technical Note: Python sort() is stable, which allows us to use it within our heuristic deterministically.
    """

    def identity_heuristic(self, moves):
        return moves

    def dense_search_heuristic(self, degree_move_tuples):
        """
        Purpose:
             This heuristic biases towards densely searching an area, which is fantastic for filling a simple space
              with no gaps (eg: the classic knights tour).

        Explanation:
            This heuristic was recommended in the referenced paper.
            "Always move the knight to an adjacent, unvisited square with minimal degree."
            Degree: Number of moves available (after taking a move).
                Let's say the knight is at position A, and has moves available taking it to positions B,C, or D.
                If those moves were taken, let's say:
                    - B has 3 moves (aka degree 3)
                    - D has 5 moves (aka degree 5)
                    - C has 2 moves (aka degree 2)
                Then from position A, we would explore C first (2), then B (3), then D (5).

        Intuition:
            This tends to pull the knight back towards the most heavily explored cluster, by always searching
            areas with the least remaining moves. This prevents like islands (area with no escape path) from forming.
            As a result, a more uniform fill is created, because those tiny islands are quickly explored and invalid paths
            are quickly discarded. This is a sort of "fail early, fail often" strategy.
        """
        degree_move_tuples.sort(key=lambda value: value[0])
        return degree_move_tuples

    def sparse_search_heuristic(self, degree_move_tuples):
        """
            Purpose:
                In particular, this heuristic biases towards open, unsearched areas. This helps it explore the span of
                the entire space quickly; however, since knight moves jump over spaces, it also has a tendency to skip
                areas, sometimes by traveling through all the spaces that would allow it to return, creating islands
                of spaces that become difficult to reach.
            """
        degree_move_tuples.sort(key=lambda value: value[0], reverse=True)
        return degree_move_tuples

    def random_search_heuristic(self, moves):
        random.shuffle(moves)
        return moves
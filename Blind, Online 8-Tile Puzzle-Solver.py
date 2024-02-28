from random import sample


class EightTilePuzzle:

    # location numbers
    # ┌───────┐
    # │ 0 1 2 │
    # │ 3 4 5 │
    # │ 6 7 8 │
    # └───────┘
    _neighbors = {
        0: (1, 3),
        1: (0, 2, 4),
        2: (1, 5),
        3: (0, 4, 6),
        4: (1, 3, 5, 7),
        5: (2, 4, 8),
        6: (3, 7),
        7: (4, 6, 8),
        8: (5, 7)
    }

    @classmethod
    def neighbors(cls, location) -> tuple[int, ...]:
        return cls._neighbors[location]

    @staticmethod
    def scrambled_puzzle(number_of_swaps: int):

        puzzle: EightTilePuzzle = EightTilePuzzle("12345678 ")

        missing_tile_path: str = ""
        current_location: int = 8
        missing_tile_path += str(current_location)
        previous_location: int | None = None

        for _ in range(number_of_swaps):
            neighbors: tuple = tuple(neighbor for neighbor in puzzle.neighbors(current_location) if neighbor != previous_location)
            next_location: int = sample(neighbors, 1)[0]
            puzzle.attempt_swap(current_location, next_location)
            missing_tile_path += str(next_location)
            previous_location, current_location = current_location, next_location
        return puzzle, missing_tile_path

    def __init__(self, initial_puzzle_state: str):
        """
        :param initial_puzzle_state: The string representation of the puzzle. The string for the puzzle should be in top-to-bottom, left-to-right order, with a space for the empty space. EG: "7681 2345" for "768" across the top, "1 2" across the middle, and "345" across the bottom.
        """
        self._puzzle: list = []
        for i in range(3):
            self._puzzle.append(list(initial_puzzle_state[3 * i:3 * i + 3]))

    def attempt_swap(self, location_a: int, location_b: int) -> None:
        if location_b not in self.neighbors(location_a):
            raise Exception(f"Swap attempted on non-neighboring location (from {location_a} to {location_b}).")

        a_row: int
        c_col: int
        b_row: int
        b_col: int
        a_row, a_col = location_a // 3, location_a % 3
        b_row, b_col = location_b // 3, location_b % 3

        if self._puzzle[a_row][a_col] == ' ' or self._puzzle[b_row][b_col] == ' ':
            self._puzzle[a_row][a_col], self._puzzle[b_row][b_col] = self._puzzle[b_row][b_col], self._puzzle[a_row][a_col]

    def is_solved(self) -> bool:
        return self._puzzle == [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

    def print(self, info=None) -> None:
        print(
            "┌───────┐\n│ {} {} {} │\n│ {} {} {} │ {}\n│ {} {} {} │\n└───────┘".format(
                *(tile for row in self._puzzle[:-1] for tile in row),
                info if info else "",
                *(tile for tile in self._puzzle[-1])
            )
        )


def solve(
    puzzle: EightTilePuzzle,
    number_of_moves_allowed: int = 31,
    conjectured_location: int = None,
    conjectured_previous_location: int = None,
    print_during_solving: bool = False
) -> str | None:

    # Initial entry into the algorithm.
    if conjectured_location is None:

        # Trivial case.
        if puzzle.is_solved():
            return "\"\""

        # For each location in the 3x3 grid (flattened)...
        for location in range(9):

            if print_during_solving:
                print(f"Assuming empty space location of {location}.")

            # Search assuming that it is the empty space.
            solution: str | None = solve(puzzle, number_of_moves_allowed, location, print_during_solving=print_during_solving)

            # If a solution was found return the path taken with the currently conjectured location prefixed.
            if solution:
                return str(location) + solution

        # Exit the algorithm and return None, indicating that no solution was found within the move limitation.
        return None

    # Recursive steps.
    else:

        # Try each neighbor.
        for neighbor in puzzle.neighbors(conjectured_location):

            # If the neighbor is the previously visited location, ignore it.
            if neighbor == conjectured_previous_location:
                continue

            # Visit the neighboring location.
            puzzle.attempt_swap(conjectured_location, neighbor)

            if print_during_solving:
                puzzle.print(f"{(conjectured_location, neighbor)} > A: Exploring")

            # Check if the solution state has been reached by visiting the neighboring location.
            solved = puzzle.is_solved()

            # Solution state was reached.
            if solved:

                # Return the puzzle to the state it was in before it was modified in this recursive step.
                puzzle.attempt_swap(conjectured_location, neighbor)

                if print_during_solving:
                    puzzle.print(f"{(conjectured_location, neighbor)} < B: Solution Found")

                # Report to the previous step that the solution state was reached and which move (neighbor) was used to do so.
                return str(neighbor)

            # Check if the remaining number of moves allowed is at least one.
            if number_of_moves_allowed - 1 >= 1:

                # Enter the next recursive step.
                next_solve: str | None = solve(puzzle, number_of_moves_allowed - 1, neighbor, conjectured_location, print_during_solving=print_during_solving)

                # The recursive step above will return the puzzle to the state it was in when control was handed off to it. Do the same / do it here.
                puzzle.attempt_swap(conjectured_location, neighbor)

                if print_during_solving:
                    puzzle.print(f"{(conjectured_location, neighbor)} < C: Returning to Previous Call")

                # If the next step reported a solution was found, prefix this move to the solution it reported and return this modified solution to the previous step.
                if next_solve:
                    return str(neighbor) + next_solve

            # There are no more moves allowed.
            else:

                # Return the puzzle to the state it was in before it was modified in this recursive step.
                puzzle.attempt_swap(conjectured_location, neighbor)

                if print_during_solving:
                    puzzle.print(f"{(conjectured_location, neighbor)} < D: Out of Moves")

        # Report to the previous step that None of the neighboring paths leads to a solution (within the move limitation).
        return None


scramble_moves: int = 20
puzzle: EightTilePuzzle
scramble_sequence: str
puzzle, scramble_sequence = EightTilePuzzle.scrambled_puzzle(scramble_moves)
solution: str | None = solve(puzzle, scramble_moves)

puzzle.print("Scrambled Puzzle")
print(f"Scrambled with: {scramble_sequence}")
print(f"Solved with: {solution}")

"""
For a solution unknown to us, the number_of_moves_allowed parameter would be set to
31, which is the minimum number of swaps that will guarantee that the solution
state is reached when given any valid, random starting state.

Although the algorithm is essentially a brute-force algorithm, the purpose of it is
not to be efficient, but to demonstrate that such problems are theoretically
solvable even under such info-minimal conditions because of the specific way in
which the problem is modeled.

The key aspect of the formulation of the problem that allows for this blind search
is the guarantee of each transformation being an involution. Regardless of the
current state of the puzzle, all transformations applied to the puzzle can be
undone by immediately applying that same transformation again. This allows for a
record of each transformation to be kept so that both the state space can be
explored and the puzzle can be returned to its initial state.

Note that this algorithm, by itself, won't necessarily yield a solution with the
minimum number of moves to solve the initial puzzle, but given that the solution
can be used to recover the initial, scrambled state of the puzzle, one needs only
to feed the recovered initial state into a traditional 8-Tile-Puzzle-Solver to
receive an optimal solution.
"""

class EightTilePuzzle:
    def __init__(self, initialPuzzleState):
        self._puzzle = initialPuzzleState

    def attemptSwap(self, swapNumber):
        if swapNumber == 0:
            if self._puzzle[0][0] == ' ' or self._puzzle[0][1] == ' ':
                temp = self._puzzle[0][0]
                self._puzzle[0][0] = self._puzzle[0][1]
                self._puzzle[0][1] = temp
        elif swapNumber == 1:
            if self._puzzle[0][1] == ' ' or self._puzzle[0][2] == ' ':
                temp = self._puzzle[0][1]
                self._puzzle[0][1] = self._puzzle[0][2]
                self._puzzle[0][2] = temp
        elif swapNumber == 2:
            if self._puzzle[1][0] == ' ' or self._puzzle[1][1] == ' ':
                temp = self._puzzle[1][0]
                self._puzzle[1][0] = self._puzzle[1][1]
                self._puzzle[1][1] = temp
        elif swapNumber == 3:
            if self._puzzle[1][1] == ' ' or self._puzzle[1][2] == ' ':
                temp = self._puzzle[1][1]
                self._puzzle[1][1] = self._puzzle[1][2]
                self._puzzle[1][2] = temp
        elif swapNumber == 4:
            if self._puzzle[2][0] == ' ' or self._puzzle[2][1] == ' ':
                temp = self._puzzle[2][0]
                self._puzzle[2][0] = self._puzzle[2][1]
                self._puzzle[2][1] = temp
        elif swapNumber == 5:
            if self._puzzle[2][1] == ' ' or self._puzzle[2][2] == ' ':
                temp = self._puzzle[2][1]
                self._puzzle[2][1] = self._puzzle[2][2]
                self._puzzle[2][2] = temp
        elif swapNumber == 6:
            if self._puzzle[0][0] == ' ' or self._puzzle[1][0] == ' ':
                temp = self._puzzle[0][0]
                self._puzzle[0][0] = self._puzzle[1][0]
                self._puzzle[1][0] = temp
        elif swapNumber == 7:
            if self._puzzle[1][0] == ' ' or self._puzzle[2][0] == ' ':
                temp = self._puzzle[1][0]
                self._puzzle[1][0] = self._puzzle[2][0]
                self._puzzle[2][0] = temp
        elif swapNumber == 8:
            if self._puzzle[0][1] == ' ' or self._puzzle[1][1] == ' ':
                temp = self._puzzle[0][1]
                self._puzzle[0][1] = self._puzzle[1][1]
                self._puzzle[1][1] = temp
        elif swapNumber == 9:
            if self._puzzle[1][1] == ' ' or self._puzzle[2][1] == ' ':
                temp = self._puzzle[1][1]
                self._puzzle[1][1] = self._puzzle[2][1]
                self._puzzle[2][1] = temp
        elif swapNumber == 10:
            if self._puzzle[0][2] == ' ' or self._puzzle[1][2] == ' ':
                temp = self._puzzle[0][2]
                self._puzzle[0][2] = self._puzzle[1][2]
                self._puzzle[1][2] = temp
        elif swapNumber == 11:
            if self._puzzle[1][2] == ' ' or self._puzzle[2][2] == ' ':
                temp = self._puzzle[1][2]
                self._puzzle[1][2] = self._puzzle[2][2]
                self._puzzle[2][2] = temp
        else:
            raise Exception("Hey Pal, did you just blow in from stupid town?")

    def isSolved(self):
        return self._puzzle == [[1,2,3], [4,5,6], [7,8,' ']]

    def print(self):
        print("┌───────┐\n│ {} {} {} │\n│ {} {} {} │\n│ {} {} {} │\n└───────┘".format(*[tile for row in self._puzzle for tile in row]))



def solve(puzzle, maximumNumberOfSwaps):
    for swap in range(12):

        print('DO', 'height:', maximumNumberOfSwaps, 'Swap:', swap)
        puzzle.attemptSwap(swap)
        puzzle.print()

        if puzzle.isSolved():
            print('UNDO SOLVED', 'height:', maximumNumberOfSwaps, 'Swap:', swap)
            puzzle.attemptSwap(swap)
            return [swap]

        if maximumNumberOfSwaps > 1:
            nextSwap = solve(puzzle, maximumNumberOfSwaps-1)
            if nextSwap is not None:
                print('UNDO SOLVED', 'height:', maximumNumberOfSwaps, 'Swap:', swap)
                puzzle.attemptSwap(swap)
                return [swap] + nextSwap

        print('UNDO', 'height:', maximumNumberOfSwaps, 'Swap:', swap)
        puzzle.attemptSwap(swap)
        puzzle.print()

    return None


'''
Example:

The puzzle is instantiated as solved and then scrambled in order to make the
solution obvious to us.
'''
puzzle = EightTilePuzzle([[1,2,3], [4,5,6], [7,8,' ']])

scrambleSwaps = [5, 4, 7, 6, 0]
for swap in scrambleSwaps:
	puzzle.attemptSwap(swap)

'''
For a solution unkown to us, the maximumNumberOfSwaps parameter would be set to
31, which is the minimum number of swaps that will guarantee that the solution
state is reached when given any valid, random starting state.

Although the time-complexity of this algorithm is abhorrent, the purpose of it is
not to be efficient, but to demonstrate that such problems are theoretically
solvable even under such info-minimal conditions.

Note that this algorithm, by itself, won't necessarily yield a solution with the
minimum number of moves to solve the initial puzzle, but given that the solution
can be used to recover the initial, scrambled state of the puzzle, one needs only
to feed the recovered initial state into a traditional 8-Tile-Puzzle-Solver to
receive an optimal solution.
'''
puzzle.print()
print('---------')
solve(puzzle, len(scrambleSwaps))

print('---------')
puzzle.print()
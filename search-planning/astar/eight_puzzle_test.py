from astar import AStarSolver, AStarState
from eight_puzzle import EightPuzzle

class EightPuzzleSolver(AStarSolver):
    def generate(self, current):
        #TODO replace these meaningless numbers by Moves
        next_steps = []
        puzzle = current.state
        if puzzle.can_move(puzzle.Moves.up):
            next_puzzle = EightPuzzle(puzzle=puzzle)
            next_puzzle.move_up()
            next_steps.append(AStarState(self.distance(next_puzzle), current.g + 1, next_puzzle, current))
        if puzzle.can_move(puzzle.Moves.right):
            next_puzzle = EightPuzzle(puzzle=puzzle)
            next_puzzle.move_right()
            next_steps.append(AStarState(self.distance(next_puzzle), current.g + 1, next_puzzle, current))
        if puzzle.can_move(puzzle.Moves.left):
            next_puzzle = EightPuzzle(puzzle=puzzle)
            next_puzzle.move_left()
            next_steps.append(AStarState(self.distance(next_puzzle), current.g + 1, next_puzzle, current))
        if puzzle.can_move(puzzle.Moves.down):
            next_puzzle = EightPuzzle(puzzle=puzzle)
            next_puzzle.move_down()
            next_steps.append(AStarState(self.distance(next_puzzle), current.g + 1, next_puzzle, current))
        return next_steps

    def is_final_state(self, state):
        return self.desired == state

    def distance(self, instance):
        """
        Manhattan distance
        """
        value = 0
        dimension = instance.dimension
        for i in range(len(instance)):
            if instance[i] == 0:
                continue
            current_i = self.desired.index(instance[i])
            value += abs(current_i % dimension - i % dimension) + abs(current_i // dimension - i // dimension)
        return value


if __name__ == '__main__':
    eightp = EightPuzzle(4)
    eightp.shuffle(80)
    solver = EightPuzzleSolver(eightp, list(range(1, len(eightp))) + [0])
    print(eightp)
    solution = solver.solve()
    for step in solution:
        print("\n", step, sep="")
    print(len(solution))

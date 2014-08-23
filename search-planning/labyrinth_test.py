import sys
from astar import AStarState, AStarSolver
from collections import namedtuple


class Labyrinth:
    def __init__(self, filename):
        self.labyrinth = list(map(lambda l:l.rstrip(), open(sys.argv[1]).readlines()))
        self.initial =  0, self.labyrinth[0].find(' ')
        self.desired = len(self.labyrinth) - 1, self.labyrinth[-1].find(' ')

    def can_move_up(self, l, c):
        return l > 0 and self.labyrinth[l - 1][c] != '*'

    def can_move_down(self, l, c):
        return l < len(self.labyrinth) and self.labyrinth[l + 1][c] != '*'

    def can_move_left(self, l, c):
        return c > 0 and self.labyrinth[l][c - 1] != '*'

    def can_move_right(self, l, c):
        return c < len(self.labyrinth) - 1 and self.labyrinth[l][c + 1] != '*'

    def print_path(self, path):
        for l, c in path:
            ll = list(self.labyrinth[l])
            ll[c] = '+'
            self.labyrinth[l] = ''.join(ll)
        print('\n'.join(self.labyrinth))


class LabyrinthSolver(AStarSolver):
    def __init__(self, labyrinth):
        super().__init__(labyrinth.initial, labyrinth.desired)
        self.labyrinth = labyrinth

    def generate(self, current):
        next_steps = []
        l, c = current.state
        if self.labyrinth.can_move_up(l, c):
            next_position = (l - 1, c)
            next_steps.append(AStarState(self.distance(next_position), current.g + 1, next_position, current))
        if self.labyrinth.can_move_down(l, c):
            next_position = (l + 1, c)
            next_steps.append(AStarState(self.distance(next_position), current.g + 1, next_position, current))
        if self.labyrinth.can_move_left(l, c):
            next_position = (l, c - 1)
            next_steps.append(AStarState(self.distance(next_position), current.g + 1, next_position, current))
        if self.labyrinth.can_move_right(l, c):
            next_position = (l, c + 1)
            next_steps.append(AStarState(self.distance(next_position), current.g + 1, next_position, current))
        return next_steps

    def is_final_state(self, state):
        return self.desired == state

    def distance(self, position):
        return len(self.labyrinth.labyrinth) - position[0] - 1


if __name__ == '__main__':
    labyrinth = Labyrinth(sys.argv[1])
    labyrinth.print_path(LabyrinthSolver(labyrinth).solve())


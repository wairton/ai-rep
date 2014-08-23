from enum import Enum
from random import choice

class EightPuzzle(list):
    """
    TODO
    """
    def __init__(self, dimension=3, puzzle=None):
        if puzzle == None:
            self.extend(range(1, dimension**2))
            self.append(0)
            self.zero = len(self) - 1
            self.dimension = dimension
        else:
            self.extend(puzzle)
            self.zero = puzzle.zero
            self.dimension = puzzle.dimension

    class Moves(Enum):
        up, down, left, right = range(1,5)

        @classmethod
        def random(cls):
            return choice(list(cls.__members__.values()))

    def can_move(self, move):
        if move == self.Moves.up:
            return self.zero < len(self) - self.dimension
        elif move == self.Moves.down:
            return self.zero >= self.dimension
        elif move == self.Moves.left:
            return self.zero % self.dimension != self.dimension - 1
        elif move == self.Moves.right:
            return self.zero % self.dimension > 0
        return False

    def move_up(self):
        self.move(self.Moves.up)

    def move_down(self):
        self.move(self.Moves.down)

    def move_right(self):
        self.move(self.Moves.right)

    def move_left(self):
        self.move(self.Moves.left)

    def move(self, move):
        if not self.can_move(move):
            return False
        zero, dim = self.zero, self.dimension
        if move == self.Moves.up:
            self[zero + dim], self[zero] = self[zero], self[zero + dim]
            self.zero += dim
        elif move == self.Moves.down:
            self[zero - dim], self[zero] = self[zero], self[zero - dim]
            self.zero -= dim
        elif move == self.Moves.left:
            self[zero], self[zero + 1] = self[zero + 1], self[zero]
            self.zero += 1
        elif move == self.Moves.right:
            self[zero], self[zero - 1] = self[zero - 1], self[zero]
            self.zero -= 1

        return True

    def shuffle(self, times=50):
        # TODO replace this dummy shuffle function
        for i in range(times):
            self.move(self.Moves.random())

    def __str__(self):
        # TODO ugly, you can do better. It works only for 1 < dimension < 4
        slist = list(map(str, self))
        return '\n'.join([' '.join(slist[i:i+self.dimension]) for i in range(0, len(self), self.dimension)])

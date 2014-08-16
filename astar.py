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

class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.desired = list(range(1, len(puzzle))) + [0]
        self.states = []

    def solve(self):
        #h(x), g(x), state, previous direction, pointer to previous state
        self.states.append((self.distance(self.puzzle), 0, self.puzzle, 0, None))
        while len(self.states) > 0:
            current = self.pop_closer()
            #print(current[0], current[1], current[0] + current[1], len(self.states))
            if current[2]  == self.desired:
                self.print_solution(current)
                break
            for new in self.generate(current):
                self.insert_state(new)
            #input()
            #print(self.states)

    def print_solution(self, state):
        self.path = []
        print("total cost: ", state[1])
        while state[-1] != None:
            self.path.append(state[2])
            state = state[-1]
        self.path.append(state[2])
        for step in self.path[::-1]: 
            print(step, '\n')

    def pop_closer(self):
        min_distance, index = float("inf") , 0
        for i, state in enumerate(self.states):
            current_distance = state[0] + state[1]
            if current_distance < min_distance:
                min_distance, index = current_distance, i
        return self.states.pop(index)

    def insert_state(self, new_state):
        found = 0
        collect = []
        for i, state in enumerate(self.states):
            if state[2] == new_state[2]:
                found += 1
                collect.append(i)
                if state[0] + state[1] >= new_state[0] + new_state[1]:
                    self.states[i] = new_state
                return
        self.states.append(new_state)

    def generate(self, current):
        next_steps = []
        #h(x), g(x), state, previous direction, pointer to previous state
        hx, gx, puzzle, before, pointer = current
        #distance, puzzle, before = current
        if before != 4 and puzzle.can_move(puzzle.Moves.up):
            tmp = EightPuzzle(puzzle=puzzle)
            tmp.move_up()
            next_steps.append((self.distance(tmp), gx + 1, tmp, 1, current))
        if before != 3 and puzzle.can_move(puzzle.Moves.right):
            tmp = EightPuzzle(puzzle=puzzle)
            tmp.move_right()
            next_steps.append((self.distance(tmp), gx + 1, tmp, 2, current))
        if before != 2 and puzzle.can_move(puzzle.Moves.left):
            tmp = EightPuzzle(puzzle=puzzle)
            tmp.move_left()
            next_steps.append((self.distance(tmp), gx + 1, tmp, 3, current))
        if before != 1 and puzzle.can_move(puzzle.Moves.down):
            tmp = EightPuzzle(puzzle=puzzle)
            tmp.move_down()
            next_steps.append((self.distance(tmp), gx + 1, tmp, 4, current))
        return next_steps

    def distance(self, state):
        """
        Manhattan distance
        """
        value = 0
        dimension = self.puzzle.dimension
        for i in range(len(self.puzzle)):
            if state[i] == 0:
                continue
            current_i = self.desired.index(state[i])
            value += abs(current_i % dimension - i % dimension) + abs(current_i // dimension - i // dimension)
        return value

    def distance2(self, state):
        """
        Hamming distance
        """
        missed = 0
        for i in range(len(self.puzzle)):
            if state[i] == 0:
                continue
            if state[i] != self.desired[i]:
                missed += 1
        return missed

if __name__ == '__main__':
    eightp = EightPuzzle(4)
    eightp.shuffle(100)
    solver = Solver(eightp)
    print(eightp)
    solver.solve()

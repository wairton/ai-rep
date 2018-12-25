import sys


class Solver:
    def get_stack(self, sudoku):
        stack = []
        for node in sudoku.nodes():
            if node.value == 0:
                # TODO: do we need to use a .copy() here?
                stack.append((node.index, node.options))
        return stack

    def solve(self, sudoku):
        return self.solve_by_guessing(sudoku)

    def solve_by_iteration(self, sudoku):
        # print('-' * 50)
        # print(self)
        dones = sudoku.iterate()
        while dones > 0:
            # print('-' * 50)
            # print(self)
            dones = sudoku.iterate()
        # print('-' * 50)
        # print(self)
        return sudoku, sudoku.is_solved

    def solve_by_guessing(self, sudoku):
        sudoku, is_solved = self.solve_by_iteration(sudoku)
        if is_solved:
            return sudoku, True
        new_line = sudoku.to_line()
        stack = self.get_stack(sudoku)
        while len(stack) > 0:
            index, options = stack.pop()
            while len(options) > 0:
                option = options.pop()
                new_list = list(new_line)
                new_list[index] = option
                guess_line = ''.join(str(k) for k in new_list)
                # print(guess_line)
                sudoku2, is_solved = self.solve_by_iteration(Sudoku.from_line(guess_line))
                if is_solved:
                    # print("opa!")
                    return sudoku2, True
        return sudoku, False


class Sudoku:
    def __init__(self, lines, columns, blocks):
        self.lines = lines
        self.columns = columns
        self.blocks = blocks

    def __str__(self):
        s = []
        for i in range(9):
            s.append(' '.join(str(n.value) for n in self.lines[i]))
        return '\n'.join(s)

    def debug(self):
        s = []
        s.append('=' * 80)
        for i in range(9):
            if i % 3 == 0:
                s.append('_' * 144)
            line = [n.debug() for n in self.lines[i]]
            f = [' ', ' ', ' | '] * 3
            s.append(''.join(ll + ff for ll, ff in zip(line, f)))
            # s.append(' '.join(n.debug() for n in self.lines[i]))
        s.append('-' * 80)
        return '\n'.join(s)

    def to_line(self):
        return ''.join(''.join(str(k.value) for k in self.lines[i]) for i in range(9))

    def nodes(self):
        ns = []
        for line in self.lines.values():
            ns.extend(line)
        return ns

    def iterate(self):
        dones = 0
        for node in self.nodes():
            if node.value != 0:
                continue
            for i, group in zip(
                    node.position, (self.lines, self.columns, self.blocks)):
                done = self.prune_options(node, group[i])
                if done:
                    dones += 1
                    break
        return dones

    @property
    def is_solved(self):
        for node in self.nodes():
            if node.value == 0:
                return False
        return True

    def prune_options(self, current, nodes):
        if current.value != 0:
            return False
        for n in nodes:
            if n.value == 0:
                continue
            if current.position == n.position:
                continue
            if n.value in current.options:
                current.options.remove(n.value)
        if len(current.options) == 1:
            current.value = current.options.pop()
            return True
        return False

    def solve(self):
        # print('-' * 50)
        # print(self)
        dones = self.iterate()
        while dones > 0:
            # print('-' * 50)
            # print(self)
            dones = self.iterate()
        # print('-' * 50)
        # print(self)
        return self.solved

    @classmethod
    def lc_to_block(cls, l, c):
        return (l // 3) * 3 + (c // 3)

    @classmethod
    def from_line(cls, line):
        line = line.strip()
        slines = {}
        scolumns = {}
        sblocks = {}
        for i, v in enumerate(line):
            li = i // 9
            co = i % 9
            bl = Sudoku.lc_to_block(li, co)
            node = Node(li, co, int(v))
            if li not in slines:
                slines[li] = []
            slines[li].append(node)
            if co not in scolumns:
                scolumns[co] = []
            scolumns[co].append(node)
            if bl not in sblocks:
                sblocks[bl] = []
            sblocks[bl].append(node)
        return Sudoku(slines, scolumns, sblocks)


class Node:
    def __init__(self, line=0, column=0, value=0):
        self.value = value
        self.line = line
        self.column = column
        if value == 0:
            self.options = set(range(1, 10))
        else:
            self.options = set()

    @property
    def position(self):
        return self.line, self.column, self.b

    @property
    def index(self):
        return self.line * 9 + self.column

    @property
    def b(self):
        return (self.line // 3) * 3 + (self.column // 3)

    def debug(self):
        # return "{} ({}) at {}".format(self.value, self.options, self.position)
        return "{} ({})".format(self.value, ''.join(str(a) for a in self.options)).ljust(15)

    def __str__(self):
        return "{} at [{}, {}]".format(self.value, self.line, self.column)




def exp1(filename):
    solved = 0
    nsolved = 0
    solver = Solver()
    for line in open(filename).readlines():
        sudoku = Sudoku.from_line(line.strip())
        sudoku, is_solved = solver.solve_by_iteration(sudoku)
        if is_solved:
            solved += 1
        else:
            nsolved += 1
    print(solved, nsolved)


def exp2(filename):
    solved = 0
    nsolved = 0
    for line in open(filename).readlines():
        sudoku = Sudoku.from_line(line.strip())
        print(sudoku.debug())
        print('-' * 50)
        sudoku.solve()
        print(sudoku.debug())
        print(sudoku.to_line())
        break


def exp3(filename):
    """
    Solve sample from scheurblock
    """
    puzzle = (
        '005090347070026010891037600'
        '000069050907304802020870000'
        '009780534040950080583040200'
    )
    sudoku, is_solved = Solver().solve_by_iteration(Sudoku.from_line(puzzle))
    print(sudoku)


def exp4(filename):
    solved, nsolved = 0, 0
    for line in open(filename).readlines():
       sudoku, is_solved = Solver().solve(Sudoku.from_line(line))
       if is_solved:
           solved += 1
       else:
           nsolved += 1
    print(solved, nsolved)

if __name__ == '__main__':
    exp4(sys.argv[1])

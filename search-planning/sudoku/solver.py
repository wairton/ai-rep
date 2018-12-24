import sys


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
    def solved(self):
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
    def from_line(self, line):
        slines = {}
        scolumns = {}
        sblocks = {}
        for i, v in enumerate(line):
            li = i // 9
            co = i % 9
            bl = lc_to_block(li, co)
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
    def b(self):
        return (self.line // 3) * 3 + (self.column // 3)

    def __str__(self):
        return "{} at [{}, {}]".format(self.value, self.line, self.column)


def lc_to_block(l, c):
    return (l // 3) * 3 + (c // 3)


def exp1(filename):
    solved = 0
    nsolved = 0
    for line in open(filename).readlines():
        sudoku = Sudoku.from_line(line.strip())
        if sudoku.solve():
            solved += 1
        else:
            nsolved += 1
    print(solved, nsolved)


if __name__ == '__main__':
    exp1(sys.argv[1])
    puzzle = (
        '005090347070026010891037600'
        '000069050907304802020870000'
        '009780534040950080583040200'
    )
    s = Sudoku.from_line(puzzle)
    print(s)
    print(s.solve())
    print(s)

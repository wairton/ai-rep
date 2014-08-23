from collections import namedtuple

#TODO this function is here because a didn't found a better place for it yet.
def hamming_distance(instance):
    """
    Hamming distance
    """
    missed = 0
    for i in range(len(self.puzzle)):
        if instance[i] == 0:
            continue
        if instance[i] != self.desired[i]:
            missed += 1
    return missed


class AStarState(namedtuple("Base", "h g state parent")):
    def __new__(cls, h, g, state, parent):
        return super().__new__(cls, h, g, state, parent)

    @property
    def f(self):
        return self.g + self.h


#TODO make this class abstract, maybe using ABC...
class AStarSolver:
    def __init__(self, instance, desired):
        self.instance = instance
        #TODO how to insert desired on class?
        self.desired = desired
        #TODO how to insert distance_function on class
        self.open = []
        self.closed = []

    def solve(self):
        self.open.append(AStarState(self.distance(self.instance), 0, self.instance, None))
        while len(self.open) > 0:
            current = self.pop_lowest()
            self.closed.append(current)
            if self.is_final_state(current.state):
                return self.build_solution(current)
            for new_state in self.generate(current):
                if self.on_closed(new_state):
                    continue
                self.insert_state(new_state)

    def pop_lowest(self):
        min_distance, index = float("inf") , 0
        for i, state in enumerate(self.open):
            current_distance = state.f
            if current_distance < min_distance:
                min_distance, index = current_distance, i
        return self.open.pop(index)

    def on_closed(self, new_state):
        for state in self.closed:
            if state.state == new_state.state:
                return True
        return False

    def is_final_state(self, state):
        raise NotImplementedError

    def generate(self, current):
        raise NotImplementedError

    def insert_state(self, new_state):
        for i, state in enumerate(self.open):
            if state.state == new_state.state:
                if state.f >= new_state.f:
                    self.open[i] = new_state
                return
        self.open.append(new_state)

    def build_solution(self, state):
        self.path = []
        while state.parent != None:
            self.path.append(state.state)
            state = state.parent
        self.path.append(state.state)
        return self.path[::-1]

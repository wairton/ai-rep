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


class AStarState(tuple):
    @property
    def g(self):
        return self[1]

    @property
    def h(self):
        return self[0]

    @property
    def f(self):
        return self.g + self.h

    @property
    def state(self):
        return self[2]

    @property
    def previous_move(self):
        return self[3]

    @property
    def parent(self):
        return self[4]

#TODO make this class abstract, maybe using ABC...
class AStarSolver:
    def __init__(self, instance, desired):
        self.instance = instance
        #TODO how to insert desired on class?
        self.desired = desired
        #TODO how to insert distance_function on class
        self.states = []

    def solve(self):
        #TODO create a new State without pass a tuple as parameter
        self.states.append(AStarState((self.distance(self.instance), 0, self.instance, 0, None)))
        while len(self.states) > 0:
            current = self.pop_closer()
            if current.state  == self.desired:
                return self.build_solution(current)
            for new_state in self.generate(current):
                self.insert_state(new_state)

    def pop_closer(self):
        min_distance, index = float("inf") , 0
        for i, state in enumerate(self.states):
            current_distance = state.f
            if current_distance < min_distance:
                min_distance, index = current_distance, i
        return self.states.pop(index)

    def generate(self, current):
        raise NotImplementedError

    def insert_state(self, new_state):
        for i, state in enumerate(self.states):
            if state.state == new_state.state:
                if state.f >= new_state.f:
                    self.states[i] = new_state
                return
        self.states.append(new_state)

    def build_solution(self, state):
        self.path = []
        while state.parent != None:
            self.path.append(state.state)
            state = state.parent
        self.path.append(state.state)
        return self.path[::-1]

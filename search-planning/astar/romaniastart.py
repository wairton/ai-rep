from astar import AStarSolver, AStarState
import json

class MapLoader:
    def __init__(self, filename):
        self.data = json.load(open(filename))

class BucharestMap:
    

class BucharestSolver(AStarSolver):
    def generate(self, current):
        import pdb; pdb.set_trace()
        h, g, current_city, previous_city, pointer = current
        next_steps = []
        for next_city, real_cost in self.map.data["neighborhood"][current_city]:
            if next_city == previous_city:
                continue
            next_steps.append((self.distance(next_city), g + real_cost, next_city, current_city, current))
        return next_steps

    def distance(self, cityname):
        return self.instance.data["straight_distance"][cityname]


if __name__ == '__main__':
    _map = Map("romania.json")
    while True:
        print("valid options", ' '.join(_map.data["cities"]))
        BucharestSolver(_map, input()).solve()

from functools import reduce
import random

class DiamondSquareGenerator:
    def __init__(self, terrain):
        self.terrain = terrain

    def average(self, values):
        valid = list(filter(lambda val: val != -1, values))
        total = reduce(lambda x, y: x + y, valid)
        return total / len(valid)

    def square(self, x, y, size, offset):
        avg = self.average([self.terrain.get(x - size, y - size), self.terrain.get(x + size, y - size),
                            self.terrain.get(x + size, y + size), self.terrain.get(x - size, y + size)])
        self.terrain.set(x, y, avg + offset)

    def diamond(self, x, y, size, offset):
        avg = self.average([self.terrain.get(x, y - size), self.terrain.get(x + size, y),
                            self.terrain.get(x, y + size), self.terrain.get(x - size, y)])
        self.terrain.set(x, y, avg + offset)

    def divide(self, size):
        x, y, half = size // 2, size // 2, size // 2
        scale = self.terrain.roughness * size
        if half < 1:
            return

        for y in range(half, self.terrain.max, size):
            for x in range(half, self.terrain.max, size):
                self.square(x, y, half, random.random() * scale * 2 - scale)

        for y in range(0, self.terrain.max + 1, half):
            for x in range((y + half) % size, self.terrain.max + 1, size):
                self.diamond(x, y, half, random.random() * scale * 2 - scale)

        self.divide(size // 2)

    # #this shit is unstable
    # def generate(self):
    #     self.terrain.set(0, 0, random.uniform(0, 1))
    #     self.terrain.set(1, 0, random.uniform(0, 1))
    #     self.terrain.set(1, 1, random.uniform(0, 1))
    #     self.terrain.set(0, 1, random.uniform(0, 1))
    #     self.divide(self.terrain.max)
    # #     #self.scale()

    #this shit is stable
    def generate(self):
        self.terrain.set(0, 0, random.uniform(0, self.terrain.max / 2))
        self.terrain.set(self.terrain.max, 0, random.uniform(0, self.terrain.max / 2))
        self.terrain.set(self.terrain.max, self.terrain.max, random.uniform(0, self.terrain.max / 2))
        self.terrain.set(0, self.terrain.max, random.uniform(0, self.terrain.max / 2))
        self.divide(self.terrain.max)
        self.scale()

    def scale(self):
        supermax = max([max(self.terrain.map[i]) for i in range(self.terrain.size)])
        # print("before max: ", supermax)
        # print("before min: ", min([min(self.terrain.map[i]) for i in range(self.terrain.size)]))
        for i in range(self.terrain.size):
            for j in range(self.terrain.size):
                self.terrain.set(i, j, self.terrain.get(i, j) / supermax)
        # print("after max: ", max([max(self.terrain.map[i]) for i in range(self.terrain.size)]))
        # print("after min: ", min([min(self.terrain.map[i]) for i in range(self.terrain.size)]))
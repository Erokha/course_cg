import diamondsquare as ds
import math
from enum import Enum
#import triangle

class terrainDescribe(Enum):
    describeMap = 1
    describeTrianguilationDeubg = 2
    pixelPointDescribeDebug = 3


class superTerrain:
    def __init__(self, detail, roughness):
        self.size = int(math.pow(2, detail)) + 1
        self.max = self.size - 1
        self.map = [0] * self.size
        self.triangulation = []
        self.roughness = roughness
        for i in range(self.size):
            self.map[i] = [0] * self.size

    def get(self, x, y):
        if x < 0 or x > self.max or y < 0 or y > self.max:
            return -1
        return self.map[y][x]

    def set(self, x, y, val):
        self.map[y][x] = val

    def describeSelf(self, option):
        res = ''
        if option == terrainDescribe.describeMap:
            for i in range(self.size):
                for j in range(self.size):
                    toprint = self.get(i, j)
                    res += str(round(toprint, 2)) + ' '
                res = '\n'
        elif option == terrainDescribe.describeTrianguilationDeubg:
            for triangle in self.triangulation:
                res += str(triangle) + '\n'
        return res

    def describeSelf(self, option, filename):
        f = open(filename, 'w')
        if option == terrainDescribe.describeMap:
            for i in range(self.size):
                for j in range(self.size):
                    toprint = self.get(i, j)
                    f.write(f'{round(toprint, 2)} ')
                f.write('\n')
        elif option == terrainDescribe.describeTrianguilationDeubg:
            for triangle in self.triangulation:
                f.write(f'{triangle}\n')
        elif option == terrainDescribe.pixelPointDescribeDebug:
            for x in range(self.size):
                for y in range(self.size):
                    f.write(f'{x}, {y}, {self.get(x, y)}\n')
        f.close()

    def triangulate(self):
        for i in range(self.size - 1):
            for j in range(self.size - 1):
                # ver of y and z changed position
                triangle1 = [i, self.get(i, j), j, i + 1, self.get(i + 1, j), j, i, self.get(i, j + 1), j + 1]
                triangle2 = [i + 1, self.get(i + 1, j + 1), j + 1, i + 1, self.get(i + 1, j), j, i, self.get(i, j + 1), j + 1]
            #     triangle1 = [i, j, self.get(i, j), i + 1, j, self.get(i + 1, j), i, j + 1, self.get(i, j + 1)]
            #     triangle2 = [i + 1, j + 1, self.get(i + 1, j + 1), i + 1, j, self.get(i + 1, j), i, j + 1, self.get(i, j + 1)]
                self.triangulation.append(triangle1)
                self.triangulation.append(triangle2)

        pass

    def generate(self):
        ds.DiamondSquareGenerator(self).generate()
        self.triangulate()
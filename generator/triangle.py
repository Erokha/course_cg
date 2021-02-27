import math
class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotateY(self, angle):
        cos = math.cos(angle * math.pi / 180)
        sin = math.sin(angle * math.pi / 180)
        tmp_x = self.x * cos + self.z * sin
        tmp_z = -self.x * sin + self.z * cos
        self.x = tmp_x
        self.z = tmp_z

    def rotateX(self, angle):
        cos = math.cos(angle * math.pi / 180)
        sin = math.sin(angle * math.pi / 180)
        tmp_y = self.y * cos - self.z * sin
        tmp_z = self.y * sin + self.z * cos
        self.y = tmp_y
        self.z = tmp_z

    def scale(self, xx, xy, xz):
        self.x *= xx
        self.y *= xy
        self.z *= xz

    def move(self, dx = 0, dy = 0, dz = 0):
        self.x += dx
        self.y += dy
        self.z += dz


class Point2d():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __init__(self, point3d):
        self.x = point3d.x
        self.y = point3d.y

class Triangle():
    def __init__(self, a: Point3d, b: Point3d, c: Point3d):
        self.a = a
        self.b = b
        self.c = c

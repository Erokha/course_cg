import math
from copy import deepcopy
from vector import Vector

class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return (f"Point: {self.x} {self.y} {self.z}")

    def pathLen(self, to):
        dx = self.x - to.x
        dy = self.y - to.y
        dz = self.z - to.z
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def rotateX(self, angle):
        cos = math.cos(angle * math.pi / 180)
        sin = math.sin(angle * math.pi / 180)
        tmp_y = self.y * cos - self.z * sin
        tmp_z = self.y * sin + self.z * cos
        self.y = tmp_y
        self.z = tmp_z

    def rotateY(self, angle):
        cos = math.cos(angle * math.pi / 180)
        sin = math.sin(angle * math.pi / 180)
        tmp_x = self.x * cos + self.z * sin
        tmp_z = -self.x * sin + self.z * cos
        self.x = tmp_x
        self.z = tmp_z

    def rotateZ(self, angle):
        cos = math.cos(angle * math.pi / 180)
        sin = math.sin(angle * math.pi / 180)
        tmp_x = self.x * cos - self.y * sin
        tmp_y = self.x * sin + self.y * cos
        self.x = tmp_x
        self.y = tmp_y

    def scale(self, xx, xy, xz):
        self.x *= xx
        self.y *= xy
        self.z *= xz

    def move(self, dx = 0, dy = 0, dz = 0):
        self.x += dx
        self.y += dy
        self.z += dz

    def getAsTuple(self):
        return self.x, self.y, self.z

    def rotateAround(self, xangle, yangle, zangle, around):
        self.move(-around.x, -around.y, -around.z)
        self.rotateY(yangle)
        self.rotateX(xangle)
        self.rotateZ(zangle)
        self.move(around.x, around.y, around.z)


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

    def avg(self) -> Point3d:
        avgx = (self.a.x + self.b.x + self.c.x) / 3
        avgy = (self.a.y + self.b.y + self.c.y) / 3
        avgz = (self.a.z + self.b.z + self.c.z) / 3
        return Point3d(avgx, avgy, avgz)

    def pathLen(self, to: Point3d):
        fromPoint = self.avg()
        return fromPoint.pathLen(to)


    def move(self, dx, dy, dz):
        self.a.move(dx, dy, dz)
        self.b.move(dx, dy, dz)
        self.c.move(dx, dy, dz)

    def getRotatedTriangle(self, xangle, yangle, zangle, around = Point3d(0, 0, 0)):
        rota = deepcopy(self.a)
        rotb = deepcopy(self.b)
        rotc = deepcopy(self.c)
        mas = [rota, rotb, rotc]
        for point in mas:
            point.rotateAround(xangle, yangle, zangle, around)
            # point.move(-around.x, -around.y, -around.z)
            # point.rotateY(yangle)
            # point.rotateX(xangle)
            # point.rotateZ(zangle)
            # point.move(around.x, around.y, around.z)
        return Triangle(rota, rotb, rotc)

    def getXRotatedTriangle(self, angle, around = Point3d(0, 0, 0)):
        rota = deepcopy(self.a)
        rotb = deepcopy(self.b)
        rotc = deepcopy(self.c)
        mas = [rota, rotb, rotc]
        for point in mas:
            point.move(-around.x, -around.y, -around.z)
            point.rotateX(angle)
            point.move(around.x, around.y, around.z)
        return Triangle(rota, rotb, rotc)

    def getYRotatedTriangle(self, angle, around = Point3d(0, 0, 0)):
        rota = deepcopy(self.a)
        rotb = deepcopy(self.b)
        rotc = deepcopy(self.c)
        mas = [rota, rotb, rotc]
        for point in mas:
            point.move(-around.x, -around.y, -around.z)
            point.rotateY(angle)
            point.move(around.x, around.y, around.z)
        return Triangle(rota, rotb, rotc)

    def __str__(self):
        return f"{str(self.a)}\n{str(self.b)}\n{str(self.c)}\n"

    #bad idea, better to use filter
    def getMaxPoint(self):
        pass

    def getAsPureArray(self):
        return [self.a.getAsTuple(), self.b.getAsTuple(), self.c.getAsTuple()]

    def getEquation(self):
        v1 = Vector.createVectorFromPoints(self.a, self.b)
        v2 = Vector.createVectorFromPoints(self.a, self.c)
        n = Vector.vectorMultiply(v1, v2)
        cfa, cfb, cfc = n.x, n.y, n.z
        cfd = cfa * -self.a.x + cfb * -self.a.y + cfc * -self.a.z
        return (cfa, cfb, cfc, cfd)

    def getNormal(self) -> Vector:
        v1 = Vector.createVectorFromPoints(self.a, self.b)
        v2 = Vector.createVectorFromPoints(self.a, self.c)
        return Vector.vectorMultiply(v1, v2)

    def getNormal(self) -> Vector:
        vx1 = self.b.x - self.a.x
        vy1 = self.b.y - self.a.y
        vz1 = self.b.z - self.a.z
        vx2 = self.b.x - self.c.x
        vy2 = self.b.y - self.c.y
        vz2 = self.b.z - self.c.z

        n = Vector.setVector(vy1 * vz2 - vz1 * vy2, vx1 * vz2 - vz1 * vx2, vx1 * vy2 - vy1 * vx2)
        wrki = math.sqrt((vy1 * vz2 - vz1 * vy2)**2 + (vz1 * vx2 - vx1 * vz2)**2 + (vx1 * vy2 - vy1 * vx2)**2)
        if wrki:
            n.x /= wrki
            n.y /= wrki
            n.z /= wrki

        return n

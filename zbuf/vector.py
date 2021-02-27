from math import sqrt
class Vector:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x = x2 - x1
        self.y = y2 - y1
        self.z = z2 - z1

    @classmethod
    def createVectorFromPoints(cls, pointA, pointB):
        # only Point3d allowed
        x = pointB.x - pointA.x
        y = pointB.y - pointA.y
        z = pointB.z - pointA.z
        return cls.setVector(x, y, z)

    @classmethod
    def setVector(cls, x, y, z):
        return Vector(0, 0, 0, x, y, z)

    def __str__(self):
        return f"vector: {self.x} {self.y} {self.z}"

    @classmethod
    def vectorMultiply(cls, a, b):
        return Vector.setVector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def cosOfAngle(a: Vector, b: Vector):
    return (a.x * b.x + a.y * b.y + a.z * b.z) / (sqrt(a.x**2 + a.y**2 + a.z**2) * sqrt(b.x**2 + b.y**2 + b.z**2))

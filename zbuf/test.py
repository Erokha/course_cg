import vector as v
import triangle as t
import math

a = t.Point3d(-3, 2, 1)
b = t.Point3d(-1, 2, 4)
c = t.Point3d(3, 3, -1)
tr = t.Triangle(b, c, a)
coef = tr.getEquation()
print(coef)
print(c.x * coef[0] + c.y * coef[1] + c.z * coef[2] + coef[3])

# a = v.Vector.createVector(2, 0, 5)
# b = v.Vector.createVector(6, 1, 0)
# print(v.Vector.vectorMultiply(a, b))



# a = triangle.Point3d(0, 0, 0)
# b = triangle.Point3d(0, 0, 100)
# c = triangle.Point3d(0, 100, 0)
#
# tr = triangle.Triangle(a, b, c)
# normal = tr.getNormal()
# print(normal)
# LIGHT_VECTOR = vector.Vector(0, 0, 10)
# angle = vector.cosOfAngle(normal, LIGHT_VECTOR)
# print(angle)

# import tkinter as tk
import triangle as gr
import math


def getTrinagles():
    f = open('result.txt')
    triangles = []
    for line in f.readlines():
        triangles.append([float(point) for point in line.replace('[', '').replace(']', '').split(',')])

    newtriangle = []
    for triangle in triangles:
        point1 = gr.Point3d(*triangle[0:3])
        # point1.scale(scalex, scaley, scalez)
        point2 = gr.Point3d(*triangle[3:6])
        # point2.scale(scalex, scaley, scalez)
        point3 = gr.Point3d(*triangle[6:9])
        # point3.scale(scalex, scaley, scalez)
        newtriangle.append(gr.Triangle(point1, point2, point3))
    return newtriangle


# triangles = getTrinagles()
# triangles = [gr.Triangle(gr.Point3d(-100, 100, 100), gr.Point3d(-100, -100, 0), gr.Point3d(100, 100, 0))]
# triangles.append(gr.Triangle(gr.Point3d(100, -100, 100), gr.Point3d(-100, -100, 0), gr.Point3d(100, 100, 0)))


import sys, random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


def allrotatex(model, angle):
    for i in range(len(model)):
        model[i].a.rotateX(angle)
        model[i].b.rotateX(angle)
        model[i].c.rotateX(angle)


def allrotatey(model, angle):
    for i in range(len(model)):
        model[i].a.rotateY(angle)
        model[i].b.rotateY(angle)
        model[i].c.rotateY(angle)


def scalePoints(scalex, scaley, scalez, array):
    for i in range(len(array)):
        array[i].a.scale(scalex, scaley, scalez)
        array[i].b.scale(scalex, scaley, scalez)
        array[i].c.scale(scalex, scaley, scalez)

def movePaints(dx, dy, dz, array):
    for i in range(len(array)):
        array[i].a.move(dx, dy, dz)
        array[i].b.move(dx, dy, dz)
        array[i].c.move(dx, dy, dz)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.setupModel()
        self.initUI()

    def setupModel(self):
        self.model = getTrinagles()
        scalePoints(25, 25, 105, self.model)
        movePaints(-self.height() // 5, -self.width() // 5, 0, self.model)

    def setupButtons(self):
        self.xupRotButton = QPushButton('^', self)
        self.xupRotButton.clicked.connect(self.rotateXpos)

        self.yupRotButton = QPushButton('<', self)
        self.yupRotButton.clicked.connect(self.rotateYpos)
        self.yupRotButton.move(42, 0)

        self.xdownRotButton = QPushButton('V', self)
        self.xdownRotButton.clicked.connect(self.rotateXneg)
        self.xdownRotButton.move(0, 24)

        self.ydownRotButton = QPushButton('>', self)
        self.ydownRotButton.clicked.connect(self.rotateYneg)
        self.ydownRotButton.move(42, 24)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Points')
        self.setupButtons()


        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def myDrawLine(self, qp: QPainter, a: gr.Point3d, b: gr.Point3d):
        atmp = gr.Point3d(a.x + (self.width() // 2), -a.y + (self.height() // 2), a.z)
        btmp = gr.Point3d(b.x + (self.width() // 2), -b.y + (self.height() // 2), b.z)
        qp.drawLine(atmp.x, atmp.y, btmp.x, btmp.y)

    def drawTriangle(self, qp: QPainter, triangle: gr.Triangle):
        self.myDrawLine(qp, triangle.a, triangle.b)
        self.myDrawLine(qp, triangle.b, triangle.c)
        self.myDrawLine(qp, triangle.a, triangle.c)

    def rotateXpos(self):
        allrotatex(self.model, 10)
        self.update()

    def rotateYpos(self):
        allrotatey(self.model, 10)
        self.update()

    def rotateXneg(self):
        allrotatex(self.model, -10)
        self.update()

    def rotateYneg(self):
        allrotatey(self.model, -10)
        self.update()

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        for triangle in self.model:
            self.drawTriangle(qp, triangle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

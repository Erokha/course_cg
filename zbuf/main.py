import sys, random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QBitmap, QImage, QPaintEvent
from PyQt5.QtCore import Qt
import triangle as tr
from vector import Vector, cosOfAngle
from math import ceil, floor, inf, acos, pi, sqrt


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
MINIX = None
MAXIX = None
MINIY = None
MAXIY = None
MAXIZ = None
MINIZ = None
MIDDLPOINT = None
LIGHTPOINT = tr.Point3d(100, 700, 100)



def getTrinagles():
    global MINIY, MAXIY, MINIX, MINIY, MINIZ, MAXIZ, MIDDLPOINT
    f = open('result.txt')
    triangles = []
    MINIY = inf
    MAXIY = -inf
    MINIX = inf
    MAXIX = -inf
    MINIZ = inf
    MAXIZ = -inf
    for line in f.readlines():
        triangles.append([(float(point)) for point in line.replace('[', '').replace(']', '').split(',')])

    newtriangle = []
    big = 20#110
    reg = 20#35
    for triangle in triangles:
        MAXIX = max(MAXIX, triangle[0], triangle[3], triangle[6])
        MINIX = min(MINIX, triangle[0], triangle[3], triangle[6])

        MAXIY = max(MAXIY, triangle[1], triangle[4], triangle[7])
        MINIY = min(MINIY, triangle[1], triangle[4], triangle[7])

        MAXIZ = max(MAXIZ, triangle[2], triangle[5], triangle[8])
        MINIZ = min(MINIZ, triangle[2], triangle[5], triangle[8])

    xmultiplier = (SCREEN_WIDTH / 1.7) / max(abs(MINIX), abs(MAXIX))
    ymultiplier = (SCREEN_HEIGHT / 3) / max(abs(MINIY), abs(MAXIY))
    zmultiplier = (SCREEN_HEIGHT / 3) / max(abs(MINIZ), abs(MAXIZ))
    # #This is stable
    # MINIY *= xmultiplier
    # MAXIY *= xmultiplier
    # MAXIX *= xmultiplier
    # MINIX *= xmultiplier
    # MAXIZ *= xmultiplier
    # MINIZ *= xmultiplier

    MINIY *= ymultiplier
    MAXIY *= ymultiplier
    MAXIX *= xmultiplier
    MINIX *= xmultiplier
    MAXIZ *= zmultiplier
    MINIZ *= zmultiplier
    MIDDLPOINT = tr.Point3d((MINIX + MAXIX) / 2, (MINIY + MAXIY) / 2, (MINIZ + MAXIZ) / 2)
    MIDDLPOINT.move(-SCREEN_WIDTH / 2.5, -SCREEN_HEIGHT / 5, 0)
    MINIY -= SCREEN_HEIGHT / 4
    MAXIY -= SCREEN_HEIGHT / 4


    for triangle in triangles:
        # #This is stable
        # triangle[0] *= xmultiplier
        # triangle[1] *= xmultiplier
        # triangle[2] *= xmultiplier
        # triangle[3] *= xmultiplier
        # triangle[4] *= xmultiplier
        # triangle[5] *= xmultiplier
        # triangle[6] *= xmultiplier
        # triangle[7] *= xmultiplier

        triangle[0] *= xmultiplier
        triangle[1] *= ymultiplier
        triangle[2] *= zmultiplier
        triangle[3] *= xmultiplier
        triangle[4] *= ymultiplier
        triangle[5] *= zmultiplier
        triangle[6] *= xmultiplier
        triangle[7] *= ymultiplier
        triangle[8] *= zmultiplier

        for i in range(len(triangle)):
            triangle[i] = floor(triangle[i])
        point1 = tr.Point3d(*triangle[0:3])
        point2 = tr.Point3d(*triangle[3:6])
        point3 = tr.Point3d(*triangle[6:9])
        newitem = tr.Triangle(point1, point2, point3)
        newitem.move(-SCREEN_WIDTH / 2.5, -SCREEN_HEIGHT / 5, 0)
        newtriangle.append(newitem)
    return newtriangle


class ViewController(QWidget):

    def __init__(self):
        super().__init__()
        self.initzbuf()
        self.model = getTrinagles()
        self.lightpoint = MIDDLPOINT
        self.lightpoint.y += 200
        self.toggleCheatMode = True
        self.needRedraw = False
        self.xangle = 0
        self.yangle = 0
        self.zangle = 0
        self.initUI()

    def changeLightPoint(self, x, y, z):
        self.lightpoint = tr.Point3d(x, y, z)

    def modelToZBuf(self, triagnle_array, color, equation):
        import math
        def Interpolate (i0, d0, i1, d1):
            if i0 == i1:
               return [int(d0)]
            values = []
            a = (d1 - d0) / (i1 - i0)
            d = d0
            for i in range(int(i0), int(i1)):
                values.append(int(d))
                d = d + a
            return values

        def DrawLine(x0, y0, x1, y1):
            if abs(x1 - x0) > abs(y1 - y0):
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                ys = Interpolate(x0, y0, x1, y1)
                for x in range(x0, x1):
                    if equation[2] != 0:
                        z = round((-equation[0] * x - equation[1] * ys[x - x0] - equation[3]) / equation[2])
                    else:
                        z = math.inf
                    self.checkZbuf(x, ys[x - x0], z, color)
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                xs = Interpolate(y0, x0, y1, x1)
                for y in range(y0, y1):
                    if equation[2] != 0:
                        z = round((-equation[0] * xs[y - y0] - equation[1] * y - equation[3]) / equation[2])
                    else:
                        z = -math.inf
                    self.checkZbuf(xs[y - y0], y, z, color)
        def strokeCheat():
            DrawLine(x0, y0, x1, y1)
            DrawLine(x0, y0, x2, y2)
            DrawLine(x1, y1, x2, y2)

        triagnle_array.sort(key=lambda tup: tup[1])
        x0, y0, z0 = [round(i) for i in triagnle_array[0]]
        x1, y1, z1 = [round(i) for i in triagnle_array[1]]
        x2, y2, z2 = [round(i) for i in triagnle_array[2]]
        x01 = Interpolate(y0, x0, y1, x1)
        x12 = Interpolate(y1, x1, y2, x2)
        x02 = Interpolate(y0, x0, y2, x2)
        if self.toggleCheatMode:
            strokeCheat()

        x01 = x01
        x012 = x01 + x12
        m = (len(x012) // 2) - 1
        if x02[m] < x012[m]:
            x_left = x02
            x_right = x012
        else:
            x_left = x012
            x_right = x02

        for y in range(int(y0), int(y2)):
            for x in range(x_left[y - int(y0)], x_right[y - int(y0)]):
                if equation[2] != 0:
                    z = round((-equation[0] * x - equation[1] * y - equation[3]) / equation[2])
                else:
                    z = -math.inf
                self.checkZbuf(x, y, z, color)

    def checkZbuf(self, x, y, z, color):
        try:
            xtmp = x + (SCREEN_WIDTH // 2)
            ytmp = -y + (SCREEN_HEIGHT // 2)
            if z > self.zbuf[xtmp][ytmp][0] and xtmp >= 0 and ytmp >= 0:
                self.zbuf[xtmp][ytmp] = [z, color]
        except Exception as e:
            pass

    def zbuf_cheat(self):
        import math
        for y in range(SCREEN_HEIGHT - 1):
            for x in range(SCREEN_WIDTH - 1):
                if self.zbuf[x][y][0] == -math.inf and (y < SCREEN_HEIGHT - 2 and y != 0) and (x < SCREEN_WIDTH - 2 and x != 0):
                    if self.zbuf[x][y + 1][1] and self.zbuf[x][y - 1][1]:
                        res = [self.zbuf[x][y - 1], self.zbuf[x][y + 1]]
                        res.sort(key= lambda tup: tup[0])
                        self.zbuf[x][y][1] = res[0][1]
                    elif self.zbuf[x + 1][y][1] and self.zbuf[x - 1][y][1]:
                        res = [self.zbuf[x + 1][y], self.zbuf[x - 1][y]]
                        res.sort(key=lambda tup: tup[0])
                        self.zbuf[x][y][1] = res[0][1]

    def drawFromZbuf(self, qp):
        pixmap = QPixmap(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.image.fill(Qt.black)
        for y in range(SCREEN_HEIGHT - 1):
            for x in range(SCREEN_WIDTH - 1):
                if self.zbuf[x][y][1]:
                   self.image.setPixelColor(x, y, self.zbuf[x][y][1])
                    #qp.setPen(self.zbuf[x][y][1])
                    #qp.drawPoint(x, y)
        self.canvas.setPixmap(QPixmap(self.image))



    def comapreToZbuf(self, x, y, z):
        try:
            if z >= self.zbuf[x][y][0]:
                self.zbuf[x][y][0] = z
                return True
            else:
                return False
        except:
            return False

    def drawLightPoint(self, qp):
        qp.setBrush(Qt.yellow)
        x = self.lightpoint.x + (SCREEN_WIDTH // 2)
        y = -self.lightpoint.y + (SCREEN_HEIGHT // 2)
        qp.drawEllipse(x - 2, y - 2, x + 2, y + 2)

    def rotateXpos(self):
        self.xangle += 15
        self.xangle %= 360
        self.update()

    def toggleCheat(self):
        self.toggleCheatMode = not self.toggleCheatMode
        self.needLayout()

    def rotateXneg(self):
        self.xangle -= 15
        self.xangle %= 360
        self.update()

    def rotateYpos(self):
        self.yangle += 15
        self.yangle %= 360
        self.update()

    def rotateYneg(self):
        self.yangle -= 15
        self.yangle %= 360
        self.update()

    def initzbuf(self):
        import math
        self.zbuf = [[[-math.inf, None] for _ in range(SCREEN_WIDTH - 1)] for _ in range(SCREEN_HEIGHT - 1)]


    def strokeTriangle(self, triagnle_array, qp):
        x1, y1, z1 = triagnle_array[0][0], triagnle_array[0][1], triagnle_array[0][2]
        x2, y2, z2 = triagnle_array[1][0], triagnle_array[1][1], triagnle_array[1][2]
        x3, y3, z3 = triagnle_array[2][0], triagnle_array[2][1], triagnle_array[2][2]
        qp.setPen(Qt.red)
        qp.drawLine(x1 + (SCREEN_WIDTH // 2), -y1 + (SCREEN_HEIGHT // 2), x2 + (SCREEN_WIDTH // 2),
                    -y2 + (SCREEN_HEIGHT // 2))
        qp.drawLine(x2 + (SCREEN_WIDTH // 2), -y2 + (SCREEN_HEIGHT // 2), x3 + (SCREEN_WIDTH // 2),
                    -y3 + (SCREEN_HEIGHT // 2))
        qp.drawLine(x1 + (SCREEN_WIDTH // 2), -y1 + (SCREEN_HEIGHT // 2), x3 + (SCREEN_WIDTH // 2),
                    -y3 + (SCREEN_HEIGHT // 2))



    def draw3dTriangle(self, triagnle_array, color):
        drawn = 0
        triagnle_array.sort(key=lambda tup: tup[1])
        x1, y1, z1 = triagnle_array[0][0], triagnle_array[0][1], triagnle_array[0][2]
        x2, y2, z2 = triagnle_array[1][0], triagnle_array[1][1], triagnle_array[1][2]
        x3, y3, z3 = triagnle_array[2][0], triagnle_array[2][1], triagnle_array[2][2]

        dx13 = 0
        dz13 = 0
        dx12 = 0
        dz12 = 0
        dx23 = 0
        dz23 = 0

        if (y3 != y1):
            dx13 = (x3 - x1) / (y3 - y1)
            dz13 = (z3 - z1) / (y3 - y1)


        if (y2 != y1):
            dx12 = (x2 - x1) / (y2 - y1)
            dz12 = (z2 - z1) / (y2 - y1)

        if (y3 != y2):
            dx23 = (x3 - x2) / (y3 - y2)
            dz23 = (z3 - z2) / (y3 - y2)

        wx1 = x1
        wz1 = z1
        wx2 = wx1
        wz2 = wz1

        _dx13 = dx13
        _dz13 = dz13

        if dx13 > dx12:
            dx13, dx12 = dx12, dx13
            dz13, dz12 = dz12, dz13

        if wx2 < wx1:
            wx1, wx2 = wx2, wx1
            wz1, wz2 = wz2, wz1

        for y in range(int(y1), int(y2)):
            z = wz1
            rng = range(int(wx1), int(wx2) + 1)
            if len(rng):
                for x in rng:
                    self.checkZbuf(x, y, z, color)
                    drawn += 1
                    z += (wz2 - wz1) / len(rng)
            else:
                self.checkZbuf(wx1, y, z, color)
            wx1 += dx13
            wz1 += dz13
            wx2 += dx12
            wz2 += dz12


        if (y1 == y2):
            wx1 = x1
            wz1 = z1
            wx2 = x2
            wz2 = z2

        if (_dx13 < dx23):
            _dx13, dx23 = dx23, _dx13
            _dz13, dz23 = dz23, _dz13

        if wx2 < wx1:
            wx1, wx2 = wx2, wx1
            wz1, wz2 = wz2, wz1

        for y in range(int(y2), int(y3)):
            z = wz1
            rng = range(int(wx1), int(wx2) + 1)
            if len(rng):
                for x in rng:
                    self.checkZbuf(x, y, z, color)
                    drawn += 1
                    z += (wz2 - wz1) / len(rng)
            else:
                self.checkZbuf(int(wx1), y, z, color)
            wx1 += _dx13
            wz1 += _dz13
            wx2 += dx23
            wz2 += dz23

    def initLabelWithTextField(self, y, labeltext, defaultvalue, labeloffset = 0):
        textfield = QLineEdit(self)
        textfield.setStyleSheet("color: rgb(255, 255, 255);")
        textfield.setText(f"{defaultvalue}")
        textfield.move(SCREEN_WIDTH + 150 - textfield.width(), y)

        label = QLabel(self)
        label.setText(f"{labeltext}")
        label.setStyleSheet("color: rgb(255, 255, 255);")
        label.move(SCREEN_WIDTH + 150 - textfield.width() - 50 - labeloffset, y - 20)
        return label, textfield

    def showError(self, title, additionalText):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"{title}")
        msg.setInformativeText(f"{additionalText}")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def somefunc(self):
        import os
        #TODO sould be read from textFields
        roughness = 0.35
        detail = 6
        try:
            detail = int(self.detailTextField.text())
            if detail > 7:
                self.showError("Ошибка", "значение 'детализированность' не может быть более 7")
                return
            if detail < 2:
                self.showError("Ошибка", "значение 'детализированность' не может быть менее 2")
                return
        except Exception:
            self.showError("Ошибка", "значение 'шероховатость' не может быть представлено как число")
            return
        try:
            roughness = float(self.roughnessTextField.text())
            if roughness > 0.8:
                self.showError("Ошибка", "значение 'шероховатость' не может быть более 0.8")
                return
            if roughness < 0.001:
                self.showError("Ошибка", "значение 'шероховатость' не может быть менее 0.001")
                return
        except Exception:
            self.showError("Ошибка", "значение 'шероховатость' не может быть представлено как число")
            return
        print(detail)
        os.system(f'pypy3 ../generator/generator/toFile.py {detail} {roughness}')
        self.model = getTrinagles()
        print(MINIY)
        self.needLayout()

    def initUI(self):
        self.setGeometry(SCREEN_WIDTH + 200, SCREEN_HEIGHT, SCREEN_WIDTH + 200, SCREEN_HEIGHT)


        self.image = QImage(SCREEN_WIDTH, SCREEN_HEIGHT, 4)
        self.image.fill(Qt.black)
        self.canvas = QLabel(self)
        self.canvas.setPixmap(QPixmap(self.image))


        self.setStyleSheet("background-color: black;")
        self.setWindowTitle('Zbuff')

        self.xRotationLabel, self.xRotationTextField = self.initLabelWithTextField(20, "Угол вращения вокруг OX", 32)
        self.yRotationLabel, self.yRotationTextField = self.initLabelWithTextField(80, "Угол вращения вокруг OY", 46)
        self.zRotationLabel, self.zRotationTextField = self.initLabelWithTextField(140, "Угол вращения вокруг OZ", 0)
        self.roughnessLabel, self.roughnessTextField = self.initLabelWithTextField(200, "Шероховатость ландшафта", 0.35)
        self.detailLabel, self.detailTextField = self.initLabelWithTextField(250, "Детализированность ландшафта", 6, 35)
        # self.xLightPointLabel, self.xLightPointTextField = self.initLabelWithTextField(290, "X источника света", int(self.lightpoint.x))
        # self.yLightPointLabel, self.yLightPointTextField = self.initLabelWithTextField(330, "Y источника света", int(self.lightpoint.y))
        # self.zLightPointLabel, self.zLightPointTextField = self.initLabelWithTextField(370, "Z источника света", int(self.lightpoint.z))

        self.go = QPushButton('Поехали', self)
        self.go.clicked.connect(self.needLayout)
        self.go.setStyleSheet("background-color: white;")
        self.go.move(SCREEN_WIDTH + 100, 300)

        self.reGenerateButton = QPushButton('Перегенерировать', self)
        #self.reGenerateButton.clicked.connect(self.toggleCheat)
        self.reGenerateButton.clicked.connect(self.somefunc)
        self.reGenerateButton.setStyleSheet("background-color: white;")
        self.reGenerateButton.move(SCREEN_WIDTH + 50, 350)



        # self.yupRotButton = QPushButton('<', self)
        # self.yupRotButton.clicked.connect(self.rotateYpos)
        # self.yupRotButton.setStyleSheet("background-color: white;")
        # self.ydownRotButton = QPushButton('>', self)
        # self.ydownRotButton.clicked.connect(self.rotateYneg)
        # self.ydownRotButton.move(60, 0)
        # self.ydownRotButton.setStyleSheet("background-color: white;")
        #
        # self.xupRotButton = QPushButton('V', self)
        # self.xupRotButton.clicked.connect(self.rotateXpos)
        # self.xupRotButton.setStyleSheet("background-color: white;")
        # self.xupRotButton.move(0, 60)
        # self.xdownRotButton = QPushButton('^', self)
        # self.xdownRotButton.clicked.connect(self.rotateXneg)
        # self.xdownRotButton.move(60, 60)
        # self.xdownRotButton.setStyleSheet("background-color: white;")
        #
        # self.toggleStrokeButton = QPushButton("Toggle stroke", self)
        # self.toggleStrokeButton.clicked.connect(self.toggleStroke)
        # self.toggleStrokeButton.setStyleSheet("background-color: white;")
        # self.toggleStrokeButton.move(200, 0)


        self.show()

    def needLayout(self):
        self.needRedraw = True
        # X
        try:
            self.xangle = int(self.xRotationTextField.text()) % 360
        except Exception:
            self.needRedraw = False
            self.showError("Ошибка", "значение 'угол поворота вокруг оси OX' не может быть представлено как число")

        # Y
        try:
            self.yangle = int(self.yRotationTextField.text()) % 360
        except Exception:
            self.needRedraw = False
            self.showError("Ошибка", "значение 'угол поворота вокруг оси OY' не может быть представлено как число")

        # Z
        try:
            self.zangle = int(self.zRotationTextField.text()) % 360
        except Exception:
            self.needRedraw = False
            self.showError("Ошибка", "значение 'угол поворота вокруг оси OZ' не может быть представлено как число")

        self.update()

    def paintEvent(self, e: QPaintEvent):
        #print(e)
        #qp = QPainter()
        #qp.begin(self)
        if self.needRedraw:
            self.initzbuf()
            for i in range(len(self.model)):
                avg = self.model[i].avg()
                #avg = self.model[i].a
                # TODO try to get int from text field
                # TODO lightpoint?
                # xlight = int(float(self.xLightPointTextField.text()))
                # ylight = int(float(self.yLightPointTextField.text()))
                # zlight = int(float(self.zLightPointTextField.text()))
                # self.lightpoint = tr.Point3d(xlight, ylight, zlight)
                # self.lightpoint.rotateAround(self.xangle, self.yangle, self.zangle, MIDDLPOINT)
                #self.drawLightPoint(qp)
                m = self.model[i].getRotatedTriangle(self.xangle, self.yangle, self.zangle, MIDDLPOINT)
                yAbs = abs(MINIY) + abs(MAXIY)
                y = (avg.y + abs(MINIY)) / yAbs
                if y > 0.92:
                    color = QColor(Qt.white)
                elif y > 0.8:
                    color = QColor(Qt.gray)
                elif y > 0.75:
                    color = QColor(Qt.darkGray)
                elif y > 0.6:
                    color = QColor(Qt.darkGreen)
                elif y > 0.45:
                    color = QColor(Qt.green)
                elif y > 0.15:
                    color = QColor(Qt.blue)
                else:
                    color = QColor(Qt.darkBlue)
                n = self.model[i].getNormal()
                l = Vector(avg.x, avg.y, avg.z, self.lightpoint.x, self.lightpoint.y, self.lightpoint.z)
                ia = 0.3
                ka = 0.3
                il = 0.8
                kd = 0.8
                try:
                    I = abs(ia * ka + il * kd * (n.x * l.x + n.y * l.y + n.z * l.z) / (
                        sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2) * sqrt(l.x ** 2 + l.y ** 2 + l.z ** 2)))
                except ZeroDivisionError:
                    I = 1
                color = color.darker(int(300 - I * 200))
                self.modelToZBuf(m.getAsPureArray(), color, m.getEquation())
                #self.strokeTriangle(m.getAsPureArray(), qp)
            if self.toggleCheatMode:
                for i in range(15):
                    self.zbuf_cheat()
            self.drawFromZbuf(None)#(qp)
            self.needRedraw = False
        #qp.end()

    def putPoint(self, qp, color, x, y, z):
        qp.setPen(color)
        # xtmp = x + (self.width() // 2)
        # ytmp = -y + (SCREEN_HEGHT // 2)
        self.checkZbuf(x, y, z, color)
        # if self.comapreToZbuf(x, y, z):
        #     self.zbuf[x][y]
        #     qp.drawPoint(xtmp, ytmp)


    def put2dPoint(self, qp, color, x, y, z):
        qp.setPen(color)
        qp.drawPoint(x, y)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ViewController()
    sys.exit(app.exec_())

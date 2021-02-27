from generator import terrain
import erokhawatch
FILENAME = 'justfortest.txt'
ROUGH = 0.35

def testfunc(detail):
    ter = terrain.superTerrain(detail, ROUGH)
    ter.generate()
    a = ter.describeSelf(terrain.terrainDescribe.describeTrianguilationDeubg, FILENAME)

for detail in range(2, 12):
    time = erokhawatch.realwatch(testfunc, [detail])
    print(detail, "-", time)
import terrain
import sys

if __name__ == '__main__':
    try:
        detail = int(str(sys.argv[1]))
    except Exception as e:
        print(e)
        detail = 5
    try:
        rough = float(str(sys.argv[2]))
    except Exception as e:
        print(e)
        rough = 0.35
    try:
        filename = str(sys.argv[3])
    except Exception as e:
        print(e)
        filename = './result.txt'

    ter = terrain.superTerrain(detail, rough)
    ter.generate()
    #a = ter.describeSelf(terrain.terrainDescribe.pixelPointDescribeDebug, 'pixel.txt')
    a = ter.describeSelf(terrain.terrainDescribe.describeTrianguilationDeubg, './result.txt')
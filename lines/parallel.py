#!/usr/bin/env python
from __future__ import division

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

def getLinePara(line):
    line.a = line.p1.y - line.p2.y
    line.b = line.p2.x - line.p1.x
    line.c = line.p1.x * line.p2.y - line.p1.y * line.p2.x

def getCross(line1, line2):
    getLinePara(line1)
    getLinePara(line2)
    D = line1.a * line2.b - line2.a * line1.b
    if D == 0:
        # lines parallel
        return (None, None)
    x = (line1.b * line2.c - line2.b * line1.c) / D
    y = (line1.c * line2.a - line2.c * line1.a) / D
    return (x, y)

if __name__ == "__main__":
    line1 = Line(Point(0, 0), Point(1, 1))
    line2 = Line(Point(1, 0), Point(2, 1))
    print getCross(line1, line2)
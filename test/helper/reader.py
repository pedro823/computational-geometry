from geocomp.common.point   import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment


def read_points(filename):
    with open(filename) as file:
        points = set()
        for line in file:
            line = line.split()
            if len(line) != 2:
                raise ValueError(
                    "Invalid input from file: {}: {}".format(filename, line))
            points.add(Point(float(line[0]), float(line[1])))
        return points


def read_segments(filename):
    if filename is None:
        raise ValueError("File name is None")
    with open(filename) as file:
        segments = set()
        for line in file:
            line = line.split()
            if len(line) != 4:
                raise ValueError(
                    "Invalid input from file: {}: {}".format(filename, line))
            segments.add(
                Segment(
                    Point(float(line[0]), float(line[1])),
                    Point(float(line[2]), float(line[3]))
                )
            )
        return segments


def read_intersections(filename):
    if filename is None:
        raise ValueError("File name is None")
    with open(filename) as file:
        intersections = {}
        point = None
        for line in file:
            line = line.split()
            if len(line) == 2:
                point = Point(float(line[0]), float(line[1]))
                intersections[point] = set()
            if len(line) == 4:
                intersections[point].add(
                    Segment(
                        Point(float(line[0]), float(line[1])),
                        Point(float(line[2]), float(line[3]))
                    )
                )
        return intersections


def read_polygons(filename):
    if filename is None:
        raise ValueError("File name is None")
    with open(filename) as file:
        polygons = []
        vertices = []
        for line in file:
            line = line.split()
            if len(line) == 0:
                polygons.append(Polygon(vertices))
                vertices = []
                continue
            if len(line) != 2:
                raise ValueError(
                    "Invalid input from file: {}: {}".format(filename, line))
            vertices.append(Point(float(line[0]), float(line[1])))
        polygons.append(Polygon(vertices))
        return polygons


def read_point_link(filename):
    if filename is None:
        raise ValueError("File name is None")
    with open(filename) as file:
        link = {}
        for line in file:
            line = line.split()
            if len(line) != 4:
                raise ValueError(
                    "Invalid input from file: {}: {}".format(filename, line))
            key = Point(float(line[0]), float(line[1]))
            adj = Point(float(line[2]), float(line[3]))
            if key not in link:
                link[key] = set()
            link[key].add(adj)
        return link

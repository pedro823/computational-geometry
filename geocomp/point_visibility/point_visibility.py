from geocomp.common.segment import Segment
from geocomp.common.point import Point
from utils.type_checker import type_checked
from geocomp.common.prim import dist2
from itertools import izip, islice
import math

class SegmentReference:
    def __init__(self, segment: Segment, point: Point):
        self.segment = segment
        self.point = point

    def __lt__(self, other):
        return other.segment.has_left(self.point)

@type_checked()
def angle_from_origin(origin_point: Point, test_point: Point) -> float:
    ''' Returns the angle, in radians, of the test point
        from the origin point, sweeping like a clock, starting from
        the right and working counter-clockwise, just like
        the sine/cosine unit cicle.
    '''
    # shifts so that the origin point is at 0,0
    shifted_test_point = Point(test_point.x - origin_point.x,
                               test_point.y - origin_point.y)
    return math.atan2(shifted_test_point.y, shifted_test_point.x)


@type_checked()
def distance_to_origin(origin_point: Point, test_point: Point) -> float:
    ''' returns the distance of a point to the origin point. '''
    return dist2(origin_point, test_point) ** 0.5


@type_checked()
def intersects(seg1: Segment, seg2: Segment) -> bool:
    ''' Returns whether two segments intersect or not. '''
    return seg1.intersects(seg2)


@type_checked()
def point_visibility(segment_list: list, origin_point: Point) -> list:
    event_points = [segment.init for segment in segment_list]
    event_points += [segment.to for segment in segment_list]
    event_points.sort(key=lambda point: distance_to_origin(origin_point, point))
    event_points.sort(key=lambda point: angle_from_origin(origin_point, point))

def point_visibility_with_points(point_list: list) -> list:
    ''' Before passing to the original point_visibility problem,
        creates a problem using points drawn on the screen.
    '''
    if len(point_list) <= 2:
        return []

    if len(point_list) % 2 == 0:
        # Even number of points => odd number on edges.
        # adds last point again
        point_list.append(point_list[-1])

    origin_point = point_list[0]
    segment_list = [Segment(x1, x2) for x1, x2
                    in izip(islice(point_list, 1, None, 2), islice(point_list, 2, None, 2))]

    return point_visibility(segment_list, origin_point)

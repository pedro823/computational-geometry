from geocomp.common.segment import Segment
from geocomp.common.point import Point
from util.type_checker import type_checked
from geocomp.common.prim import dist2
import math


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
def point_visibility(segment_list: list, origin_point: Point):
    event_points = [segment.init for segment in segment_list]
    event_points += [segment.to for segment in segment_list]
    event_points.sort(key=lambda point: distance_to_origin(origin_point, point))
    event_points.sort(key=lambda point: angle_from_origin(origin_point, point))

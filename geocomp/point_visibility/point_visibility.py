import math
from dataclasses import dataclass
from itertools import islice
from enum import Enum

from geocomp.common.segment import Segment
from geocomp.common.vector import Vector
from geocomp.common.ray import Ray
from geocomp.common.point import Point
from geocomp.common.prim import dist2
from geocomp.common.binary_search_tree import BinarySearchTree
from geocomp.common.heap import Heap
from utils.type_checker import type_checked

class SegmentReference:
    def __init__(self, segment: Segment, point: Point):
        self.segment = segment
        self.point = point

    def __lt__(self, other):
        return other.segment.has_left(self.point)

class EventType(Enum):
    INSERT = 0
    DELETE = 1
    SWAP = 2

@dataclass
class Event:
    segment_ids: list
    point: Point
    type: EventType

class SweepLine:
    def __init__(self, origin_point: Point):
        self.bst = BinarySearchTree()
        self.ray = Ray(origin_point, Vector([1, 0]))

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
    angle = math.atan2(shifted_test_point.y, shifted_test_point.x)
    return angle if angle >= 0 else angle + 2*math.pi


@type_checked()
def distance_to_origin(origin_point: Point, test_point: Point) -> float:
    ''' returns the distance of a point to the origin point. '''
    return dist2(origin_point, test_point) ** 0.5


@type_checked()
def intersects(seg1: Segment, seg2: Segment) -> bool:
    ''' Returns whether two segments intersect or not. '''
    return seg1.intersects(seg2)

@type_checked()
def intersects_with_sweep_line(sweep_line: SweepLine, seg: Segment) -> bool:
    return sweep_line.ray.intersects(seg)

@type_checked()
def add_to_sweep_line(sweep_line: SweepLine, id: int, segment: Segment):
    ref = SegmentReference(segment, segment.init)
    sweep_line.bst.insert(id, ref)

@type_checked()
def point_visibility(segment_list: list, origin_point: Point) -> list:

    visible_segments = []

    # STEP 1: Sort event points
    event_points = [Event([i], segment.init, EventType.INSERT) for i, segment in enumerate(segment_list)]
    event_points += [Event([i], segment.to, EventType.DELETE) for i, segment in enumerate(segment_list)]
    event_points.sort(key=lambda e: distance_to_origin(origin_point, e.point))

    # Unfortunately, python has no currying
    event_heap = Heap.from_list(event_points,
                                key_function = lambda e: angle_from_origin(origin_point, e.point))

    # STEP 2: Initialize sweep line
    sweep_line = SweepLine(origin_point)

    # STEP 2.1: Check if there are no points inside the sweep line already. O(n)
    for i, segment in enumerate(segment_list):
        segment.hilight()
        if intersects_with_sweep_line(sweep_line, segment):
            add_to_sweep_line(sweep_line, i, segment)

    # print(sweep_line.bst)
    # while event_heap:
    #     el = event_heap.pop_element()
    #     print(el, angle_from_origin(origin_point, el.point))

    # STEP 3: Sweep line

    return []

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
    segment_list = []
    for x1, x2 in zip(islice(point_list, 1, None, 2), islice(point_list, 2, None, 2)):
        a1 = angle_from_origin(origin_point, x1)
        a2 = angle_from_origin(origin_point, x2)
        d1 = distance_to_origin(origin_point, x1)
        d2 = distance_to_origin(origin_point, x2)
        if (a1 > a2 and a1 - a2 <= math.pi) or \
           (a1 < a2 and a2 - a1 > math.pi) or \
           (a1 == a2 and d1 > d2):
            segment_list.append(Segment(x2, x1))
        else:
            segment_list.append(Segment(x1, x2))

    print(segment_list, origin_point)
    # for segment in segment_list:
    #     segment.plot()
    origin_point.hilight('yellow')

    return point_visibility(segment_list, origin_point)

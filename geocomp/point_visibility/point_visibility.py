import math

from itertools import islice
from enum import Enum

from geocomp.common import control
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

class Event:
    def __init__(self, segment_id: int, point: Point, type: EventType):
        self.segment_id = segment_id
        self.point = point
        self.type = type

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
    print(f"Adding {id}")
    ref = SegmentReference(segment, segment.init)
    sweep_line.bst.insert(id, ref)

@type_checked()
def remove_from_sweep_line(sweep_line: SweepLine, id: int):
    print(f"Removing {id}")
    sweep_line.bst.delete(id)

@type_checked()
def point_visibility(segment_list: list, origin_point: Point) -> list:
    origin_point.hilight('yellow')

    visible_segments = set()

    # HACK trocar a ordenação: pontos de inicio, quando empatam, vao crescente por distancia,
    # já os finais, vao decrescente por distancia
    @type_checked()
    def comparison_function(e1: Event, e2: Event) -> float:
        angle1, angle2 = angle_from_origin(origin_point, e1.point), angle_from_origin(origin_point, e2.point)
        if abs(angle1 - angle2) < 1e-7:
            multiplier = float(1 if e1.type == EventType.INSERT else -1)

            if e1.type != e2.type:
                return -multiplier

            return round(distance_to_origin(origin_point, e1.point)
                        - distance_to_origin(origin_point, e2.point), 7) * multiplier
        return angle1 - angle2

    @type_checked()
    def counterclockwise(p1: Point, p2: Point) -> float:
        angle1, angle2 = angle_from_origin(origin_point, p1), angle_from_origin(origin_point, p2)
        if abs(angle1 - angle2) < 1e-7:
            return -1.0
        if (angle1 > angle2 and angle1 - angle2 <= math.pi) \
            or (angle1 < angle2 and angle2 - angle1 > math.pi):
            return 1.0
        return -1.0

    # STEP 1: Sort event points
    event_points = []
    for idx, segment in enumerate(segment_list):
        if counterclockwise(segment.init, segment.to) > 0:
            segment.to, segment.init = segment.init, segment.to

        event_points.append(Event(idx, segment.init, EventType.INSERT))
        event_points.append(Event(idx, segment.to, EventType.DELETE))

        segment.hilight()
        control.sleep()
        segment.plot()

    event_heap = Heap.from_list(event_points,
                                cmp_function=comparison_function)

    # STEP 2: Initialize sweep line
    sweep_line = SweepLine(origin_point)

    sweep_line.ray.plot('pink')

    # STEP 2.1: Check if there are no points inside the sweep line already. O(n)
    for i, segment in enumerate(segment_list):
        segment.plot('blue')
        control.sleep()
        if intersects_with_sweep_line(sweep_line, segment) \
           and not sweep_line.ray.has_inside(segment.init):
            add_to_sweep_line(sweep_line, i, segment)
            segment.hide()
            segment.plot('green')
        else:
            segment.hide()
            segment.plot()

    print(sweep_line.bst)

    # STEP 3: Sweep line
    while event_heap:
        event = event_heap.pop_element()
        # 3.1: Take the minimum and put it into the set
        sweep_line.ray.hide()
        sweep_line.ray.direction = Vector.from_angle(angle_from_origin(origin_point, event.point))
        sweep_line.ray.plot('white')
        print(sweep_line.bst)

        minimum = sweep_line.bst.minimum()
        if minimum:
            visible_segments.add(minimum.key.segment)
            minimum.key.segment.hide()
            minimum.key.segment.plot('yellow')

        # 3.2: Insert/remove items from the BBST
        segment = segment_list[event.segment_id]

        if event.type == EventType.INSERT:
            add_to_sweep_line(sweep_line, event.segment_id, segment)
            if not (segment in visible_segments):
                segment.hide()
                segment.plot('green')
        elif event.type == EventType.DELETE:
            remove_from_sweep_line(sweep_line, event.segment_id)
            if not (segment in visible_segments):
                segment.hide()
                segment.plot()

        control.sleep()

    minimum = sweep_line.bst.minimum()
    if minimum:
        visible_segments.add(minimum.key.segment)
        minimum.key.segment.hide()
        minimum.key.segment.plot('yellow')

    sweep_line.ray.hide()
    print(visible_segments)
    return list(visible_segments)

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
                    in zip(islice(point_list, 1, None, 2), islice(point_list, 2, None, 2))]

    return point_visibility(segment_list, origin_point)

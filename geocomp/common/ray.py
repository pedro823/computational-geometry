from .point import Point
from .segment import Segment
from .vector import Vector

class Ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        self.direction = direction

    def intersects(self, other: Segment):
        max_distance = max(other.init.distance_to(self.origin), other.to.distance_to(self.origin))
        expanded_vector = self.direction * max_distance
        end_point = self.origin + expanded_vector
        segment = Segment(self.origin, end_point)
        return segment.intersects(other)
#!/usr/bin/env python

from . import control
from geocomp import config
from .prim import area2, left

class Segment:
    "Um segmento de reta"
    def __init__ (self, pto_from=None, pto_to=None):
        "Para criar, passe os dois pontos extremos"
        self.init = pto_from
        self.to = pto_to

    def __repr__ (self):
        "retorna uma string da forma [ ( x0 y0 );( x1 y1 ) ]"
        return '[ '+repr(self.init)+'; '+repr(self.to)+' ]'

    def hilight (self, color_line=config.COLOR_HI_SEGMENT,
            color_point=config.COLOR_HI_SEGMENT_POINT):
        "desenha o segmento de reta com destaque na tela"
        self.lid = self.init.lineto (self.to, color_line)
        self.pid0 = self.init.hilight (color_point)
        self.pid1 = self.to.hilight ('blue')
        return self.lid

    def plot (self, cor=config.COLOR_SEGMENT):
        "desenha o segmento de reta na tela"
        self.lid = self.init.lineto (self.to, cor)
        return self.lid

    def hide (self, id=None):
        "apaga o segmento de reta da tela"
        if id is None: id = self.lid
        control.plot_delete (id)

    def has_left(self, point):
        return left(self.init, self.to, point)

    def colinear_with(self, point):
        ''' returns if point is colinear with the segment. '''
        return area2(self.init, self.to, point) == 0

    def has_inside(self, point):
        ''' returns if point is inside the segment. '''
        if not self.colinear_with(point):
            return False
        if self.init.x != self.to.x:
            return self.init.x <= point.x <= self.to.x \
                   or self.to.x <= point.x <= self.init.x
        else:
            return self.init.y <= point.y <= self.to.y \
                   or self.to.y <= point.y <= self.init.y

    def intersects_inside(self, other_segment) -> bool:
        ''' returns whether the other segment intersects this segment
            (not counting border points) '''
        if self.colinear_with(other_segment.init)    \
           or self.colinear_with(other_segment.to)   \
           or other_segment.colinear_with(self.init) \
           or other_segment.colinear_with(self.to):
            return False

        return (left(self.init, self.to, other_segment.init)
                ^ left(self.init, self.to, other_segment.to))            \
               and (left(other_segment.init, other_segment.to, self.init)
                   ^ left(other_segment.init, other_segment.to, self.to))


    def intersects(self, other_segment) -> bool:
        if self.intersects_inside(other_segment):
            return True

        return self.has_inside(other_segment.init)    \
               or self.has_inside(other_segment.to)   \
               or other_segment.has_inside(self.init) \
               or other_segment.has_inside(self.to)

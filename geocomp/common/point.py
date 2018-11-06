#!/usr/bin/env python

from . import control
from .vector import Vector
from .prim import dist2
from geocomp import config

class Point:
    "Um ponto representado por suas coordenadas cartesianas"

    def __init__ (self, x, y, z=None):
        "Para criar um ponto, passe suas coordenadas."
        self.x = x
        self.y = y
        self.z = z
        self.lineto_id = {}

    def __repr__ (self):
        "Retorna uma string da forma '( x y )'"
        return '( ' + repr(self.x) + ' ' + repr(self.y) + ' )'

    def plot (self, color=config.COLOR_POINT):
        "Desenha o ponto na cor especificada"
        self.plot_id = control.plot_disc (self.x, self.y, color,
                            config.RADIUS)
        return self.plot_id

        ################### VICTOR MUDOU #######################

    def unplot(self, id = None):
        if id == None: id = self.plot_id
        control.plot_delete(id)



        ################## FIM ############################

    def hilight (self, color=config.COLOR_HI_POINT):
        "Desenha o ponto com 'destaque' (raio maior e cor diferente)"
        self.hi = control.plot_disc (self.x, self.y, color,
                        config.RADIUS_HILIGHT)
        return self.hi

    def unhilight (self, id = None):
        "Apaga o 'destaque' do ponto"
        if id == None: id = self.hi
        control.plot_delete (id)

    def __add__(self, other: Vector):
        if not isinstance(other, Vector):
            raise ValueError('Cannot add point and {}'.format(type(other)))
        if other.dimension != 2:
            raise ValueError('Cannot add 2-d point with non 2-d vector')
        return Point(self.x + other[0], self.y + other[1])

    def distance_to(self, other):
        return dist2(self, other) ** 0.5
    # def __sub__(self, other):
    #     if not isinstance(other, Point):
    #         raise ValueError('Cannot subtract point and ' + str(type(other)))
    #     return Point(self.x - other.x, self.y - other.y)

    def lineto (self, p, color=config.COLOR_LINE):
        "Desenha uma linha ate um ponto p na cor especificada"
        self.lineto_id[p] = control.plot_line (self.x, self.y, p.x, p.y, color)
        return self.lineto_id[p]

    def remove_lineto (self, p, id = None):
        "Apaga a linha ate o ponto p"
        if id == None: id = self.lineto_id[p]
        control.plot_delete (id)

    def is_inside(self, segment):
        ''' returns if point is inside the segment. '''
        return segment.has_inside(self)

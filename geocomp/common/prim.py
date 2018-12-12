#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

"""Primitivas geometricas usadas nos algoritmos

Use o modulo geocomp.common.guiprim para que essas primitivas sejam
desenhadas na tela  medida que elas so usadas. Tambm  possvel
desenh-las de um jeito especfico para um determinado algoritmo.
Veja geocomp.convexhull.quickhull para um exemplo.
"""

# Numero de vezes que a funcao area2 foi chamada
num_area2 = 0
# Numero de vezes que a funcao dist2 foi chamada
num_dist = 0

def area2 (a, b, c):
    "Retorna duas vezes a area do tringulo determinado por a, b, c"
    global num_area2
    num_area2 = num_area2 + 1
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def area_sign(a, b, c):
    area = area2(a, b, c)
    if area > 0:
        return 1
    if area < 0:
        return -1
    return 0

def left (a, b, c):
    "Verdadeiro se c est  esquerda do segmento orientado ab"
    return area2 (a, b, c) > 0

def left_on (a, b, c):
    "Verdadeiro se c est  esquerda ou sobre o segmento orientado ab"
    return area2 (a, b, c) >= 0

def collinear (a, b, c):
    "Verdadeiro se a, b, c sao colineares"
    return area2 (a, b, c) == 0

def right (a, b, c):
    "Verdadeiro se c est  direita do segmento orientado ab"
    return not (left_on (a, b, c))

def right_on (a, b, c):
    "Verdadeiro se c est  direita ou sobre o segmento orientado ab"
    return not (left (a, b, c))

def dist2 (a, b):
    "Retorna o quadrado da distancia entre os pontos a e b"
    global num_dist
    num_dist = num_dist + 1
    dy = b.y - a.y
    dx = b.x - a.x

    return dy*dy + dx*dx

def get_count ():
    "Retorna o numero total de operacoes primitivas realizadas"
    return num_area2 + num_dist

def reset_count ():
    "Zera os contadores de operacoes primitivas"
    global num_area2, num_dist
    num_area2 = 0
    num_dist = 0

def ccw_angle(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")
    dot   = u[0] * v[0] + u[1] * v[1]
    det   = u[0] * v[1] - u[1] * v[0]
    theta = math.atan2(det, dot)

    if theta >= 0:
        return theta
    return 2.0 * math.pi + theta

def cw_angle(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")
    dot   = u[0] * v[0] + u[1] * v[1]
    det   = u[0] * v[1] - u[1] * v[0]
    theta = math.atan2(det, dot)

    if theta < 0:
        return 2 * math.pi + theta
    return theta

def cross(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")

    if len(u) != len(v):
        raise ValueError("Vectors have different dimensions")

    dim = len(u)
    w = []
    for i in range(dim):
        w.append(0)
        for j in range(dim):
            if j != i:
                for k in range(dim):
                    if k != i:
                        if k > j:
                            w[i] += u[j] * v[k]
                        elif k < j:
                            w[i] -= u[j] * v[k]
    return w


def intersect(a, b, c, d):
    if a is None or \
       b is None or \
       c is None or \
       d is None:
        raise ValueError("Points must not be None")

    if intersect_prop(a, b, c, d):
        return True

    if on_segment(a, b, c) or \
       on_segment(a, b, d) or \
       on_segment(c, d, a) or \
       on_segment(c, d, b):
        return True
    return False


# TODO: Não trata o caso de todos os pontos colineares mas ainda com
# uma interseção própria.
#
# Ex: [(0,0), (2,0)] e [(1,0), (3,0)]
# retornaria que não intersecta propriamente, quando an verdade seus
# interiores se tocam
def intersect_prop(a, b, c, d):
    if a is None or \
       b is None or \
       c is None or \
       d is None:
        raise ValueError("Points must not be None")

    if collinear(a, b, c) or \
       collinear(a, b, d) or \
       collinear(a, c, d) or \
       collinear(b, c, d):
        return False

    return left(a, b, c) ^ left(a, b, d) and \
           left(c, d, a) ^ left(c, d, b)

def on_segment(a, b, c):
    if a is None or \
       b is None or \
       c is None:
        raise ValueError("Points must not be None")

    if not collinear(a, b, c):
        return False

    if a.x != b.x:
        return \
            a.x <= c.x <= b.x or \
            b.x <= c.x <= a.x
    return \
        a.y <= c.y <= b.y or \
        b.y <= c.y <= a.y



def dot(u, v):
    return u.x * v.x + u.y * v.y

def perp(a, b):
    if a is None or b is None:
        raise ValueError("Illegal argument of None type")
    return a.x * b.y - a.y * b.x

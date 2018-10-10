#!/usr/bin/env python
"""Modulo para leitura de um arquivo de dados"""

if __name__ != '__main__':
    from .point import Point
    from .segment import Segment
else:
    from point import Point
    from segment import Segment

def open_file (name):
    """Le o arquivo passado, e retorna o seu conteudo

    Atualmente, ele espera que o arquivo contenha uma lista de pontos,
    um ponto por linha, as duas coordenadas em cada linha. Exemplo:

    0 0
    0 1
    10 100

    """
    f = open (name, 'r')
    #t = range (5000)
    lista = []
    cont = 0

    for linha in f.readlines ():
        if linha[0] == '#': continue

        coord = linha.split()

        fields = len (coord)
        if fields == 0:
            continue
        if fields != 2:
            raise Exception('cada linha deve conter 2 coordenadas')

        x = float (coord[0])
        y = float (coord[1])
        lista.append (Point (x, y))

    f.close()

    return lista


def parse_point_visibility_file(filename: str) -> tuple:
    ''' Opens and parse a point visibility problem file.

        File must be in format:
        <ORIGIN POINT>
        <SEGMENT>
        <SEGMENT>
        ...
        <SEGMENT>
        where
        ORIGIN POINT = float float
        SEGMENT = float_x1 float_y1 float_x2 float_y2

        returns a tuple containing:
        (origin: Point, segments: list[Segment])
    '''
    with open(filename, 'r') as file:
        point_line = file.readline()
        try:
            origin_point = Point(*[float(coordinate) for coordinate in point_line.split()])
        except Exception as ex:
            raise Exception(f'Parse error at line 1: {ex}')
        segment_list = []
        for line_number, segment_line in enumerate(file):
            try:
                x1, y1, x2, y2 = segment_line.split()
                segment_list.append(
                    Segment(Point(x1, y1), Point(x2, y2))
                )
            except Exception as ex:
                raise Exception(f'Parse error at line {line_number + 2}: {ex}')
        return origin_point, segment_list


if __name__ == '__main__':
    import sys

    for filename in sys.argv[1:]:
        print(f'filename={filename}')
        origin_point, segment_list = parse_point_visibility_file(filename)
        print(f'origin_point={origin_point}\nsegment_list={segment_list}')

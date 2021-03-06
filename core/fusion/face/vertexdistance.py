import itertools

from .. import util


def vertex_distance(first, second):
    return [util.distance(primary_vertex.geometry, secondary_vertex.geometry)
            for primary_vertex, secondary_vertex in itertools.product(first, second)]


def point_distance(first, second):
    return [util.distance(primary_point, secondary_point)
            for primary_point, secondary_point in itertools.product(first, second)]

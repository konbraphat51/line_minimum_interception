from __future__ import annotations
from typing import Iterable
from .GeometryExpressions import Vector, Line

def calculate_minimum_movements(lines: Iterable[Line]) -> list[Vector]:
    """
    Calculate minimum movements to have all lines intersect 
    
    Create a matrix of equations under intersection condition,
    and minimize the sum of squares of the movement vector.
    
    :param Iterable[Line] lines: lines to let intersect
    :return: minimum movements vector of each lines.
    Each vector is perpendicular to the direction vector of the line.
    The order is same as the give iteration.
    :rtype: list[Vector]
    """
    
    #get normal vectors of each lines
    normal_vectors = [_find_normal_vectors(line.direction) for line in lines]
    
    
    
def _find_normal_vectors(vector: Vector) -> tuple[Vector]:
    """
    Find a pair of normal vectors of the given vector.
    
    :param Vector vector: vector to find normal vectors
    :return: pair of normal vectors.
    The pair is perpendicular to each other, and normalized.
    :rtype: tuple[Vector]
    """
    
    # first of the pair
    # make it perpendicular to the given vector and a dummy vector
    # dummy vector: anything Okey, but not parallel to the given vector
    if vector.x != 0:
        dummy = Vector(0, 1, 0)
    else:
        dummy = Vector(1, 0, 0)
    first = Vector.calculate_cross(vector, dummy).calculate_normalized()
    
    # second of the pair
    # this must be perpendicular to the first vector and the given vector
    second = Vector.calculate_cross(first, vector).calculate_normalized()
    
    return (first, second)
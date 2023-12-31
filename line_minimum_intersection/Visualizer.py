"""
Visualize results
"""

from __future__ import annotations
from typing import Iterable
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from .GeometryExpressions import Vector, Line


def visualize_intersection(
    lines: Iterable[Line],
    intersection_point: Vector,
    movement_vectors: Iterable[Vector],
    line_length: float = 100.0,
) -> None:
    """
    Visualize optimized results

    :param Iterable[Line] lines: lines to let intersect
    :param Vector intersection_point: intersection point
    :param Iterable[Vector] movement_vectors: movement vectors
        should be same order/length as lines
    :param float line_length: length of line to draw
    :rtype: None
    """

    line_n = len(lines)

    # canvas
    figure = plt.figure()
    axes = figure.add_subplot(projection="3d")

    # draw lines
    for line_id in range(line_n):
        _draw_line(
            axes,
            intersection_point,
            lines[line_id].direction,
            movement_vectors[line_id],
            line_length,
        )

    # draw intersection point
    axes.scatter(
        [intersection_point.x],
        [intersection_point.y],
        [intersection_point.z],
        color="red",
    )

    # draw movement vectors
    for line_id in range(line_n):
        _draw_movement_vector(
            axes, intersection_point, movement_vectors[line_id], color="green"
        )

    # label
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")

    plt.show()


def _draw_line(
    axes: Axes3D,
    intersection_position: Vector,
    direction: Vector,
    movement_vector: Vector,
    line_length: float,
    color: str = "blue",
) -> None:
    """
    Draw a line

    :param Axes3D axes: axes to draw
    :param Vector intersection_position: intersection position
    :param Vector direction: direction of the line
    :param Vector movement_vector: movement vector
    :param float line_length: length of line to draw
    :param str color: color of line
    :rtype: None
    """

    # draw from here
    start_position = intersection_position - movement_vector

    # make on-line points
    x = []
    y = []
    z = []
    extension = 0.0
    while extension <= line_length:
        # plus direction
        x.append(start_position.x + direction.x * extension)
        y.append(start_position.y + direction.y * extension)
        z.append(start_position.z + direction.z * extension)

        # minus direction
        x.append(start_position.x - direction.x * extension)
        y.append(start_position.y - direction.y * extension)
        z.append(start_position.z - direction.z * extension)

        extension += line_length / 100.0

    # draw 1 line
    axes.plot(x, y, z, color=color)


def _draw_movement_vector(
    axes: Axes3D,
    intersection_position: Vector,
    movement_vector: Vector,
    color: str = "green",
) -> None:
    """
    Draw a movement vector

    :param Axes3D axes: axes to draw
    :param Vector intersection_position: intersection position
    :param Vector movement_vector: movement vector
    :param str color: color of line
    :rtype: None
    """

    axes.quiver(
        intersection_position.x,
        intersection_position.y,
        intersection_position.z,
        movement_vector.x,
        movement_vector.y,
        movement_vector.z,
        pivot="tip",
        color=color,
    )

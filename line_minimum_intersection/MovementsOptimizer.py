from __future__ import annotations
from typing import Iterable
from scipy.optimize import minimize
from .GeometryExpressions import Vector, Line


def calculate_minimum_movements(
    lines: Iterable[Line],
) -> dict[str, Vector | list[Vector]]:
    """
    Calculate minimum movements to have all lines intersect

    Create a matrix of equations under intersection condition,
    and minimize the sum of squares of the movement vector.

    :param Iterable[Line] lines: lines to let intersect
    :return: {
        "intersection_point": one intersection point of all lines(Vector),
        "movement_vectors": minimum movements vector of each lines.(list[Vector])
            Each vector is perpendicular to the direction vector of the line.
    }
    The order is same as the give iteration.
    :rtype: dict[str, Vector|list[Vector]]
    """

    # get normal vectors of each lines
    normal_vectors = [_find_normal_vectors(line.direction) for line in lines]

    # set conditions
    conditions = []
    for cnt in range(len(lines) - 1):
        # for each pair of lines: former and the next
        conditions.extend(
            _compute_conditions(
                cnt,
                lines[cnt],
                normal_vectors[cnt],
                cnt + 1,
                lines[cnt + 1],
                normal_vectors[cnt + 1],
            )
        )

    # optimize
    parameters = _optimize(len(lines), conditions)

    # convert to Vector
    movement_vectors = []
    for line_id in range(len(lines)):
        movement_vector = (
            normal_vectors[line_id][0] * parameters[line_id][1][0]
            + normal_vectors[line_id][1] * parameters[line_id][1][1]
        )
        movement_vectors.append(movement_vector)

    # get intersection point
    intersection_point = (
        lines[0].start_position
        + lines[0].direction * parameters[0][0]
        + movement_vectors[0]
    )

    # make result
    result = {
        "intersection_point": intersection_point,
        "movement_vectors": movement_vectors,
    }

    return result


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


def _compute_conditions(
    id0: int,
    line0: Line,
    normals0: tuple[Vector, Vector],
    id1: int,
    line1: Line,
    normals1: tuple[Vector, Vector],
) -> list[dict]:
    """
    Set intersection conditions between two lines.


    the intersection point on the line is expressed using vector as:
        start + direction * t + normal0 * movement_0 + normal1 * movement_1
            ...where t, M0, M1 are optimized parameters that been set for each lines
    This will set 3 condition for xyz components.
    the parameter_name will use _get_extension_param_name() and _get_movement_param_name().

    :param int id0: id of the first line. This is used for naming parameters
    :param Line line0: first line to intersect
    :param tuple[Vector, Vector] normals0: normal vectors of the first line
    :param int id1: id of the second line. This is used for naming parameters
    :param Line line1: second line to intersect
    :param tuple[Vector, Vector] normals1: normal vectors of the second line
    :return: 3 conditions that returns the value of the condition of xyz,
    the parameter of this function using the naming functions
    :rtype: list[dict]
    """

    conditions = []

    # per component
    for component_id in range(3):
        conditions.append(
            _compute_condition(
                component_id, id0, line0, normals0, id1, line1, normals1
            )
        )

    return conditions


def _compute_condition(
    component_id: int,
    id0: int,
    line0: Line,
    normals0: tuple[Vector, Vector],
    id1: int,
    line1: Line,
    normals1: tuple[Vector, Vector],
) -> dict:
    """
    Set intersection conditions between two lines for single component.

    See docstring of _set_conditions() for details.

    :param int component_id: id of the component. x: 0, y: 1, z: 2
    :param int id0: id of the first line. This is used for naming parameters
    :param Line line0: first line to intersect
    :param tuple[Vector, Vector] normals0: normal vectors of the first line
    :param int id1: id of the second line. This is used for naming parameters
    :param Line line1: second line to intersect
    :param tuple[Vector, Vector] normals1: normal vectors of the second line
    :return: condition that returns the value of the condition,
    the parameter of this function using the naming functions
    :rtype: callable[dict, float]
    """

    return {
        "type": "eq",
        "fun": lambda params: (
            (
                line0.start_position[component_id]
                + line0.direction[component_id]
                * params[_get_extension_param_position(id0)]
                + normals0[0][component_id]
                * params[_get_movement_param_position(id0, 0)]
                + normals0[1][component_id]
                * params[_get_movement_param_position(id0, 1)]
            )
            - (
                line1.start_position[component_id]
                + line1.direction[component_id]
                * params[_get_extension_param_position(id1)]
                + normals1[0][component_id]
                * params[_get_movement_param_position(id1, 0)]
                + normals1[1][component_id]
                * params[_get_movement_param_position(id1, 1)]
            )
        ),
    }


def _compute_score(params: list[float]):
    """
    Compute the score of the parameters.

    This is sum of squares of the movement vectors.

    :param list[float] params: parameters
    :return: score
    :rtype: float
    """

    # square of the movement vector length
    score = 0
    for cnt in range(len(params)):
        # HACK: this is not adaptive
        index0 = _get_movement_param_position(cnt, 0)
        if index0 >= len(params):
            break
        score += params[index0] ** 2

        index1 = _get_movement_param_position(cnt, 1)
        if index1 >= len(params):
            break
        score += params[index1] ** 2

    return score


def _optimize(
    line_n: int, conditions: list[float]
) -> list[float, tuple[float, float]]:
    """
    Optimize the parameters.

    :param int line_n: number of lines
    :param list[float] conditions: parameters to optimize
    :return: optimized (extension, (movement0, movement1)) of each lines.
    Order responds to the line id.
    :rtype: list[float, tuple[float, float]]
    """

    # initialize parameters
    parameters = [0] * (
        max(
            _get_extension_param_position(line_n - 1),
            _get_movement_param_position(line_n - 1, 1),
        )
        + 1
    )
    for line_id in range(line_n):
        parameters[_get_extension_param_position(line_id)] = 0
        for normal_id in range(2):
            parameters[_get_movement_param_position(line_id, normal_id)] = 0

    # optimize
    result = minimize(_compute_score, parameters, constraints=conditions)

    # clean results
    parameters = []
    for line_id in range(line_n):
        # (movement0, movement1) of each lines
        movements = (
            result.x[_get_movement_param_position(line_id, 0)],
            result.x[_get_movement_param_position(line_id, 1)],
        )

        # extension of each lines
        extension = result.x[_get_extension_param_position(line_id)]

        parameters.append((extension, movements))

    return parameters


def _get_extension_param_position(id: int) -> int:
    """
    Get the position of the parameter that represents the extension of the direction vector.

    Posiotion in the parameters list.

    :param int id: id of the line
    :return: position of the parameter
    :rtype: int
    """
    return 3 * id


def _get_movement_param_position(id: int, normal_id: int) -> int:
    """
    Get the position of the parameter that represents the movement.

    Posiotion in the parameters list.

    :param int id: id of the line
    :param int normal_id: id of the normal vector
    :return: position of the parameter
    :rtype: int
    """
    return 3 * id + 1 + normal_id

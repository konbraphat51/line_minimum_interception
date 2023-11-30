#unit-test calculate_minimum_movements()

from line_minimum_intersection import Vector, Line, calculate_minimum_movements

lines = []
lines.append(Line(Vector(0, 0, 0), Vector(1, 0, 0)))
lines.append(Line(Vector(1, 1, 1), Vector(0, 0, -1)))

movement_vectors = calculate_minimum_movements(lines)

for vector in movement_vectors:
    print(vector)
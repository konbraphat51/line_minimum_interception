# unit-test calculate_minimum_movements()

from line_minimum_intersection import Vector, Line, calculate_minimum_movements

lines = []
lines.append(Line(Vector(0, 0, 0), Vector(1, 0, 0)))
lines.append(Line(Vector(1, 1, 1), Vector(0, 0, -1)))

movement_vectors = calculate_minimum_movements(lines)

print("intersection point:")
print(movement_vectors["intersection_point"])

print("movement vectors:")
for vector in movement_vectors["movement_vectors"]:
    print(vector)

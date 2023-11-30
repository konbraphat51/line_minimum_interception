"""
Module for prepare classes for geometry expressions
"""

from __future__ import annotations

class Vector:
    """
    3D Vector
    """
    
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Set vector components
        
        :param float x: x component
        :param float y: y component
        :param float z: z component
        :rtype: None
        """
        
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, sc: float) -> Vector:
        return Vector(self.x * sc, self.y * sc, self.z * sc)
    
    def __rmul__(self, sc: float) -> Vector:
        return self * sc
    
    def __div__(self, sc: float) -> Vector:
        return Vector(self.x / sc, self.y / sc, self.z / sc)
    
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector index out of range")
 
    def calculate_length(self) -> float:
        """
        Calculate vector length
        
        :return: vector length
        :rtype: float
        """
        
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def calculate_normalized(self) -> Vector:
        """
        Return normalized vector
        
        Doesn't modify the original instance.
        
        :return: normalized vector
        :rtype: Vector
        """
        
        return self / self.calculate_length()
    
    def calculate_cross(vector0: Vector, vector1: Vector) -> Vector:
        """
        Calculate cross product of two vectors
        
        This is static function
        
        :param Vector vector0: vector0
        :param Vector vector1: vector1
        :return: cross product of two vectors
        :rtype: Vector
        """
            
        return Vector(
            vector0.y * vector1.z - vector0.z * vector1.y,
            vector0.z * vector1.x - vector0.x * vector1.z,
            vector0.x * vector1.y - vector0.y * vector1.x
        )
    
class Line:
    """
    Line in 3D space
    """
    
    def __init__(self, start_position: Vector, direction: Vector) -> None:
        """
        Set attributes
        
        :param Vector start_position: start position
        :param Vector direction: direction
        :rtype: None
        """
        
        self.start_position = start_position
        self.direction = direction.calculate_normalized()
        
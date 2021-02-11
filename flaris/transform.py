"""Implements classes related to Euclidean space."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .component import Component

__all__ = ["Direction", "Transform", "Vector"]


@dataclass(frozen=True)
class Vector:
    """An object representing a three-dimensional vector."""

    x: float
    y: float
    z: float

    def __add__(self, vector: Vector) -> Vector:
        """Add a vector to this vector.

        Args:
            vector: The vector to add.

        Returns:
            A new vector representing the result of adding a vector to
                this vector.
        """
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def __sub__(self, vector: Vector) -> Vector:
        """Subtract a vector from this vector.

        Args:
            vector: The vector to subtract with.

        Returns:
            A new vector representing the result of subtracting a vector from
                this vector.
        """
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def __mul__(self, obj: Union[Vector, float]) -> Vector:
        """Multiply a vector with a scalar or vector.

        Vector multiplication is performed component-wise.

        Args:
            object: The scalar or vector to multiply this vector with.

        Returns:
            A new vector representing the result of multiplying this vector with
                a scalar or vector.
        """
        if isinstance(obj, (float, int)):
            return Vector(obj * self.x, obj * self.y, obj * self.z)
        if isinstance(obj, Vector):
            return Vector(obj.x * self.x, obj.y * self.y, obj.z * self.z)
        raise NotImplementedError

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> Vector:
        """Divide a vector by a scalar.

        Args:
            scalar: The scalar to divide this vector by.

        Returns:
            A new vector representing the result of dividing this vector by a
                scalar.
        """
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other: object) -> bool:
        """Return true if other is an equivalent Vector.

        Args:
            other: The object to compare with.

        Returns:
            Returns true if and only if the other object is a Vector, and
                all three vector components are equal.
        """
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __matmul__(self, other: Vector) -> float:
        """Compute the dot product of this vector with another vector.

        Args:
            other: The vector to compute the dot product with.

        Returns:
            A float representing the dot product of this vector with another
                vector.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __mod__(self, other: int) -> Vector:
        """Apply the modulo operator to each component of the vector.

        Args:
            other: The modulus of the operation.

        Returns:
            A new vector representing the result of the applying the modulo
                operator to each component of the vector.

        Raises:
            ValueError: if other is not an int.
        """
        if not isinstance(other, int):
            raise ValueError("Expected int but got %s." % type(other))

        return Vector(self.x % other, self.y % other, self.z % other)

    def __iter__(self):
        """Return an iterator over this vector."""
        return iter([self.x, self.y, self.z])

    def __repr__(self) -> str:
        """Represent the Vector as a string."""
        return "Vector(%s, %s, %s)" % (self.x, self.y, self.z)


class Direction:  # pylint: disable=too-few-public-methods
    """Defines commonly used unit vectors."""
    RIGHT = Vector(1, 0, 0)
    LEFT = Vector(-1, 0, 0)
    UP = Vector(0, 1, 0)
    DOWN = Vector(0, -1, 0)
    FORWARD = Vector(0, 0, 1)
    BACKWARD = Vector(0, 0, -1)


class Transform(Component):  # pylint: disable=unused-argument
    """An object representing a position, rotation, and scale.

    Attributes:
        position: A Vector representing the world position of the transform.
        rotation: A Vector representing the euler angles of the transform.
        scale: A Vector the scale of the transform.
    """

    def __init__(self,
                 position: Vector = Vector(0, 0, 0),
                 rotation: Vector = Vector(0, 0, 0),
                 scale: Vector = Vector(1, 1, 1)):
        """Initialize the position, rotation, and scale attributes.

        Args:
            position: The world position of the transform (default:
                Vector(0, 0, 0)).
            rotation: The euler angles of the transform (default:
                Vector(0, 0, 0)).
            scale: The scale of the transform (default: Vector(1, 1, 1)).
        """
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def __eq__(self, other: object) -> bool:
        """Return true if other is an equivalent Transform.

        Args:
            other: The object to compare with.

        Returns:
            Returns true if and only if the other object is a Transform, and
            the values of the position, rotation, and scale attributes are
            equal.
        """
        if not isinstance(other, Transform):
            return False
        return (self.position == other.position and
                self.rotation == other.rotation and self.scale == other.scale)

    def __copy__(self) -> Transform:
        """Return a copy of this transform."""
        return Transform(self.position, self.rotation, self.scale)

    def translate(self, movement: Vector) -> None:
        """Move the transform in a direction.

        Args:
            movement: A vector representing the direction and magnitude of a
                movement.
        """
        self.position += movement

    def rotate(self, angles: Vector) -> None:
        """Rotate the transform around three axes.

        Args:
            angles: A vector representing the yaw, pitch, and roll.
        """
        # TODO (@bveeramani): Use quaternions instead of euler angles.
        self.rotation += angles
        self.rotation %= 360

    def __repr__(self):
        """Represent the Transform as a string."""
        string = "Transform("
        if self.position != Vector(0, 0, 0):
            string += f"position={self.position}, "
        if self.rotation != Vector(0, 0, 0):
            string += f"rotation={self.rotation}, "
        if self.scale != Vector(0, 0, 0):
            string += f"scale={self.scale}, "

        # Remove trailing ', '
        string = string[:-len(", ")]
        string += ")"
        return string

"""Unit tests for flaris.transform."""
import copy
import pytest

from flaris import Vector, Transform


class TestVector:
    """Unit tests for flaris.transform.Vector."""

    @pytest.mark.parametrize("vector, other_vector, expected_vector", [
        (Vector(1, 6, 3), Vector(-7, -4, 2), Vector(-6, 2, 5)),
        (Vector(3, 9, 4), Vector(0, 0, 0), Vector(3, 9, 4)),
        (Vector(1, 0, 2), Vector(0, 3, 0), Vector(1, 3, 2)),
    ])
    def testAdd(self, vector, other_vector, expected_vector):
        assert vector + other_vector == expected_vector

    @pytest.mark.parametrize("vector, other_vector, expected_vector", [
        (Vector(1, 6, 3), Vector(-7, -4, 2), Vector(8, 10, 1)),
        (Vector(3, 9, 4), Vector(0, 0, 0), Vector(3, 9, 4)),
        (Vector(1, 0, 2), Vector(0, 3, 0), Vector(1, -3, 2)),
    ])
    def testSub(self, vector, other_vector, expected_vector):
        assert vector - other_vector == expected_vector

    @pytest.mark.parametrize("scalar, vector, expected_vector", [
        (0, Vector(1, 1, 1), Vector(0, 0, 0)),
        (1, Vector(1, 1, 1), Vector(1, 1, 1)),
        (-1, Vector(1, 1, 1), Vector(-1, -1, -1)),
    ])
    def testMul_Scalar(self, scalar, vector, expected_vector):
        assert scalar * vector == expected_vector

    @pytest.mark.parametrize("vector, other_vector, expected_vector", [
        (Vector(1, -2, -3), Vector(3, 7, -4), Vector(3, -14, 12)),
        (Vector(1, 0, 2), Vector(0, 0, 0), Vector(0, 0, 0)),
    ])
    def testMul_Vector(self, vector, other_vector, expected_vector):
        assert vector * other_vector == expected_vector

    @pytest.mark.parametrize("vector, other_vector, expected_bool", [
        (Vector(3, 9, 4), Vector(3, 9, 4), True),
        (Vector(1, 0, 2), Vector(7, 3, 2), False),
    ])
    def testEq(self, vector, other_vector, expected_bool):
        assert (vector == other_vector) == expected_bool

    @pytest.mark.parametrize("vector, other_object", [
        (Vector(3, 9, 4), "3, 9, 4"),
        (Vector(4, 2, 6), [4, 2, 6]),
    ])
    def testEq_DifferentTypeObject(self, vector, other_object):
        assert vector != other_object

    @pytest.mark.parametrize("vector, number, expected_vector", [
        (Vector(5, 4, 7), 2, Vector(1, 0, 1)),
        (Vector(90, -45, 30), 360, Vector(90, 315, 30)),
    ])
    def testMod(self, vector, number, expected_vector):
        assert (vector % number) == expected_vector

    @pytest.mark.parametrize("vector, expected_string", [
        (Vector(3, 9, 4), "Vector(3, 9, 4)"),
        (Vector(1, 0, 2), "Vector(1, 0, 2)"),
    ])
    def testRepr(self, vector, expected_string):
        assert repr(vector) == expected_string


class TestTransform:
    """Unit tests for flaris.transform.Transform."""

    @pytest.mark.parametrize("initial_position, movement, expected_position", [
        (Vector(1, 6, 3), Vector(-7, -4, 2), Vector(-6, 2, 5)),
        (Vector(3, 9, 4), Vector(0, 0, 0), Vector(3, 9, 4)),
        (Vector(1, 0, 2), Vector(0, 3, 0), Vector(1, 3, 2)),
    ])
    def testTranslate(self, initial_position, movement, expected_position):
        transform = Transform(position=initial_position)
        transform.translate(movement)
        assert transform.position == expected_position

    @pytest.mark.parametrize(
        "transform, other_transform, expected_bool",
        [(Transform(), Transform(), True),
         (Transform(), Transform(position=Vector(1, 0, 0)), False),
         (Transform(), Vector(0, 0, 0), False)])
    def testEq(self, transform, other_transform, expected_bool):
        assert (transform == other_transform) == expected_bool

    def testCopy(self):
        transform = Transform(position=Vector(1, 0, 0),
                              rotation=Vector(30, 45, 60),
                              scale=Vector(2, 2, 2))
        expected_transform = Transform(position=Vector(1, 0, 0),
                                       rotation=Vector(30, 45, 60),
                                       scale=Vector(2, 2, 2))

        transform_copy = copy.copy(transform)

        assert transform_copy == expected_transform
        assert transform_copy is not expected_transform

    @pytest.mark.parametrize("initial_rotation, angles, expected_rotation", [
        (Vector(0, 0, 0), Vector(30, -45, 60), Vector(30, 315, 60)),
    ])
    def testRotate(self, initial_rotation, angles, expected_rotation):
        transform = Transform(rotation=initial_rotation)
        transform.rotate(angles)
        assert transform.rotation == expected_rotation

    @pytest.mark.parametrize("transform, expected_string", [
        (Transform(), "Transform()"),
        (Transform(position=Vector(1, 0, 0)),
         "Transform(position=Vector(1, 0, 0))"),
        (Transform(position=Vector(1, 0, 0),
                   rotation=Vector(30, 45, 60),
                   scale=Vector(2, 2, 2)),
         "Transform(position=Vector(1, 0, 0), rotation=Vector(30, 45, 60), scale=Vector(2, 2, 2))")  # noqa: E501
    ])
    def testRepr(self, transform, expected_string):
        assert repr(transform) == expected_string

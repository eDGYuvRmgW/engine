"""Unit tests for engine.physics.colliders."""
import pytest

from engine import Vector, Transform, BoxCollider


class TestBoxCollider:
    """Unit tests for engine.physics.colliders.BoxCollider."""

    # TODO(@bveeramani): Add tests that vary orientation, scale, and size.
    @pytest.mark.parametrize("collider, other, expected", [
        (BoxCollider(transform=Transform(position=Vector(0, 0, 0))),
         BoxCollider(transform=Transform(position=Vector(0, 0, 0))), True),
        (BoxCollider(transform=Transform(position=Vector(1, 0, 0))),
         BoxCollider(transform=Transform(position=Vector(0, 0, 0))), True),
        (BoxCollider(transform=Transform(position=Vector(2, 0, 0))),
         BoxCollider(transform=Transform(position=Vector(0, 0, 0))), False),
    ])
    def testIntersects(self, collider, other, expected: bool):
        assert collider.intersects(other) == expected

    def testRepr(self):
        transform, size = Transform(), Vector(0, 0, 0)
        collider = BoxCollider(transform=transform, size=size)

        actual = repr(collider)
        expected = "BoxCollider(transform=%s, size=%s)" % (transform, size)

        assert actual == expected

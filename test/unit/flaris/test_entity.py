"""Unit tests for flaris.entity."""
import pytest

from flaris import Entity, Transform


class TestEntity:
    """Unit tests for flaris.entity.Entity."""

    def testAttachClassComponent(self):

        class A(Entity):
            a = 

"""Unit tests for the `flaris.component` module."""
from flaris.component import Component
from flaris.entity import Entity


class StubComponent(Component):
    """A simple component used for testing."""


class StubEntity(Entity):
    """A simple entity used for testing."""

    def __init__(self, component: Component):
        super().__init__()
        self.component = component


class TestComponent:
    """Unit tests for `Component` class."""

    def testEntity(self):
        component = StubComponent()
        assert not component.entity
        entity = StubEntity(component)
        assert component.entity is entity

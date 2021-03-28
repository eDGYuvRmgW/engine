"""Unit tests for the `flaris.component` module."""
from flaris.component import Component
from flaris.entity import Entity


class StubComponent(Component):
    """A simple component used for testing."""
    pass


class StubEntity(Entity):
    """A simple entity used for testing."""

    def __init__(self, component: Component):
        super().__init__()
        self.component = component


class TestComponent:
    """Unit tests for `Component` class."""

    def testSimple(self):
        component = StubComponent()
        entity = StubEntity(component)
        assert entity[StubComponent] is component
        assert component.entity is entity

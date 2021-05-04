"""Implements the `Entity` class."""
from typing import Any, Iterable

from .component import Component, ComponentError

__all__ = ["Entity"]


class Entity:
    """A collection of components representing a particular object.

    You should use this as the base class for all game objects.
    """

    def __init__(self):
        """Initialize the entity."""
        self._components = {}

    def __getitem__(self, key: type):
        """Return the component with the given type.

        Args:
            key: A component type.

        Returns:
            The value of the component with the given type, if one has been
            attached.

        Raises:
            ComponentError: If the entity does not have a component of the given
                type.
        """
        component_type = key
        if component_type not in self._components:
            raise ComponentError(f"Entity {self} does not have a "
                                 f"{component_type} component.")

        return self._components[key]

    def __contains__(self, key: type):
        """Return true if the entity contains a component of the given type."""
        try:
            components = self.__dict__["_components"]
        except KeyError as error:
            raise AttributeError("Cannot check components before "
                                 "Entity.__init__() call.") from error
        return key in components

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an instance attribute.

        If value is an instance of `Component`, then the value is inserted into
        the entity's collection of components.

        Args:
            name: The name of the attribute to set.
            value: The value of the attribute to set.

        Raises:
            ComponentError: If the given value is an instance of `Component`
                and the entity already contains a component of the same type.
            AttributeError: If the given value is an instance of `Component`
                and the `Entity` constructor has not been called.
        """
        object.__setattr__(self, name, value)

        if not isinstance(value, Component):
            return
        component = value

        try:
            components = self.__dict__["_components"]
        except KeyError as error:
            raise AttributeError("Cannot attach components before "
                                 "Entity.__init__() call.") from error

        if type(component) in components:
            raise ComponentError(f"Cannot attach {type(component)} to {self} "
                                 f"because a component of that type is already "
                                 f"attached.")

        components[type(component)] = component
        component.entity = self

    def __delattr__(self, name: str) -> None:
        """Delete an instance attribute.

        If the value of the attribute with the given name is an instance of
        `Component`, then the value is also removed from the entity's collection
        of components.

        Raises:
            AttributeError: If the value of the attribute with the given name is
                an instance of `Component` and the `Entity` constructor has not
                been called.
        """
        value = self.__dict__[name]
        object.__delattr__(self, name)  # pytype: disable=attribute-error

        if isinstance(value, Component):
            return
        component = value

        try:
            components = self.__dict__["_components"]
        except AttributeError as error:
            raise AttributeError("Cannot attach components before"
                                 "Entity.__init__() call.") from error

        del components[type(component)]
        component.entity = None

    def update(self, delta: float):
        """Update this entity.

        You should override this method to implement behavior.
        """

    @property
    def components(self) -> Iterable[Component]:
        """Return an iterator over the components attached to this entity."""
        return iter(self._components.values())

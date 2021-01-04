"""Defines the `System` base class and implements various systems."""
from __future__ import annotations

import abc
from typing import Iterable, List, TYPE_CHECKING

from .component import ComponentError

if TYPE_CHECKING:
    from .entity import Entity

__all__ = ["System", "PipelinedSystem", "UpdateSystem"]


class System:
    """A collection of routines that describes an action taken every frame.

    Attributes:
        REQUIRED_COMPONENTS: A list of types describing the components that this
            system acts on.
    """

    REQUIRED_COMPONENTS = ()

    def __init__(self):
        """Initialize the system."""
        self._entities = set()

    def __contains__(self, entity: Entity) -> bool:
        """Return true if the entity is part of the system."""
        return entity in self._entities

    def start(self) -> None:
        """Set up the system.

        This method is called after the window context is created but before the
        main loop begins.
        """
        pass

    def exit(self) -> None:
        """Clean up the system.

        This method is called after the main loop ends.
        """
        pass

    def add(self, entity: Entity) -> None:
        """Add an entity to the system.

        After adding an entity to the system, the system can act on the entity
        every frame.

        Args:
            entity: The entity to add.

        Raises:
            ComponentError: If the entity does not possess the components
                requried to be part of this system.
        """
        if not self.accepts(entity):
            raise ComponentError
        self._entities.add(entity)

    def remove(self, entity: Entity) -> None:
        """Remove an entity from the system."""
        self._entities.remove(entity)

    @abc.abstractmethod
    def step(self, delta: float) -> None:
        """Perform an action on all entities in the system.

        Args:
            delta: The amount of time required to complete the previous frame.
        """
        pass

    def accepts(self, entity: Entity) -> bool:
        """Return true if the entity is valid for this system.

        Returns: True, if and only if the entity possesses all of the components
            required by this system, as defined by `System.REQUIRED_COMPONENTS`.
        """
        for component_type in self.REQUIRED_COMPONENTS:
            if component_type not in entity:
                return False
        return True

    @property
    def entities(self) -> Iterable[Entity]:
        """Return an iterator over the entities in this system."""
        return iter(self._entities)


class PipelinedSystem:
    """A collection of systems run sequentially."""

    def __init__(self, systems: List[System]):
        """Initialize the systems.

        Args:
            systems: An ordered collection of systems to pipeline.
        """
        self.systems = systems

    def __contains__(self, entity: Entity) -> bool:
        """Return true if the entity is part of the system."""
        return any(entity in system for system in self.systems)

    def start(self) -> None:
        """Set up each system in the pipeline."""
        for system in self.systems:
            system.start()

    def exit(self) -> None:
        """Exit each system in the pipeline."""
        for system in self.systems:
            system.exit()

    def add(self, entity: Entity) -> None:
        """Add an entity to the system.

        After adding an entity to the system, the system can act on the entity
        every frame.

        Args:
            entity: The entity to add.

        Raises:
            ComponentError: If the entity does not possess the components
                requried to be part of this system.
        """
        for system in self.systems:
            try:
                system.add(entity)
            except ComponentError:
                pass

    def remove(self, entity: Entity) -> None:
        """Remove an entity from the system."""
        for system in self.systems:
            if entity in system:
                system.remove(entity)

    def step(self, delta: float) -> None:
        """Advance each system in the pipeline by one step.

        Args:
            delta: The amount of time required to complete the previous frame.
        """
        for system in self.systems:
            system.step(delta)


class UpdateSystem(System):
    """A system that calls the update method of every entity."""

    def step(self, delta: float) -> None:
        """Call the update method of each entity in the system.

        Args:
            delta: The amount of time required to complete the previous frame.
        """
        for entity in self.entities:
            entity.update(delta)

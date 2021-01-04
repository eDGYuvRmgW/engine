from engine.system import PipelinedSystem

from .key import KeyboardHandlingSystem

__all__ = ["InputSystem"]


class InputSystem(PipelinedSystem):

    def __init__(self):
        super().__init__([KeyboardHandlingSystem()])

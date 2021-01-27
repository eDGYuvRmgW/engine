from typing import TYPE_CHECKING

from framework import Direction, Game, Entity, Transform
from framework.rendering import Sprite, Text
from framework.inputs import key

if TYPE_CHECKING:
    from framework import Transform


class Box(Entity):

    def __init__(self, transform: Transform, speed: float = 100):
        super().__init__()
        self.text = Text("Hello, world!")

        self.yeet = transform
        self.speed = speed

    def update(self, delta: float):
        if key.is_down(key.LEFT):
            self.yeet.position += self.speed * Direction.LEFT * delta
        if key.is_down(key.RIGHT):
            self.yeet.position += self.speed * Direction.RIGHT * delta


game = Game("Simple Game")

box = Box(Transform())
game.add(box)

game.run(width=800, height=600)

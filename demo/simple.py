from typing import TYPE_CHECKING

from flaris import Direction, Entity, Game, Transform
from flaris.rendering import Sprite, Text
from flaris.inputs import key

if TYPE_CHECKING:
    from flaris import Transform


class Box(Entity):

    def __init__(self, transform: Transform, speed: float = 100):
        super().__init__()
        self.text = Text("Hello, world!")

        self.transform = transform
        self.speed = speed

    def update(self, delta: float) -> None:
        if key.is_down(key.LEFT):
            self.transform.position += self.speed * Direction.LEFT * delta
        if key.is_down(key.RIGHT):
            self.transform.position += self.speed * Direction.RIGHT * delta


game = Game("Simple Game")

box = Box(Transform())
game.add(box)

game.run(width=800, height=600)

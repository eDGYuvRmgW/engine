from flaris import Entity, Game, Transform, Vector
from flaris.rendering import Mesh, OrthographicCamera


class Cube(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        # NOTE: This doesn't do anything right now.
        self.mesh = Mesh("demo/cube.dae")

    def update(self, delta: float) -> None:
        self.transform.rotation -= Vector(0, 45, 0) * delta


class MainCamera(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        self.camera = OrthographicCamera(near=-1)


game = Game("Simple Demo")

camera = MainCamera(Transform(rotation=Vector(-30, -45, 0)))

game.add(camera)

cube = Cube(Transform())
game.add(cube)

game.run(width=800, height=600)

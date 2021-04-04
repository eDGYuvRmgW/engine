from flaris import Entity, Game, Transform, Vector
from flaris.rendering import Mesh, OrthographicCamera, DirectionalLight, Material, AmbientLight, Color
from flaris.inputs import key

class Cube(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        # NOTE: This doesn't do anything right now.
        self.mesh = Mesh("demo/cube.dae")
        self.material = Material(albedo=Color(1, 0.5, 0.5))
        assert Material in self

    def update(self, delta: float) -> None:
        return
        self.transform.rotation -= Vector(0, 45, 0) * delta


class MainCamera(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        self.camera = OrthographicCamera(near=-1)


class Sun(Entity):

    def __init__(self, transform: Transform, color: Color):
        super().__init__()
        self.light = DirectionalLight(color)
        self.light2 = AmbientLight(color)
        self.transform = transform

    def update(self, delta: float) -> None:
        if key.is_down(key.RIGHT):
            self.transform.rotation += Vector(0, 90, 0) * delta
        if key.is_down(key.LEFT):
            self.transform.rotation -= Vector(0, 90, 0) * delta
        if key.is_down(key.DOWN):
            self.transform.rotation += Vector(90, 0, 0) * delta
        if key.is_down(key.UP):
            self.transform.rotation -= Vector(90, 0, 0) * delta
        print(self.transform.rotation, end="\r")
        

game = Game("Simple Demo")

camera = MainCamera(Transform(rotation=Vector(-30, -45, 0)))

game.add(camera)

cube = Cube(Transform())
game.add(cube)

sun = Sun(Transform(), Color(1, 1, 1))
game.add(sun)

moon = Sun(Transform(rotation=Vector(0, 180, 0)), Color(0, 0, 1))
game.add(moon)

game.run(width=800, height=600)

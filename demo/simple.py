from flaris import Entity, Game, Transform, Vector
from flaris.rendering import Mesh, OrthographicCamera, DirectionalLight, Material, AmbientLight, Color, Texture
from flaris.inputs import key

class Stone(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        # NOTE: This doesn't do anything right now.
        self.mesh = Mesh("demo/cube.dae")
        self.texture = Texture("demo/checkers.png")
        self.material = Material(albedo=Color(0.2, 0.2, 0.2))


    def update(self, delta: float) -> None:
        return
        self.transform.rotation -= Vector(0, 45, 0) * delta


class Crate(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        # NOTE: This doesn't do anything right now.
        self.mesh = Mesh("demo/cube.dae")
        self.texture = Texture("demo/container.png")
        self.material = Material()


    def update(self, delta: float) -> None:
        return
        self.transform.rotation -= Vector(0, 45, 0) * delta



class MainCamera(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        self.camera = OrthographicCamera(near=-5)


class Sun(Entity):

    def __init__(self, transform: Transform, color: Color):
        super().__init__()
        self.light = DirectionalLight(color, intensity=1.5)
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
        

game = Game("Simple Demo")

camera = MainCamera(Transform(rotation=Vector(-30, -45, 0)))

game.add(camera)

for x in range(-3, 4):
    for z in range(-3, 4):
        cube = Stone(Transform(position=Vector(x, 0, z)))
        game.add(cube)

crate1 = Crate(Transform(position=Vector(-1, 1, 2)))
game.add(crate1)

crate2 = Crate(Transform(position=Vector(2, 1, 0)))
game.add(crate2)

sun = Sun(Transform(rotation=Vector(0, 90, -45)), Color(1, 1, 1))
game.add(sun)

game.run(width=800, height=600)

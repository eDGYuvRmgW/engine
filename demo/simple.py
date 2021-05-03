"""A simple demo."""
from flaris import Entity, Game, Transform, Vector
from flaris.rendering import Model, OrthographicCamera, DirectionalLight, Material, AmbientLight, Color, Texture
from flaris.inputs import key


class Cow(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        self.model = Model("demo/cow.dae")
        self.texture = Texture("demo/checkers.png")
        self.material = Material(albedo=Color(0.2, 0.2, 0.2))

    def update(self, delta: float):
        self.transform.position += Vector(0, 1, 0) * delta


class MainCamera(Entity):

    def __init__(self, transform):
        super().__init__()
        self.transform = transform
        self.camera = OrthographicCamera(near=-100)


class Sun(Entity):

    def __init__(self, transform: Transform, color: Color):
        super().__init__()
        self.transform = transform
        self.directional_light = DirectionalLight(color, intensity=1.5)
        self.ambient_light = AmbientLight(color)


game = Game("Simple Demo")

camera = MainCamera(Transform(rotation=Vector(-30, -45, 0)))
game.add(camera)

cow = Cow(Transform(scale=Vector(5, 5, 5)))
game.add(cow)

sun = Sun(Transform(rotation=Vector(0, 90, -45)), Color(1, 1, 1))
game.add(sun)

game.run(width=800, height=600)

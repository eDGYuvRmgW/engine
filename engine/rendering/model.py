"""Do something."""
from dataclasses import dataclass

from engine.rendering.mesh import Mesh
from engine.rendering.shader import Shader
from engine.rendering.texture import Texture


@dataclass
class Model:
    """Do something."""
    texture: Texture
    shader: Shader
    mesh: Mesh


from voxel import Transform, Game, GameObject
from voxel.rendering import Sprite, Icon
from voxel.physics import collision

game = Game("Breakout", icon=Icon("breakout/foo"))


class Block(GameObject):

    model = Model(mesh=Mesh("Asdf/asdf.png"))

    def __init__(self, transform: Transform):
        self.transform = transform

        size = Vector(self.texture.width, self.texture.height, 0)
        collider = BoxCollider(self.transform, size=size)
        self.rigidbody = Rigidbody(self.transform, collider, kinematic=True)


for i in range(0, 5):
    block = Block(Transform(position=Vector(i, 0, 0)))
    game.add(block)

Light()

if entity in simulation:
    pass

for entity in game:
    game.remove(entity)

game.run(width=520, height=520)

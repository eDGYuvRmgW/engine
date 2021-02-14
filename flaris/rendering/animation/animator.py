"""Do something."""
import glfw
import glm

from flaris import Vector

from flaris.rendering import Mesh, MeshRenderer, Joint

from .animation import Animation
from .keyframe import Keyframe

__all__ = ["Animator"]


class Animator(): # pylint: disable=too-few-public-methods
    """Do something."""

    def __init__(self, mesh: Mesh):
        """Do something."""
        self.mesh = mesh
        self.current_animation = None
        self.animation_time = 0.0

    def play(self, animation: Animation) -> None:
        """Do something."""
        self.animation_time = 0.0
        self.current_animation = animation

    def update(self) -> None:
        """Do something."""
        if self.current_animation is not None:
            self.animation_time += glfw.get_time() # TODO: might not be right??
            if self.animation_time > self.current_animation.length:
                self.animation_time %= self.current_animation.length

            current_pose = self.calculate_pose()
            self.apply_pose(current_pose, mesh.root)

    def calculate_pose(self) -> dict:
        """Do something."""
        frames = self.get_previous_next_keyframes()
        progression = self.calculate_progression(frames[0], frames[1])
        return self.interpolate_poses(frames[0], frames[1], progression)

    def apply_pose(self, current_pose: dict, joint: Joint, parent_transform: glm.mat4 = glm.mat4()) -> None:
        """Do something."""
        current_local_transform = current_pose[joint.name]
        current_transform = parent_transform * current_local_transform

        for child in joint.children:
            self.apply_pose(current_pose, child, current_transform)

        current_transform = current_transform * joint.inverse_bind_transform
        joint.animated_transform = current_transform

    def get_previous_next_keyframes(self) -> list:
        """Do something."""
        all_frames = self.current_animation.keyframes
        previous_frame = all_frames[0]
        next_frame = all_frames[0]

        for frame in all_frames:
            next_frame = frame
            if next_frame.timestamp > self.animation_time:
                break
            previous_frame = frame

        return [previous_frame, next_frame]

    def calculate_progression(self, previous_frame: Keyframe, next_frame: Keyframe) -> float:
        """Do something."""
        total_time = next_frame.timestamp - previous_frame.timestamp
        current_time = self.animation_time - previous_frame.timestamp
        return current_time / total_time

    def interpolate_poses(self, previous_frame : Keyframe, next_frame: Keyframe, progression: float) -> dict:
        """Do something."""
        current_pose = {}

        for name in previous_frame.keyframes.keys():
            previous_transform = previous_frame.keyframes[name]
            next_transform = next_frame.keyframes[name]
            current_transform = JointTransform.interpolate(previous_transform, next_transform, progression)
            current_pose[name] = current_transform.local_transform

        return current_pose


class JointTransform(): # pylint: disable=too-few-public-methods
    """Do something."""

    def __init__(self, position: Vector):
        """Do something."""
        self.position = position

    @staticmethod
    def interpolate(first: JointTransform, second: JointTransform, progression: float) -> JointTransform:
        """Do something."""
        return JointTransform(Vector())

    @property
    def local_transform(self) -> glm.mat4:
        """Do something."""

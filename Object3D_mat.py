from OpenGL.GL import *
from Mesh3D import Mesh3D
import pygame
import primitives
import math
import numpy

# An object in 3D space, with a mesh, position, orientation (yaw/pitch/roll),
# and scale.

class Object3D:
    def __init__(self, mesh: Mesh3D,
                 position: numpy.array = numpy.array([0.0, 0.0, 0.0]),
                 orientation: numpy.array = numpy.array([0.0, 0.0, 0.0]),
                 scale: numpy.array = numpy.array([1.0, 1.0, 1.0])):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale
        #ScaleX = 1

    def local_to_world(self, local_vertex: numpy.array) -> numpy.array:
        """
        Transforms the given local-space vertex to world space,
        by applying the translation, orientation, and scale vectors
        of the Object3D.
        """

        # Finish this function to return a transformed world-space vertex.
        # Remember the correct order of compound transformations:
        # scale
        # then rotate yaw, rotate pitch, rotate roll
        # then translate.

        #Scaling
        LocalMatrix = numpy.array([
            [local_vertex[0]],
            [local_vertex[1]],
            [local_vertex[2]],
            [1]
        ])

        Scale = numpy.array([
            [self.scale[0], 0, 0, 0],
            [0, self.scale[1], 0, 0],
            [0, 0, self.scale[2], 0],
            [0, 0, 0, 1]
        ])

        LocalMatrix = numpy.matmul(Scale, LocalMatrix)

        x, y, z = self.orientation  # unpacking

        yaw_cos = math.cos(y)  # math.cos(self.orientation[1]
        yaw_sin = math.sin(y)

        pitch_cos = math.cos(x)  # math.cos(self.orientation[0]
        pitch_sin = math.sin(x)

        roll_cos = math.cos(z) # math.cos(self.orientation[2]
        roll_sin = math.sin(z)

        #Yaw (Rotate Y-Axis)
        Yaw = numpy.array([
            [yaw_cos, 0, yaw_sin, 0],
            [0, 1, 0, 0],
            [-yaw_sin, 0, yaw_cos,  0],
            [0, 0, 0, 1]
        ])

        LocalMatrix = numpy.matmul(Yaw, LocalMatrix)

        #Pitch (Rotate X-Axis)
        Pitch = numpy.array([
            [1, 0, 0, 0],
            [0, pitch_cos, -pitch_sin, 0],
            [0, pitch_sin, pitch_cos, 0],
            [0, 0, 0, 1]
        ])

        LocalMatrix = numpy.matmul(Pitch, LocalMatrix)

        #Roll (Rotate Z-Axis)
        Roll = numpy.array([
            [roll_cos, -roll_sin, 0, 0],
            [roll_sin, roll_cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        LocalMatrix = numpy.matmul(Roll, LocalMatrix)


        #Translation
        Translation = numpy.array([
            [self.position[0], 0, 0, 0],
            [0, self.position[1], 0, 0],
            [0, 0, self.position[2], 0],
            [0, 0, 0, 1]
        ])

        LocalMatrix2 = numpy.array([
            [LocalMatrix[0,0], 0, 0, 0],
            [0, LocalMatrix[1,0], 0, 0],
            [0, 0, LocalMatrix[2,0], 0],
            [0, 0, 0, 0]
        ])

        LocalMatrix = Translation + LocalMatrix2

        local_vertex = (LocalMatrix[0, 0], LocalMatrix[1, 1], LocalMatrix[2, 2])
        return local_vertex

    def world_to_view(self, world_vertex) -> numpy.array:
        """
        Transforms the given world-space vertex to view space,
        by translating and rotating the object according to the
        camera location and vectors.
        """

        # We don't have a movable camera for this demo, so world space
        # is identical to view space.
        return world_vertex

    def view_to_clip(self, view_vertex: numpy.array, frustum) -> numpy.array:
        """
        Projects the view-space vertex to clip space(normalized device coordinates).
        """
        # Finish this function to compute (xn, yn, zn) by first projecting
        # to the near-plane coordinates (xp, yp, zp), and then interpolating
        # along the clip space 2x2x2 cube.
        near, far, left, right, bottom, top = frustum

        xp = view_vertex[0] * (-near / view_vertex[2])
        yp = view_vertex[1] * (-near / view_vertex[2])
        zp = -near

        view_vertex = ((2 * xp) / (right - left), (2 * yp) / (top - bottom), (2 * zp) / (far - near))
        return view_vertex

    def clip_to_screen(self, clip_vertex: pygame.Vector3, surface: pygame.Surface) -> tuple[int, int]:
        """
        Projects the clip-space/NDC coordinate to the screen space represented
        by the given pygame Surface object.
        """
        clip_vertex = (((clip_vertex[0] + 1) / 2) * surface.get_width(), (surface.get_height() - ((clip_vertex[1] + 1) / 2) * surface.get_height()))

        # Finish this function to compute (xs, ys). Don't forget that
        # the the positive y-axis goes DOWN in Pygame, but UP in clip space.
        return (int(clip_vertex[0]), int(clip_vertex[1]))

    def draw(self, surface: pygame.Surface, frustum):
        projected = []
        for v_local in self.mesh.vertices:
            v_world = self.local_to_world(v_local)
            v_view = self.world_to_view(v_world)
            v_clip = self.view_to_clip(v_view, frustum)
            v_screen = self.clip_to_screen(v_clip, surface)
            projected.append(v_screen)

        for tri in self.mesh.faces:
            a, b, c = (
                projected[tri[0]],
                projected[tri[1]],
                projected[tri[2]],
            )
            primitives.draw_triangle(surface, a, b, c, tri[3])

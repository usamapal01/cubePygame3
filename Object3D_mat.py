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
                 scale: numpy.array = numpy.array([0.5, 0.5, 0.5])):
        self.mesh = mesh
        self.position = position
        self.orientation = orientation
        self.scale = scale

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

        # scale
        scale_mat = numpy.array([[self.scale[0], 0, 0, 0],
                                 [0, self.scale[1], 0, 0],
                                 [0, 0, self.scale[2], 0],
                                 [0, 0, 0, 1]])

        x, y, z = self.orientation  # unpacking

        yaw_cos = math.cos(y)  # math.cos(self.orientation[1]
        yaw_sin = math.sin(y)

        pitch_cos = math.cos(x)  # math.cos(self.orientation[0]
        pitch_sin = math.sin(x)

        roll_cos = math.cos(z)  # math.cos(self.orientation[2]
        roll_sin = math.sin(z)

        # Yaw (Rotate Y-Axis)
        yaw_mat = numpy.array([
            [yaw_cos, 0, -yaw_sin, 0],
            [0, 1, 0, 0],
            [yaw_sin, 0, yaw_cos, 0],
            [0, 0, 0, 1]
        ])

        # Pitch (Rotate X-Axis)
        pitch_mat = numpy.array([
            [1, 0, 0, 0],
            [0, pitch_cos, pitch_sin, 0],
            [0, -pitch_sin, pitch_cos, 0],
            [0, 0, 0, 1]
        ])

        # Roll (Rotate Z-Axis)
        roll_mat = numpy.array([
            [roll_cos, roll_sin, 0, 0],
            [-roll_sin, roll_cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # translate
        translated_mat = numpy.array([
            [1, 0, 0, self.position[0]],
            [0, 1, 0, self.position[1]],
            [0, 0, 1, self.position[2]],
            [0, 0, 0, 1]
        ])

        # rotate (multiplying matrices in correct order)
        local_vertex = numpy.matmul(translated_mat, numpy.matmul(roll_mat, numpy.matmul(
            pitch_mat, numpy.matmul(yaw_mat, numpy.matmul(scale_mat, local_vertex)))))

        return local_vertex

    def world_to_view(self, world_vertex, camera) -> numpy.array:
        """
        Transforms the given world-space vertex to view space,
        by translating and rotating the object according to the
        camera location and vectors.
        """

        # We don't have a movable camera for this demo, so world space
        # is identical to view space.
        eyeX, eyeY, eyeZ, atX, atY, atZ, upX, upY, upZ = camera

        forward = numpy.array([atX - eyeX, atY - eyeY, atZ - eyeZ])
        forward = forward / numpy.linalg.norm(forward)

        right = numpy.cross(forward, numpy.array([upX, upY, upZ]))
        right = right / numpy.linalg.norm(right)

        up = numpy.cross(right, forward)
        up = up / numpy.linalg.norm(up)

        eye = numpy.array([eyeX, eyeY, eyeZ])

        tx = numpy.dot(eye, right)
        ty = numpy.dot(eye, up)
        tz = numpy.dot(eye, forward)

        a_camera = numpy.array([[right[0], up[0], forward[0], 0],
                                [right[1], up[1], forward[1], 0],
                                [right[2], up[2], forward[2], 0],
                                [tx, ty, tz, 1]])

        a_camera_inverse = numpy.linalg.inv(a_camera)

        world_vertex = numpy.matmul(a_camera_inverse, world_vertex)

        # view_vertex = numpy.matmul(a_camera_inverse, world_vertex)
        # return view_vertex

        return world_vertex

    def view_to_clip(self, view_vertex, frustum) -> numpy.array:
        """
        Projects the view-space vertex to clip space(normalized device coordinates).
        """
        # Finish this function to compute (xn, yn, zn) by first projecting
        # to the near-plane coordinates (xp, yp, zp), and then interpolating
        # along the clip space 2x2x2 cube.
        near, far, left, right, bottom, top = frustum

        a_persp = numpy.array([
            [2 * near / (right - left), 0, (right + left) / (right - left), 0],
            [0, 2 * near / (top - bottom), (top + bottom) / (top - bottom), 0],
            [0, 0, (far + near) / (near - far), 2 * far * near / (near - far)],
            [0, 0, -1, 0]
        ])

        view_vertex = numpy.matmul(a_persp, view_vertex)

        view_vertex = numpy.array([view_vertex[0] / view_vertex[3],
                                   view_vertex[1] / view_vertex[3],
                                   view_vertex[2], view_vertex[3]
                                   ])
        return view_vertex

    def clip_to_screen(self, clip_vertex, surface: pygame.Surface) -> tuple[int, int]:
        """
        Projects the clip-space/NDC coordinate to the screen space represented
        by the given pygame Surface object.
        """
        width = surface.get_width()
        height = surface.get_height()

        xn = clip_vertex[0]
        xy = clip_vertex[1]

        xs = (xn + 1) / 2 * width
        ys = height - (xy + 1) / 2 * height

        # Finish this function to compute (xs, ys). Don't forget that
        # the the positive y-axis goes DOWN in Pygame, but UP in clip space.
        return int(xs), int(ys)

    def draw(self, surface: pygame.Surface, frustum, camera):
        projected = []
        for v_local in self.mesh.vertices:
            v_world = self.local_to_world(v_local)
            v_view = self.world_to_view(v_world, camera)
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

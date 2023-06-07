# from OpenGL.GL import *
# import pygame
#
# # This code is reorganized somewhat from the reading, so we can
# # add colors to each of the faces.
# class Mesh3D:
#     def __init__(self, vertices: list[tuple[pygame.Vector3]], faces: list[tuple[tuple[int, int, int, pygame.Color]]]):
#         self.vertices = vertices
#         self.faces = faces
#
#     def cube():
#         Vertices = [
#                  (0.5, -0.5, 0.5),      #0
#                  (-0.5, -0.5, 0.5),     #1
#                  (0.5, 0.5, 0.5),       #2
#                  (-0.5, 0.5, 0.5),      #3
#                  (0.5, 0.5, -0.5),      #4
#                  (-0.5, 0.5, -0.5),     #5
#                  (-0.5, -0.5, -0.5),    #6
#                  (0.5, -0.5, -0.5)      #7
#         ]
#
#         Faces = [
#             (0, 2, 3, pygame.Color(255, 0, 0)), (0, 3, 1, pygame.Color(127, 0, 0)),
#             (7, 6, 4, pygame.Color(0, 255, 0)), (4, 5, 6, pygame.Color(0, 127, 0)),
#             (3, 1, 5, pygame.Color(0, 0, 255)), (6, 1, 5, pygame.Color(0, 0, 127)),
#             (2, 4, 7, pygame.Color(255, 255, 0)), (2, 0, 7, pygame.Color(127, 127, 0)),
#             (1, 0, 7, pygame.Color(255, 0, 255)), (6, 7, 1, pygame.Color(127, 0, 127)),
#             (3, 4, 5, pygame.Color(0, 255, 255)), (3, 2, 4, pygame.Color(0, 127, 127))
#         ]
#         return Mesh3D(Vertices, Faces)


from OpenGL.GL import *
import pygame


# This code is reorganized somewhat from the reading, so we can
# add colors to each of the faces.
class Mesh3D:
    def __init__(
            self,
            vertices: list[tuple[float, float, float]],
            faces: list[tuple[int, int, int, pygame.Color]],
    ):
        self.vertices = vertices
        self.faces = faces


    @staticmethod
    def cube():
        verts = [
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, 0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (0.5, -0.5, 0.5),
        ]
        tris = [
            (0, 1, 2, pygame.Color(255, 0, 0)),
            (0, 2, 3, pygame.Color(127, 0, 0)),
            (4, 0, 3, pygame.Color(0, 255, 0)),
            (4, 3, 7, pygame.Color(0, 127, 0)),
            (5, 4, 7, pygame.Color(0, 0, 255)),
            (5, 7, 6, pygame.Color(0, 0, 127)),
            (1, 5, 6, pygame.Color(255, 255, 0)),
            (1, 6, 2, pygame.Color(127, 127, 0)),
            (4, 5, 1, pygame.Color(255, 0, 255)),
            (4, 1, 0, pygame.Color(127, 0, 127)),
            (2, 6, 7, pygame.Color(0, 255, 255)),
            (2, 7, 3, pygame.Color(0, 127, 127)),

        ]

        return Mesh3D(verts, tris)

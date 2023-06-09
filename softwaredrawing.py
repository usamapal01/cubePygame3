import pygame
from Mesh3D import Mesh3D
import math
# from Object3D_mat import Object3D
from Object3D_mat import Object3D

######
# REQUIREMENTS:
# make a file "primitives.py", and copy all your draw_line, draw_triangle, and fill_triangle code there.
# copy the Mesh3D file from the last lesson.


def make_cube():
    return Object3D(Mesh3D.cube())


if __name__ == "__main__":
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    done = False
    m = make_cube()
    m.position = pygame.Vector3(0, 0, -2)

    # Given the vertical half-FOV, compute coordinates of the perspective frustum.
    v_fov = 30
    near = 0.1
    far = 100
    top = math.tan(math.radians(v_fov)) * near
    right = top * screen_width / screen_height
    left = -right
    bottom = -top

    print("Frustum coordinates: near, far, left, right, bottom, top")
    print(near, far, left, right, bottom, top)
    frustum = (near, far, left, right, bottom, top)
    black = pygame.Color(0, 0, 0)
    # m.scale[0] = 1
    # m.scale[1] = 1
    # m.scale[2] = 1
    camera = (1, 3, -2, 1, 3, -5, 0, 1, 0)


    while not done:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        m.orientation += pygame.Vector3(0.001, 0.001, 0.001)
        m.position += pygame.Vector3(0.00, 0.00, -0.001)  # backwards
        m.scale += pygame.Vector3(-0.001, -0.001, -0.001)  # reverted

        m.draw(screen, frustum, camera)
        pygame.display.flip()
    pygame.quit()

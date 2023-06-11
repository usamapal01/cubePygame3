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
    m.position = pygame.Vector3(0, 0, -5)

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
    m.scale[0] = 0.25
    m.scale[1] = 0.25
    m.scale[2] = 0.25

    # static_orientation = m.orientation
    # static_position = m.position
    # static_scale = m.scale
    camera = (1, 3, -2, 1, 3, -5, 0, 1, 0)

    m.model_matrix_update()
    m.view_matrix_update(camera)
    m.projection_matrix_update(frustum)

    curr_orientation = (m.orientation[0], m.orientation[1], m.orientation[2])
    curr_scale = (m.scale[0], m.scale[1], m.scale[2])
    curr_position = (m.position[0], m.position[1], m.position[2])
    curr_camera = (camera[0], camera[1], camera[2], camera[3], camera[4], camera[5], camera[6], camera[7], camera[8])
    curr_frustum = (frustum[0], frustum[1], frustum[2], frustum[3], frustum[4], frustum[5])

    while not done:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # checking if the cube has been moved, scaled, or turned
        if curr_orientation != m.orientation or curr_position != m.position or curr_scale != m.scale:
            m.model_matrix_update()

            curr_orientation = (m.orientation[0], m.orientation[1], m.orientation[2])
            curr_scale = (m.scale[0], m.scale[1], m.scale[2])
            curr_position = (m.position[0], m.position[1], m.position[2])
        if curr_camera != (
                camera[0], camera[1], camera[2], camera[3], camera[4], camera[5], camera[6], camera[7], camera[8]):
            curr_camera = (
                camera[0], camera[1], camera[2], camera[3], camera[4], camera[5], camera[6], camera[7], camera[8])
            m.projection_matrix_update(curr_camera)
        if curr_frustum != (frustum[0], frustum[1], frustum[2], frustum[3], frustum[4], frustum[5]):
            curr_frustum = (frustum[0], frustum[1], frustum[2], frustum[3], frustum[4], frustum[5])
            m.view_matrix_update(curr_frustum)

        m.orientation += pygame.Vector3(0.001, 0.001, 0.001)
        m.position += pygame.Vector3(0.00, 0.00, -0.001)  # backwards
        m.scale += pygame.Vector3(-0.001, -0.001, -0.001)  # reverted

        m.draw(screen, m.model_matrix, m.view_matrix, m.projection_matrix)
        pygame.display.flip()
    pygame.quit()

import pygame

def fill_triangle(surface: pygame.Surface, point_a: tuple[int, int], point_b: tuple[int, int], point_c: tuple[int, int], color: pygame.Color):
    # First, sort the vertices by y coordinate
    if point_a[1] > point_b[1]:
        point_a, point_b = point_b, point_a
    if point_a[1] > point_c[1]:
        point_a, point_c = point_c, point_a
    if point_b[1] > point_c[1]:
        point_b, point_c = point_c, point_b
    # Now, A has the smallest y coordinate, and C has the largest.
    im_AC = (point_c[0] - point_a[0]) / (point_c[1] - point_a[1])
    x_AB = x_AC = point_a[0]

    # Draw the upper segment of the triangle: the lines connecting edge AB with part of AC.
    if point_a[1] != point_b[1]:
        # First find the inverse slope of AB and AC.
        im_AB = (point_b[0] - point_a[0]) / (point_b[1] - point_a[1])

        # We will "walk" down the lines by repeatedly adding the inverse slope
        # to an x-coordinate accumulator for each line segment, starting at point A.

        surface.set_at(point_a, color)
        # For the vertical range of edge AB:
        for y in range(point_a[1] + 1, point_b[1]):
            # Compute the x coordinate for edge AB and AC by moving their current coordinate
            # by their inverse slope.
            x_AB += im_AB
            x_AC += im_AC

            # Connect the two points with a horizontal line.
            # Make sure the range goes in increasing order from left to right.
            if x_AB > x_AC:
                l, r = x_AC, x_AB
            else:
                l, r = x_AB, x_AC

            for x in range(int(l), int(r) + 1):
                surface.set_at((x, y), color)

    # Repeat the process, for the lower segment: edge BC and the remainder of edge AC.
    if point_b[1] != point_c[1]:
        im_BC = (point_c[0] - point_b[0]) / (point_c[1] - point_b[1])
        x_BC = point_b[0]
        for y in range(point_b[1], point_c[1]):
            x_BC += im_BC
            x_AC += im_AC

            if x_AC > x_BC:
                l, r = x_BC, x_AC
            else:
                l, r = x_AC, x_BC

            for x in range(int(l), int(r) + 1):
                surface.set_at((x, y), color)

def draw_line_low(surface: pygame.Surface, start: tuple[int, int], end: tuple[int, int], color: pygame.Color):
    x0, y0 = start
    x1, y1 = end

    if x0 > x1:
        x0, x1 = x1, x0
        temp = y0
        y0 = y1
        y1 = temp

    dx = x1 - x0
    dy = y1 - y0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1 + 1):
        surface.set_at((x, int(y)), color)
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * (dy)


def draw_triangle(surface: pygame.Surface, point_a: tuple[int, int], point_b: tuple[int, int], point_c: tuple[int, int], color: pygame.Color,):
    draw_line(surface, point_a, point_b, color)
    draw_line(surface, point_a, point_c, color)
    draw_line(surface, point_b, point_c, color)

def draw_line_high(surface: pygame.Surface, start: tuple[int, int], end: tuple[int, int],color: pygame.Color):
    x0, y0 = start
    x1, y1 = end

    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx

    D = (2 * dx) - dy
    x = x0

    for y in range(y0, y1 + 1):
        surface.set_at((x, y), color)
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * (dx)


def draw_line_vertical(surface: pygame.Surface, start: tuple[int, int], end: tuple[int, int], color: pygame.Color):
    x0, y0 = start
    x1, y1 = end
    for y in range(y0, y1 + 1):
        surface.set_at((x0, y), color)


def draw_line(surface: pygame.Surface, start: tuple[int, int], end: tuple[int, int], color: pygame.Color):
    x0, y0 = start
    x1, y1 = end
    if x0 == x1:
        draw_line_vertical(surface, start, end, color)
    else:
        m = (y1 - y0) / (x1 - x0)
        if abs(m) <= 1:
            draw_line_low(surface, start, end, color)
        else:
            draw_line_high(surface, start, end, color)










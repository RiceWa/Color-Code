import pygame
import math
from pygame.locals import *
from sys import exit

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
CENTER = [WIDTH // 2, HEIGHT // 2]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubik's Cube")

# Perspective distance
distance = 400

# Initial rotation angles for the entire cube
angle_x, angle_y = 0, 0
is_dragging = False
last_mouse_pos = (0, 0)

# Colors for each face (Front, Back, Bottom, Top, Right, Left)
face_colors = {
    'front': (255, 0, 0),       # Red
    'back': (255, 165, 0),      # Orange
    'bottom': (255, 255, 0),    # Yellow
    'top': (255, 255, 255),     # White
    'right': (0, 255, 0),       # Green
    'left': (0, 0, 255),        # Blue
}

# Define the vertices for the cube (a 2x2x2 cube at the origin)
vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1]
]

# Define the faces of the cube with the corners
faces = {
    'front': [0, 1, 2, 3],
    'back': [4, 5, 6, 7],
    'bottom': [0, 1, 5, 4],
    'top': [2, 3, 7, 6],
    'right': [1, 2, 6, 5],
    'left': [0, 3, 7, 4]
}

def rotate(point, angle_x, angle_y):
    """Rotate point around the X and Y axes"""
    x, y, z = point
    
    # Rotate around X-axis
    y_temp = y * math.cos(angle_x) - z * math.sin(angle_x)
    z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y = y_temp

    # Rotate around Y-axis
    x_temp = x * math.cos(angle_y) + z * math.sin(angle_y)
    z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x = x_temp

    return [x, y, z]

def project(x, y, z):
    """Project a 3D point into 2D"""
    factor = distance / (z + 5)
    x_proj = int(x * factor) + CENTER[0]
    y_proj = int(y * factor) + CENTER[1]
    return x_proj, y_proj

def draw_face(face_vertices, color):
    """Draw a single face of the cube with a 3x3 grid"""
    pygame.draw.polygon(screen, color, face_vertices)

    # Draw black lines for the 3x3 grid
    for i in range(1, 3):
        # Horizontal lines
        p1 = [
            face_vertices[0][0] + (face_vertices[3][0] - face_vertices[0][0]) * i / 3,
            face_vertices[0][1] + (face_vertices[3][1] - face_vertices[0][1]) * i / 3,
        ]
        p2 = [
            face_vertices[1][0] + (face_vertices[2][0] - face_vertices[1][0]) * i / 3,
            face_vertices[1][1] + (face_vertices[2][1] - face_vertices[1][1]) * i / 3,
        ]
        pygame.draw.line(screen, (0, 0, 0), p1, p2, 3)

        # Vertical lines
        p3 = [
            face_vertices[0][0] + (face_vertices[1][0] - face_vertices[0][0]) * i / 3,
            face_vertices[0][1] + (face_vertices[1][1] - face_vertices[0][1]) * i / 3,
        ]
        p4 = [
            face_vertices[3][0] + (face_vertices[2][0] - face_vertices[3][0]) * i / 3,
            face_vertices[3][1] + (face_vertices[2][1] - face_vertices[3][1]) * i / 3,
        ]
        pygame.draw.line(screen, (0, 0, 0), p3, p4, 3)

def rotate_face(face_indices, axis, angle):
    """Rotate a specific face around a given axis (x, y, or z)"""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    for i in face_indices:
        x, y, z = vertices[i]
        if axis == 'x':
            y, z = y * cos_angle - z * sin_angle, y * sin_angle + z * cos_angle
        elif axis == 'y':
            x, z = x * cos_angle + z * sin_angle, -x * sin_angle + z * cos_angle
        elif axis == 'z':
            x, y = x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle
        vertices[i] = [x, y, z]

# Command mapping for rotations
commands = {
    "F": lambda: rotate_face(faces['front'], 'z', -math.pi / 2),
    "f": lambda: rotate_face(faces['front'], 'z', math.pi / 2),
    "B": lambda: rotate_face(faces['back'], 'z', math.pi / 2),
    "b": lambda: rotate_face(faces['back'], 'z', -math.pi / 2),
    "L": lambda: rotate_face(faces['left'], 'x', math.pi / 2),
    "l": lambda: rotate_face(faces['left'], 'x', -math.pi / 2),
    "R": lambda: rotate_face(faces['right'], 'x', -math.pi / 2),
    "r": lambda: rotate_face(faces['right'], 'x', math.pi / 2),
    "U": lambda: rotate_face(faces['top'], 'y', -math.pi / 2),
    "u": lambda: rotate_face(faces['top'], 'y', math.pi / 2),
    "D": lambda: rotate_face(faces['bottom'], 'y', math.pi / 2),
    "d": lambda: rotate_face(faces['bottom'], 'y', -math.pi / 2),
}

while True:
    screen.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            is_dragging = True
            last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == MOUSEBUTTONUP:
            is_dragging = False
        elif event.type == MOUSEMOTION and is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            delta_x = mouse_x - last_mouse_pos[0]
            delta_y = mouse_y - last_mouse_pos[1]
            last_mouse_pos = (mouse_x, mouse_y)

            # Update rotation angles based on mouse movement
            angle_y += math.radians(delta_x * 0.5)
            angle_x += math.radians(delta_y * 0.5)
        elif event.type == KEYDOWN:
            command = event.unicode
            if command in commands:
                commands[command]()

    # Rotate and project the vertices
    rotated_vertices = [rotate(v, angle_x, angle_y) for v in vertices]
    projected_vertices = [project(*v) for v in rotated_vertices]

    # Draw each face with depth sorting
    face_depths = []
    for face_name, indices in faces.items():
        avg_z = sum(rotated_vertices[i][2] for i in indices) / 4
        face_depths.append((avg_z, face_name))

    face_depths.sort(reverse=True, key=lambda x: x[0])

    for _, face_name in face_depths:
        indices = faces[face_name]
        face_vertices = [projected_vertices[i] for i in indices]
        draw_face(face_vertices, face_colors[face_name])

    pygame.display.flip()
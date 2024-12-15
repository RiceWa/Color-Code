import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def draw_cube(ax, position, size=1):
    """Draw a cube at a specific position with hidden internal faces."""
    x, y, z = position
    
    # Define vertices of a unit cube
    vertices = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
        [1, 0, 1]
    ]) * size

    vertices += [x, y, z]

    # Define the 6 faces of the cube
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Front
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Back
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Left
        [vertices[3], vertices[2], vertices[6], vertices[7]]   # Right
    ]

    # Only draw faces on the outer edges
    x_cond = (x == 0 or x == 2)
    y_cond = (y == 0 or y == 2)
    z_cond = (z == 0 or z == 2)

    # Map conditions to faces
    draw_faces = [
        z == 0,           # Bottom face
        z == 2,           # Top face
        y == 0,           # Front face
        y == 2,           # Back face
        x == 0,           # Left face
        x == 2            # Right face
    ]

    # Plot the faces that meet the conditions
    for i, face in enumerate(faces):
        if draw_faces[i]:
            ax.add_collection3d(Poly3DCollection([face], color='blue', edgecolor='black', alpha=0.5))

def plot_rubiks_cube():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw the 3x3x3 grid of cubes
    for x in range(3):
        for y in range(3):
            for z in range(3):
                draw_cube(ax, (x, y, z))

    # Set the axes limits
    ax.set_xlim([0, 3])
    ax.set_ylim([0, 3])
    ax.set_zlim([0, 3])
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    plt.show()

# Run the function to display the Rubik's cube
plot_rubiks_cube()

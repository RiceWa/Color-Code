import random

# Generate color mapping
def generate_color_mapping(seed):
    random.seed(seed)
    colors = ['White', 'Yellow', 'Blue', 'Green', 'Red', 'Orange']
    binaries = ['000', '001', '010', '011', '100', '101']
    random.shuffle(binaries)
    return dict(zip(colors, binaries))

# Generate randomized character set
def generate_character_set(seed):
    random.seed(seed)
    charset = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+")
    random.shuffle(charset)
    return ''.join(charset)

# Generate randomized matrix positions
def generate_matrix_positions(seed):
    random.seed(seed)
    positions = [0, 1, 2, 3, 5, 6, 7, 8]
    random.shuffle(positions)
    return positions

# Convert a face matrix to binary using the randomized positions
def matrix_to_binary(face_matrix, positions, color_mapping):
    return ''.join(color_mapping[face_matrix[i]] for i in positions)

# Generate the password
def generate_password_from_cube(cube_faces, seed, length=16):
    # Generate mappings based on the seed
    color_mapping = generate_color_mapping(seed)
    randomized_charset = generate_character_set(seed)
    matrix_positions = generate_matrix_positions(seed)
    
    # Convert each face to binary data
    binary_data = ''.join(matrix_to_binary(face, matrix_positions, color_mapping) for face in cube_faces)
    
    # Convert binary data to a password

    # Takes 8 Bits and converts to an int
    # Use Modulus operator to keep number below number of char in charset
    # Retrieve character from charset and append to password
    # Truncate result to keep length to 16 or less characters
    password = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            break
        index = int(byte, 2) % len(randomized_charset)
        password += randomized_charset[index]
    
    return password[:length]

# Example scrambled cube state (6 faces, 3x3 matrices each)
# In order, White - Yellow - Blue - Green - Red - Orange
# Assuming White is top for Red - Orange - Green - Blue,
# Red is bottom for White and Top for Yellow.

# I will eventually make a vision system for this
# With the current scramble, the cube is solved
example_cube_faces = [
    ['White', 'White', 'White', 'White', 'White', 'White', 'White', 'White', 'White'],  # Center White
    ['Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow'],  # Center Yellow
    ['Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue'],  # Center Blue
    ['Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Green'],  # Center Green
    ['Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Red'],  # Center Red
    ['Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', 'Orange', ]  # Center Orange
]

# Generate a password using a seed
seed = input("Enter a seed: ")
password = generate_password_from_cube(example_cube_faces, seed)
print("Generated Password:", password)

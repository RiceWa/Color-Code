from PIL import Image
import textwrap

# Define the color mapping
COLOR_MAPPING = {
    '0000': (0, 0, 0),          # Black
    '0001': (128, 0, 0),        # Dark Red
    '0010': (0, 128, 0),        # Dark Green
    '0011': (0, 0, 128),        # Dark Blue
    '0100': (128, 128, 0),      # Dark Yellow
    '0101': (128, 0, 128),      # Dark Magenta
    '0110': (0, 128, 128),      # Dark Cyan
    '0111': (64, 64, 64),       # Dark Gray
    '1000': (192, 192, 192),    # Light Gray
    '1001': (255, 0, 0),        # Red
    '1010': (0, 255, 0),        # Green
    '1011': (0, 0, 255),        # Blue
    '1100': (255, 255, 0),      # Yellow
    '1101': (255, 0, 255),      # Magenta
    '1110': (0, 255, 255),      # Cyan
    '1111': (255, 255, 255)     # White
}

def text_to_binary(text):
    # Convert text to binary, padded to 8 bits per character
    return ''.join(format(ord(char), '08b') for char in text)

def pad_binary_data(binary_data, size):
    # Pad the binary data to fit the required size (8192 bits for 64x64)
    return binary_data.ljust(size, '0')

def create_image_from_text(text, output_path):
    # Convert text to binary and pad to 16384 bits (2048 bytes)
    binary_data = text_to_binary(text)
    binary_data = pad_binary_data(binary_data, 16384)

    # Create a new 64x64 image
    img = Image.new('RGB', (64, 64))

    # Iterate through the binary data in 2-bit chunks and set pixel colors
    for i in range(0, len(binary_data), 4):
        x = (i // 4) % 64
        y = (i // 4) // 64
        color_code = binary_data[i:i+4]
        color = COLOR_MAPPING[color_code]
        img.putpixel((x, y), color)

    # Save the image
    img.save(output_path)
    print(f"Image saved to {output_path}")

# Conversion
text = input("Enter text to convert: ")
file_name = input("Enter a file name: ")
create_image_from_text(text, f"{file_name}.png")

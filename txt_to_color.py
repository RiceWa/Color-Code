from PIL import Image
import textwrap

# Define the color mapping
COLOR_MAPPING = {
    '00': (0, 0, 0),         # Black
    '01': (255, 0, 0),       # Red
    '10': (0, 255, 0),       # Green
    '11': (0, 0, 255)        # Blue
}

def text_to_binary(text):
    # Convert text to binary, padded to 8 bits per character
    return ''.join(format(ord(char), '08b') for char in text)

def pad_binary_data(binary_data, size):
    # Pad the binary data to fit the required size (8192 bits for 64x64)
    return binary_data.ljust(size, '0')

def create_image_from_text(text, output_path):
    # Convert text to binary and pad to 8192 bits (1024 bytes)
    binary_data = text_to_binary(text)
    binary_data = pad_binary_data(binary_data, 8192)

    # Create a new 64x64 image
    img = Image.new('RGB', (64, 64))

    # Iterate through the binary data in 2-bit chunks and set pixel colors
    for i in range(0, len(binary_data), 2):
        x = (i // 2) % 64
        y = (i // 2) // 64
        color_code = binary_data[i:i+2]
        color = COLOR_MAPPING[color_code]
        img.putpixel((x, y), color)

    # Save the image
    img.save(output_path)
    print(f"Image saved to {output_path}")

# Conversion
text = input("Enter text to convert: ")
file_name = input("Enter a file name: ")
create_image_from_text(text, f"{file_name}.png")

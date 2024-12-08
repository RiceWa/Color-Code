from PIL import Image

# Reverse color mapping
REVERSE_COLOR_MAPPING = {
    (0, 0, 0): '00',         # Black
    (255, 0, 0): '01',       # Red
    (0, 255, 0): '10',       # Green
    (0, 0, 255): '11'        # Blue
}

def image_to_text(image_path):
    # Open the image
    img = Image.open(image_path)
    binary_data = ''

    # Read each pixel and convert to binary
    for y in range(64):
        for x in range(64):
            color = img.getpixel((x, y))
            binary_data += REVERSE_COLOR_MAPPING.get(color, '00')  # Default to '00' if color not recognized

    # Convert binary data to text (8 bits per character)
    text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        char = chr(int(byte, 2))
        if char == '\x00':
            break  # Stop at padding
        text += char

    return text

file_to_decode = input("Enter file name: ")
decoded_text = image_to_text(file_to_decode)
print(f"Decoded text: {decoded_text}")

from PIL import Image

# Reverse color mapping
REVERSE_COLOR_MAPPING = {
    (0, 0, 0): '0000',          # Black
    (128, 0, 0): '0001',        # Dark Red
    (0, 128, 0): '0010',        # Dark Green
    (0, 0, 128): '0011',        # Dark Blue
    (128, 128, 0): '0100',      # Dark Yellow
    (128, 0, 128): '0101',      # Dark Magenta
    (0, 128, 128): '0110',      # Dark Cyan
    (64, 64, 64): '0111',       # Dark Gray
    (192, 192, 192): '1000',    # Light Gray
    (255, 0, 0): '1001',        # Red
    (0, 255, 0): '1010',        # Green
    (0, 0, 255): '1011',        # Blue
    (255, 255, 0): '1100',      # Yellow
    (255, 0, 255): '1101',      # Magenta
    (0, 255, 255): '1110',      # Cyan
    (255, 255, 255): '1111'     # White
}

def image_to_text(image_path):
    # Open the image
    img = Image.open(image_path)
    binary_data = ''

    # Read each pixel and convert to binary
    for y in range(64):
        for x in range(64):
            color = img.getpixel((x, y))
            binary_data += REVERSE_COLOR_MAPPING.get(color, '0000')  # Default to '0000' if color not recognized

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

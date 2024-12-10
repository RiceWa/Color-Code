from PIL import Image

def image_to_text(image_path):
    # Open the image
    img = Image.open(image_path)
    binary_data = ''

    # Read each pixel and convert each RGB component to an 8-bit binary string
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary_data += f"{r:08b}{g:08b}{b:08b}"

    # Convert binary data to text (8 bits per character, 24 bits per 3 characters)
    text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            char = chr(int(byte, 2))
            text += char

    # Remove padding (e.g., zero-width spaces) at the end if present
    text = text.rstrip('\u200B')
    return text

# Prompt for input and decode the image
file_to_decode = input("Enter file name: ")
decoded_text = image_to_text(file_to_decode)
print(f"Decoded text: {decoded_text}")

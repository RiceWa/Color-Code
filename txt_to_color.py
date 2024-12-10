from PIL import Image

def pad_text(text):
    # Ensure the length of the text is a multiple of 3 by padding with zero-width spaces
    while len(text) % 3 != 0:
        text += '\u200B'  # Zero-width space character
    return text

def text_to_rgb_chunks(text):
    # Split the text into chunks of 3 characters each
    chunks = [text[i:i+3] for i in range(0, len(text), 3)]
    rgb_values = []

    for chunk in chunks:
        # Convert each character to its 8-bit binary representation
        binary_data = ''.join(format(ord(char), '08b') for char in chunk)
        
        # Extract the Red, Green, and Blue values (8 bits each)
        r = int(binary_data[0:8], 2)
        g = int(binary_data[8:16], 2)
        b = int(binary_data[16:24], 2)

        rgb_values.append((r, g, b))

    return rgb_values

def create_image_from_text(text, output_path):
    # Pad the text so its length is a multiple of 3
    padded_text = pad_text(text)
    rgb_values = text_to_rgb_chunks(padded_text)

    # Determine the image dimensions (64x64 for simplicity)
    img_size = 64
    img = Image.new('RGB', (img_size, img_size))

    # Set pixels based on RGB values
    for i, (r, g, b) in enumerate(rgb_values):
        x = i % img_size
        y = i // img_size
        if y < img_size:
            img.putpixel((x, y), (r, g, b))

    # Save the image
    img.save(output_path)
    print(f"Image saved to {output_path}")

# Conversion
text = input("Enter text to convert: ")
file_name = input("Enter a file name: ")
create_image_from_text(text, f"{file_name}.png")

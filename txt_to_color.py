import math
import argparse
from PIL import Image

HEADER_MAGIC = b"CC"      # Magic marker for identifying encoded images
HEADER_PIXELS = 2         # Two pixels (6 bytes) reserved for header

def build_header(byte_len):
    # Create a 6-byte header: "CC" + 4-byte big-endian payload length
    return HEADER_MAGIC + byte_len.to_bytes(4, "big")

def pack_bytes_to_pixels(data):
    # Convert raw bytes into RGB pixel tuples (3 bytes per pixel)
    pixels = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        r = chunk[0] if len(chunk) > 0 else 0
        g = chunk[1] if len(chunk) > 1 else 0
        b = chunk[2] if len(chunk) > 2 else 0
        pixels.append((r, g, b))
    return pixels

def create_image_from_text(text, output_path):
    # Encode text as UTF-8 bytes
    payload = text.encode("utf-8")

    # Create header pixels (6 bytes → 2 pixels)
    header_bytes = build_header(len(payload))
    header_pixels = [
        (header_bytes[0], header_bytes[1], header_bytes[2]),
        (header_bytes[3], header_bytes[4], header_bytes[5])
    ]

    # Pack payload bytes into pixels
    data_pixels = pack_bytes_to_pixels(payload)

    # Calculate smallest square image that fits everything
    total_pixels = HEADER_PIXELS + len(data_pixels)
    side = math.ceil(math.sqrt(total_pixels))
    img = Image.new("RGB", (side, side), (0, 0, 0))

    # Write header + data pixels row by row
    all_pixels = header_pixels + data_pixels
    for i, (r, g, b) in enumerate(all_pixels):
        x = i % side
        y = i // side
        img.putpixel((x, y), (r, g, b))

    # Save the image
    img.save(output_path)
    print(f"Image saved to {output_path} ({side}x{side})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_text", help="Text to encode")
    parser.add_argument("--out", dest="output_path", required=True, help="Output PNG file")
    args = parser.parse_args()

    # If no --in given, ask the user
    text = args.input_text if args.input_text else input("Enter text to convert: ")
    create_image_from_text(text, args.output_path)

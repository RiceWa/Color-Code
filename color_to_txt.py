import argparse
from PIL import Image

HEADER_MAGIC = b"CC"
HEADER_PIXELS = 2  # Two pixels = 6 bytes

def read_header(img):
    # Read first 2 pixels (6 bytes total)
    p0 = img.getpixel((0, 0))
    p1 = img.getpixel((1, 0))
    header = bytes([p0[0], p0[1], p0[2], p1[0], p1[1], p1[2]])

    # If header starts with "CC", parse length
    if header[:2] == HEADER_MAGIC:
        length = int.from_bytes(header[2:6], "big")
        return length, True
    return 0, False

def extract_bytes(img, start_pixel_idx, num_bytes):
    # Extract exactly num_bytes from pixels starting at index
    data = bytearray()
    w, h = img.width, img.height
    idx = start_pixel_idx
    while len(data) < num_bytes and idx < w * h:
        x = idx % w
        y = idx // w
        r, g, b = img.getpixel((x, y))
        for comp in (r, g, b):
            if len(data) < num_bytes:
                data.append(comp)
        idx += 1
    return bytes(data)

def legacy_decode(img):
    # Fallback: read all pixels and try to decode (for old images)
    raw = bytearray()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            raw.extend([r, g, b])
    return bytes(raw).rstrip(b"\x00").decode("utf-8", errors="ignore").rstrip("\u200B")

def image_to_text(path):
    # Open the image and check for header
    img = Image.open(path).convert("RGB")
    length, has_header = read_header(img)

    if has_header:
        # Modern decode: read exactly "length" bytes
        data = extract_bytes(img, HEADER_PIXELS, length)
        return data.decode("utf-8")
    else:
        # Old decode: read whole image
        return legacy_decode(img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", required=True, help="Input PNG file")
    parser.add_argument("--out", dest="output_path", help="Optional output text file")
    args = parser.parse_args()

    text = image_to_text(args.input_path)

    # Save to file if requested, else print
    if args.output_path:
        with open(args.output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text written to {args.output_path}")
    else:
        print(text)

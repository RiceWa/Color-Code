# color_codec.py
import math
from PIL import Image

HEADER_MAGIC = b"CC"
HEADER_PIXELS = 2

def build_header(byte_len):
    # Build a 6-byte header: "CC" + 4-byte big-endian length
    return HEADER_MAGIC + byte_len.to_bytes(4, "big")

def pack_bytes_to_pixels(data):
    # Convert bytes into list of RGB tuples
    pixels = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        r = chunk[0] if len(chunk) > 0 else 0
        g = chunk[1] if len(chunk) > 1 else 0
        b = chunk[2] if len(chunk) > 2 else 0
        pixels.append((r, g, b))
    return pixels

def create_image_from_text(text):
    # Encode text as UTF-8
    payload = text.encode("utf-8")
    header = build_header(len(payload))

    # Convert header to two pixels
    header_pixels = [
        (header[0], header[1], header[2]),
        (header[3], header[4], header[5])
    ]
    data_pixels = pack_bytes_to_pixels(payload)

    total_pixels = HEADER_PIXELS + len(data_pixels)
    side = math.ceil(math.sqrt(total_pixels))
    img = Image.new("RGB", (side, side), (0, 0, 0))

    all_pixels = header_pixels + data_pixels
    for i, (r, g, b) in enumerate(all_pixels):
        x = i % side
        y = i // side
        img.putpixel((x, y), (r, g, b))

    return img

def read_header(img):
    # Try to read first two pixels as header
    if img.width < 2:
        return 0, False
    p0 = img.getpixel((0, 0))
    p1 = img.getpixel((1, 0))
    header = bytes([p0[0], p0[1], p0[2], p1[0], p1[1], p1[2]])
    if header[:2] == HEADER_MAGIC:
        length = int.from_bytes(header[2:6], "big")
        return length, True
    return 0, False

def extract_bytes(img, start_pixel_idx, num_bytes):
    # Extract exactly num_bytes from pixels
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
    # Read all pixels and try best-effort decode
    raw = bytearray()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            raw.extend([r, g, b])
    return bytes(raw).rstrip(b"\x00").decode("utf-8", errors="ignore").rstrip("\u200B")

def image_to_text(file_like):
    # Decode PNG from a file-like object or path
    img = Image.open(file_like).convert("RGB")
    length, has_header = read_header(img)
    if has_header:
        data = extract_bytes(img, HEADER_PIXELS, length)
        return data.decode("utf-8")
    return legacy_decode(img)

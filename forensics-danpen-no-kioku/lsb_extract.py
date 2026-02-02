import os
from PIL import Image

def extract_lsb(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)
            
    # Convert bits to bytes
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            bytes_data.append(int(byte, 2))
            
    return bytes_data

images = [
    "extracted/image1.png",
    "extracted/image2.png",
    "extracted/image3.png",
    "extracted/image4.png",
    "extracted/image5.png",
    "extracted/recovered_png_1.png"
]

for img_path in sorted(images):
    if os.path.exists(img_path):
        print(f"--- {img_path} ---")
        data = extract_lsb(img_path)
        # Look for printable strings
        import re
        printable = "".join([chr(b) if 32 <= b <= 126 else "." for b in data])
        # Find parts that look like fragments (e.g., flag content)
        matches = re.findall(r'[a-zA-Z0-9_{}-]{4,}', printable)
        if matches:
            print("Matches:", matches[:5])
        else:
            print("No simple printable matches found in first LSB pass.")

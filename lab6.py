

from PIL import Image
from collections import Counter
import os

# AES-ECB Image Reconstruction
# Based on the ECB Penguin technique

# read encrypted file
with open("aes.bmp.enc", "rb") as file:
    data = file.read()

# 16-byte AES blocks
blocks = []

for i in range(0, len(data) - 15, 16):
    blocks.append(data[i:i+16])

# repeated blocks
counts = Counter(blocks)

print("Total blocks:", len(blocks))
print("Unique blocks:", len(counts))

# which block shows up the most
most_common = counts.most_common(1)[0][0]

# blocks to black and white
visual_data = bytearray()

for block in blocks:
    if block == most_common:
        colour = 255  # White
    else:
        colour = 0    # Black

    visual_data.extend([colour] * 16)

# output folder
output_folder = "reconstructed_images"
os.makedirs(output_folder, exist_ok=True)

# test diff image widths
widths = [320, 480, 640, 800, 1024, 1280, 2560]

for width in widths:

    # calculate image height
    height = len(visual_data) // (width * 3)

    required_bytes = width * height * 3
    pixels = bytes(visual_data[:required_bytes])

    # reconstruct image
    image = Image.frombytes(
        "RGB",
        (width, height),
        pixels
    )

    # flip vertically to correct BMP orientation (originally was upside down so I updated this)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    filename = f"recovered_{width}.png"
    image.save(os.path.join(output_folder, filename))

    print("Created:", filename)

print("Finished! Created 5 images.")

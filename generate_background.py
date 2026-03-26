import numpy as np
from PIL import Image, ImageDraw
import random

# Image dimensions
width, height = 1920, 1080

# Create a new image with dark background
img = Image.new('RGB', (width, height), color=(10, 10, 20))
draw = ImageDraw.Draw(img, 'RGBA')

# Create neon grid effect
line_color_cyan = (0, 255, 255, 200)
line_color_magenta = (255, 0, 255, 200)

# Draw horizontal and vertical lines with neon effect
for i in range(0, width, 80):
    # Vertical lines
    if random.random() > 0.3:
        color = line_color_cyan if random.random() > 0.5 else line_color_magenta
        draw.line([(i, 0), (i + 200, height)], fill=color, width=2)

for i in range(0, height, 80):
    # Horizontal lines
    if random.random() > 0.3:
        color = line_color_cyan if random.random() > 0.5 else line_color_magenta
        draw.line([(0, i), (width, i + 200)], fill=color, width=2)

# Add some glowing dots
for _ in range(300):
    x = random.randint(0, width)
    y = random.randint(0, height)
    radius = random.randint(1, 4)
    color = line_color_cyan if random.random() > 0.5 else line_color_magenta
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

# Save the image
img.save('static/images/cyber_background.png')
print("Background image generated successfully!")

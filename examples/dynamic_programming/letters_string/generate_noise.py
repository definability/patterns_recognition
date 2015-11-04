from PIL import Image, ImageDraw
from random import gauss

def generate_noise(width, height, mu=255.0/2, sigma=255.0/2):
    noise = Image.new('RGBA', (width, height), 'black')
    draw = ImageDraw.Draw(noise)
    for i in range(width):
        for j in range(height):
            draw.point((i,j), fill=(0, 0, 0, int(gauss(mu, sigma))))
    return noise

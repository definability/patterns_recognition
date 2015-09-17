from sys import argv

from generate_message import generate_message
from draw_message import draw_message
from generate_noise import generate_noise

from PIL import Image, ImageDraw

EPSILON = 1E-6

if __name__ == '__main__':

    count = int(argv[1])
    letters = map(lambda x: x[0], argv[2::2])
    probabilities = map(float, argv[3::2])

    if (abs(1 - sum(probabilities)) > EPSILON):
        raise ValueError('Sum of probabilities should be equal 1')

    image = draw_message(generate_message(letters, probabilities, count), 50)
    noise = generate_noise(image.getbbox()[2], image.getbbox()[3])

    image.paste(noise, mask=noise)
    image.save('out.png')

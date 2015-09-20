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

    letters = draw_message(generate_message(letters, probabilities, count), 50)
    width, height = letters.getbbox()[2], letters.getbbox()[3]
    noise = generate_noise(width, height)

    letters.paste(Image.new('RGB', (width, height), 'black'), mask=noise)
    image = Image.new('RGB', (width, height), 'white')
    image.paste(Image.new('RGB', (width, height), 'black'), mask=letters)
    image.save('out.png')

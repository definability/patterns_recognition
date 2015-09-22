from sys import argv

from get_characters import get_characters
from generate_message import generate_message
from draw_message import draw_message
from generate_noise import generate_noise
from Recognizer import Recognizer, get_penalty

from PIL import Image, ImageDraw

EPSILON = 1E-6
FONT_SIZE = 14

if __name__ == '__main__':

    count = int(argv[1])
    letters = map(lambda x: x[0], argv[2::2])
    probabilities = map(float, argv[3::2])

    if [p for p in probabilities if p < 0]:
        raise ValueError('Probabilities can not be negative')
    elif abs(1 - sum(probabilities)) > EPSILON and ' ' in letters:
        raise ValueError('Sum of probabilities should be equal to 1')
    elif ' ' not in letters:
        letters.append(' ')
        probabilities.append(1 - sum(probabilities))

    characters = get_characters(letters, FONT_SIZE)
    message = generate_message(letters, probabilities, count)
    text = draw_message(message, characters)
    width, height = text.size[0], text.size[1]
    noise = generate_noise(width, height, 0, 555)

    text.paste(Image.new('RGB', (width, height), 'black'), mask=noise)
    image = Image.new('RGB', (width, height), 'white')
    image.paste(Image.new('LA', (width, height), 'black'), mask=text)

    recognizer = Recognizer(characters, image)
    domains, result = recognizer.calculate(lambda x, y: min(x, y), lambda x, y: x+y, float('inf'), 0)
    recognized = recognizer.find_path(domains)
    print ''.join(recognized)
    print ''.join(message)
    print 1.0*sum([1 for r, m in zip(recognized, message) if r != m])/count
    #print sum(get_penalty(characters[recognized[i]], characters[message[i]]) for i in range(len(message)) if recognized[i] != message[i])

    image.save('out.png')

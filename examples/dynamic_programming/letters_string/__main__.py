from sys import argv, float_info
from math import log

from get_characters import get_characters
from generate_message import generate_message
from draw_message import draw_message
from generate_noise import generate_noise
from build_problem import build_problem
from classes.image import *
from classes.semiring import *

from PIL import Image, ImageDraw

EPSILON = float_info.epsilon
FONT_SIZE = 14
SIGMA = 255


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_penalty(image, pattern, probability):
    if probability < EPSILON:
        return float('inf')
    result = 0
    for xv, kv in zip(image, pattern):
        for x, k in zip(xv, kv):
            result += (x-k)**2
    return result - log(probability) * 2 * (SIGMA**2)


if __name__ == '__main__':

    count = int(argv[1])
    letters = map(lambda x: x[0], argv[2::2])
    probabilities = map(float, argv[3::2])

    if [p for p in probabilities if p < 0]:
        raise ValueError('Probabilities can not be negative')
    elif 1 - sum(probabilities) > EPSILON and ' ' in letters:
        raise ValueError('Sum of probabilities should be equal to 1')
    elif sum(probabilities) - 1 > EPSILON:
        raise ValueError('Sum of probabilities should be equal to 1')
    elif ' ' not in letters:
        letters.append(' ')
        probabilities.append(1 - sum(probabilities))

    characters = get_characters(letters, FONT_SIZE)
    message = generate_message(letters, probabilities, count)
    text = draw_message(message, characters)
    width, height = text.size[0], text.size[1]
    mp_orig = MatrixPointer(list(text.convert('L').getdata()), (text.size[0], text.size[1]))
    noise = generate_noise(width, height, 0, SIGMA)

    text.paste(Image.new('RGB', (width, height), 'black'), mask=noise)
    image = Image.new('RGB', (width, height), 'white')
    image.paste(Image.new('LA', (width, height), 'black'), mask=text)

    gc_characters = {}
    for c in characters:
        gc_characters[c] = characters[c].convert('L')

    image = image.convert('L')
    print 'Get vertices and edges'

    problem = build_problem(image, gc_characters)
    print 'Solve'
    solution = problem.solve(SemiringArgminPlusElement)
    print '"'+''.join(solution.value[1])+'"'
    mp_img = MatrixPointer(list(image.getdata()), (image.size[0], image.size[1]))
    diff = mp_img.reduce(lambda accumulator, x, y: accumulator + (x - y)**2, 0, mp_orig) - solution.value[0]
    print 'Solution is better than original on', diff, '(negative number is bad)'

    #recognizer = Recognizer(image, characters, dict(zip(letters, probabilities)))

    #domains, result = recognizer.calculate(lambda x, y: min(x, y), lambda x, y: x+y, float('inf'), 0, get_penalty)
    #recognized = recognizer.find_path(domains)

    #print 'ORIGINAL'
    #print ''.join(message)
    #print 'Simple'
    #print ''.join([('' if m == r else bcolors.FAIL) + r + bcolors.ENDC for m, r in zip(message, recognized)])
    #print 1.0*sum([1 for r, m in zip(recognized, message) if r != m])/count

    image.save('out.png')


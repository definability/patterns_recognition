from Texture import Texture
from os.path import join as pjoin, dirname

from PIL import Image


if __name__ == '__main__':
    texture = Texture(2, 2, 2)
    image = Image.open(pjoin(dirname(__file__), 'stripes.png')).convert('L')
    mask = Image.open(pjoin(dirname(__file__), 'mask.png'))
    width, height = image.size

    data = list(image.getdata())
    mask_data = list(mask.getdata())
    for x in xrange(height-1):
        for y in xrange(width-1):
            cur = data[x*width+y]
            cur = 0 if cur == 0 else 1

            params = {}

            r = data[x*width+(y+1)]
            r = 0 if r == 0 else 1
            params[0] = (cur, r)

            b = data[(x+1)*width+y]
            b = 0 if b == 0 else 1
            params[1] = (cur, b)

            current_class = 0 if mask_data[x*width+y][0] == 255 else 1
            texture.pick_texture_sample(params, current_class)

    test_image = Image.open(pjoin(dirname(__file__), 'test.png')).convert('L')
    test_width, test_height = test_image.size
    test_data = list(test_image.getdata())
    results = []
    for x in xrange(test_height):
        row = []
        for y in xrange(test_width):
            cur = test_data[x*test_width+y]
            cur = 0 if cur == 0 else 1

            params = {}
            if y < test_width-1:
                r = test_data[x*test_width+(y+1)]
                r = 0 if r == 0 else 1
                params[0] = (cur, r)
            if x < test_height-1:
                b = test_data[(x+1)*test_width+y]
                b = 0 if b == 0 else 1
                params[1] = (cur, b)

            t = texture.recognize_texture(params)
            row.append(t)
        results += row

    results = [((200, 50, 50) if r == 0 else (50, 50, 200)) for r in results]
    result = Image.new('RGB', test_image.size)
    result.putdata(results)
    result.save(pjoin(dirname(__file__), 'result.png'))


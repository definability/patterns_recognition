from Texture import Texture
from os.path import join as pjoin, dirname


from PIL import Image


if __name__ == '__main__':
    texture = Texture(2, 2, 2)
    image = Image.open(pjoin(dirname(__file__), 'stripes.png')).convert('L')
    width, height = image.size

    texture.pick_texture_sample({
        0: (0, 1),
        1: (0, 0)
    }, 0)
    texture.pick_texture_sample({
        0: (1, 0),
        1: (1, 1)
    }, 0)
    texture.pick_texture_sample({
        0: (0, 0),
        1: (0, 0)
    }, 0)

    texture.pick_texture_sample({
        1: (0, 1),
        0: (0, 0)
    }, 1)
    texture.pick_texture_sample({
        1: (1, 0),
        0: (1, 1)
    }, 1)

    data = list(image.getdata())
    results = []
    for x in xrange(width):
        row = []
        for y in xrange(height):
            cur = data[x*width+y]
            cur = 0 if cur == 0 else 1

            params = {}
            if y < width-1:
                r = data[x*width+(y+1)]
                r = 0 if r == 0 else 1
                params[0] = (cur, r)
            if x < height-1:
                b = data[(x+1)*width+y]
                b = 0 if b == 0 else 1
                params[1] = (cur, b)

            t = texture.recognize_texture(params)
            row.append(t)
        results += row

    results = [((200, 50, 50) if r == 0 else (50, 50, 200)) for r in results]
    result = Image.new('RGB', image.size)
    result.putdata(results)
    for x in xrange(width):
        print results[x*height:(x+1)*height]
    result.save(pjoin(dirname(__file__), 'result.png'))


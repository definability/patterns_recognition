from os import path

from build_problem import build_problem

from PIL import Image, ImageDraw


if __name__ == '__main__':
    model_image = Image.open(path.join(path.dirname(__file__), 'rect_model.png'))
    model_image_mask = [p[3] > 0 for p in list(model_image.getdata())]
    model_image_grayscale = model_image.convert('L')

    raw_image = Image.open(path.join(path.dirname(__file__), 'rect_raw.png'))
    raw_image_grayscale = raw_image.convert('L')

    build_problem(model_image_grayscale, raw_image_grayscale, model_image_mask)


from PIL import Image, ImageDraw, ImageFont

def get_characters(characters, size):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size)
    images = {}
    space_height = 0
    for c in characters:
        width, height = font.getsize(c)
        if height > space_height:
            space_height = height
        o_width, o_height = font.getoffset(c)
        image = Image.new('RGBA', (width, height), (255,255,255,0))
        draw = ImageDraw.Draw(image)
        draw.text((-o_width, -o_height), c, 'black', font=font)
        if c == ' ':
            images[' '] = Image.new('RGBA', (size/2, space_height), (255,255,255,0))
        else:
            images[c] = image.crop(image.getbbox())
    return images

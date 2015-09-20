from PIL import Image, ImageDraw, ImageFont

def draw_message(message, size):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size)
    width, height = font.getsize(message)
    o_width, o_height = font.getoffset(message)

    image = Image.new('RGBA', (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((-o_width, -o_height), message, 'black', font=font)

    return image.crop(image.getbbox())

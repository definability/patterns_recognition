from PIL import Image, ImageDraw, ImageFont

def draw_message(message, size):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size)
    image = Image.new('RGBA', font.getsize(message), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), message, 'black', font=font)
    del draw
    return image

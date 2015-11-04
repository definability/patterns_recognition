from PIL import Image, ImageDraw, ImageFont

def draw_message(message, characters):
    images = [characters[c] for c in message]

    width  = sum(character.size[0] for character in images)
    height = max(character.size[1] for character in images)

    image = Image.new('RGBA', (width, height), (0,0,0,0))
    horizontal_offset = 0
    for character in images:
        image.paste(character, (horizontal_offset, 0))
        horizontal_offset += character.size[0]

    return image

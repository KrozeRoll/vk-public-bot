from PIL import ImageFont, ImageDraw


def make_great_cover(image, str):
    font_size = 30
    font = ImageFont.truetype("/home/KrozeRoll/mysite/wrift.ttf", font_size)
    text_size = font.getsize(str)

    draw = ImageDraw.Draw(image)

    h = image.size[1]
    w = image.size[0]

    draw.text(((w - text_size[0]) / 2, h - text_size[1] - 10), str,
              font=font, fill="white")
    return image

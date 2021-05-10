from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def is_vowel(ch):
    return ch in ('А', 'О', 'У', 'Э', 'Ы', 'Я', 'Ё', 'Ю', 'Е', 'И')


def make_result_string(str):
    str = str.upper()
    if str.find('-ХУ') == -1 and str.find('- ХУ') == -1:
        pk = 0
        while pk < len(str) and is_vowel(str[pk]) == 0:
            pk = pk + 1

        if pk == len(str):
            pk = 0

        if str[pk:][0] == "Е" or str[pk:][0] == "Э":
            str = str + " - ХУЕ" + str[pk + 1:]
        elif str[pk:][0] == "У" or str[pk:][0] == "Ю":
            str = str + " - ХУЮ" + str[pk + 1:]
        elif str[pk:][0] == "А" or str[pk:][0] == "Я":
            str = str + " - ХУЯ" + str[pk + 1:]
        elif str[pk:][0] == "И" or str[pk:][0] == "Ы":
            str = str + " - ХУИ" + str[pk + 1:]
        elif str[pk:][0] == "О" or str[pk:][0] == "Ё":
            str = str + " - ХУЁ" + str[pk + 1:]
        else:
            str = str + " - ХУЕ" + str[pk:]

    return str


def make_normal_size(image):
    w = image.size[0]
    h = image.size[1]

    kf = 1024 / w
    if kf < 768 / h:
        kf = 768 / h

    image = image.resize((int(w * kf), int(h * kf)))

    w = image.size[0]
    h = image.size[1]

    if h > 768:
        area = (0, int((h - 768) / 2), w, int((h - 768) / 2) + 768)
        image = image.crop(area)
    elif w > 1024:
        area = (int((w - 1024) / 2), 0, int((w - 1024) / 2) + 1024, h)
        image = image.crop(area)
    return image


def bright(source):
    enhancer = ImageEnhance.Brightness(source)

    factor = 0.5
    result = enhancer.enhance(factor)

    return result


def make_result_image(image, str):
    w = image.size[0]
    h = image.size[1]

    if w * h > 1024 * 768:
        image = make_normal_size(image)
        image = bright(image)
    else:
        image = bright(image)
        image = make_normal_size(image)

    h = 768
    w = 1024

    draw = ImageDraw.Draw(image)
    str = make_result_string(str)

    font_size = 72
    font = ImageFont.truetype("/home/KrozeRoll/mysite/wrift.ttf", font_size)
    text_size = font.getsize(str)

    while text_size[0] > w - 10:
        font_size = font_size - 1
        font = ImageFont.truetype("/home/KrozeRoll/mysite/wrift.ttf", font_size)
        text_size = font.getsize(str)

    draw.text(((w - text_size[0]) / 2, (h - text_size[1]) / 2 - 30), str, font=font, fill="white")
    return image

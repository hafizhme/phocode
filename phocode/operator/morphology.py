from PIL import Image

import math as mt


def dilation(original_image: Image):
    def operation(s, val):
        if val == 255:
            val = 1
        return s ^ val

    def summarize(acc):
        res = 0
        for a in acc:
            res = res or a
        if res == 1:
            return 255
        return 0

    original_image = original_image.convert(mode='1')
    resulted_image = Image.new(
        mode='1',
        size=original_image.size,
    )

    S = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]

    s_size = len(S)
    s_half = mt.floor(s_size / 2)

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            acc = []
            counting = 0
            for k_x, n_x in enumerate(range(x - s_half, x + s_half + 1)):
                neigboor_pixels = None
                for k_y, n_y in enumerate(range(y - s_half, y + s_half + 1)):
                    try:
                        neigboor_pixels = original_image.getpixel((n_x, n_y))
                    except IndexError:
                        neigboor_pixels = 0
                counting += 1

                acc.append(operation(S[k_x][k_y], neigboor_pixels))

            res = summarize(acc)
            resulted_image.putpixel(
                xy=(x, y),
                value=res
            )

    return resulted_image, None


def erosion(original_image: Image):
    def operation(s, val):
        if val == 255:
            val = 1
        return s and val

    def summarize(acc):
        res = 0
        for a in acc:
            res = res and a
        if res == 1:
            return 255
        return 0

    original_image = original_image.convert(mode='1')
    resulted_image = Image.new(
        mode='1',
        size=original_image.size,
    )

    S = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]

    s_size = len(S)
    s_half = mt.floor(s_size / 2)

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            acc = []
            counting = 0
            for k_x, n_x in enumerate(range(x - s_half, x + s_half + 1)):
                neigboor_pixels = None
                for k_y, n_y in enumerate(range(y - s_half, y + s_half + 1)):
                    try:
                        neigboor_pixels = original_image.getpixel((n_x, n_y))
                    except IndexError:
                        neigboor_pixels = 0
                counting += 1

                acc.append(operation(S[k_x][k_y], neigboor_pixels))

            resulted_image.putpixel(
                xy=(x, y),
                value=summarize(acc)
            )

    return resulted_image, None

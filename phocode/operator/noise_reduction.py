from PIL import Image
# == MAPPING USED ==
#      ~ ~ * ~ ~
#      ~ * * * ~
#      * * # * *
#      ~ * * * ~
#      ~ ~ * ~ ~
# ==================


def get_pixel(img: Image, pos):
    try:
        return img.getpixel((pos))
    except IndexError:
        return (0, 0, 0)


def mean(img: Image, pos):
    r, g, b = 0, 0, 0
    for i, x in enumerate(range(pos[0]-2, pos[0]+3)):
        for j, y in enumerate(range(pos[1]-2, pos[1]+3)):
            if (i == 0 and j == 2) \
                    or (i == 1 and j > 0 and j < 4) \
                    or (i == 2) \
                    or (i == 3 and j > 0 and j < 4) \
                    or (i == 4 and j == 2):
                px = get_pixel(img, (x, y))
                r += px[0]
                g += px[1]
                b += px[2]

    return r // 13, g // 13, b // 13


def modus(img: Image, pos):
    def add_or_init_to_dict(dictionary, key):
        try:
            dictionary[key] += 1
        except KeyError:
            dictionary[key] = 0

    def highest(dictionary):
        highest = 0
        key_h = None
        for key in dictionary:
            if dictionary[key] >= highest:
                key_h = key
                highest = dictionary[key_h]
        return key_h

    r, g, b = {}, {}, {}
    for i, x in enumerate(range(pos[0]-2, pos[0]+3)):
        for j, y in enumerate(range(pos[1]-2, pos[1]+3)):
            if (i == 0 and j == 2) \
                    or (i == 1 and j > 0 and j < 4) \
                    or (i == 2) \
                    or (i == 3 and j > 0 and j < 4) \
                    or (i == 4 and j == 2):
                px = get_pixel(img, (x, y))
                add_or_init_to_dict(r, px[0])
                add_or_init_to_dict(g, px[1])
                add_or_init_to_dict(b, px[2])

    return highest(r), highest(g), highest(b)


def median(img: Image, pos):
    def put_to_list(lis, element):
        x = 0
        while x < len(lis) and lis[x] < element:
            x += 1

        lis.insert(x, element)

    r, g, b = [], [], []
    for i, x in enumerate(range(pos[0]-2, pos[0]+3)):
        for j, y in enumerate(range(pos[1]-2, pos[1]+3)):
            if (i == 0 and j == 2) \
                    or (i == 1 and j > 0 and j < 4) \
                    or (i == 2) \
                    or (i == 3 and j > 0 and j < 4) \
                    or (i == 4 and j == 2):
                px = get_pixel(img, (x, y))
                put_to_list(r, px[0])
                put_to_list(g, px[1])
                put_to_list(b, px[2])

    return r[6], g[6], b[6]  # from 13 elements


def do(original_image: Image, method):
    size = (
        original_image.size[0],
        original_image.size[1]
    )
    resulted_image = Image.new(
        mode=original_image.mode,
        size=size,
        color=(256, 256, 256)
    )

    if method == 'mean':
        function = mean
    elif method == 'median':
        function = median
    else:
        function = modus

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            resulted_image.putpixel(
                xy=(x, y),
                value=function(original_image, (x, y))
            )

    return resulted_image, None

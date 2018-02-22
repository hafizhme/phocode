from PIL import Image


def do(original_image: Image, factor):
    resulted_image = Image.new(
        mode=original_image.mode,
        size=original_image.size,
        color=(256, 256, 256)
    )

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            pixels = original_image.getpixel((x, y))
            new_pixels = []
            for p in pixels:
                new_pixels.append(mul_max(p, factor))

            resulted_image.putpixel(
                xy=(x, y),
                value=tuple(new_pixels)
            )

    return resulted_image, None


def mul_max(a, b):
    ret = int(a * b)
    if ret >= 255:
        ret = 255
    return ret

from PIL import Image

import math as mt

# https://en.wikipedia.org/wiki/Kernel_(image_processing)


def convolve(original_image: Image, kernel, factor=1):
    def raise_or_lower(val):
        if factor == 1:
            if val > 255:
                return 255
            elif val < 0:
                return 0
            return val
        else:
            val = int(val * factor)
            if val > 255:
                return 255
            return val

    ker_size = len(kernel)
    ker_half = mt.floor(ker_size / 2)

    resulted_image = Image.new(
        mode=original_image.mode,
        size=original_image.size,
        color=(256, 256, 256)
    )

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            acc_r = 0
            acc_g = 0
            acc_b = 0
            counting = 0
            for k_x, n_x in enumerate(range(x - ker_half, x + ker_half + 1)):
                neigboor_pixels = None
                for k_y, n_y in enumerate(range(y - ker_half, y + ker_half + 1)):
                    try:
                        neigboor_pixels = original_image.getpixel((n_x, n_y))
                    except IndexError:
                        neigboor_pixels = (0, 0, 0)
                counting += 1

                acc_r += kernel[k_x][k_y] * neigboor_pixels[0]
                acc_g += kernel[k_x][k_y] * neigboor_pixels[1]
                acc_b += kernel[k_x][k_y] * neigboor_pixels[2]

            resulted_image.putpixel(
                xy=(x, y),
                value=(
                    raise_or_lower(acc_r),
                    raise_or_lower(acc_g),
                    raise_or_lower(acc_b),
                )
            )

    return resulted_image, None


def edge_detection(original_image: Image):
    return convolve(original_image, [
        [ 0,  1,  0],
        [ 1, -4,  1],
        [ 0,  1,  0],
    ])


def sharpen(original_image: Image):
    return convolve(original_image, [
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ])


def gaussian_blur_3(original_image: Image):
    return convolve(original_image, [
        [ 1,  2,  1],
        [ 2,  4,  2],
        [ 1,  2,  1],
    ], factor=1/16)

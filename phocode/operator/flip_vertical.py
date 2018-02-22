from PIL import Image


def do(original_image: Image):
    resulted_image = Image.new(
        mode=original_image.mode,
        size=original_image.size,
        color=(256, 256, 256)
    )

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            original_xy = (x, y)
            resulted_xy = (x, original_image.size[1] - y - 1)

            resulted_image.putpixel(
                xy=resulted_xy,
                value=original_image.getpixel(original_xy)
            )

    return resulted_image, None

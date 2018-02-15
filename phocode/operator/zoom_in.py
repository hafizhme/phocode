from PIL import Image


def do(original_image: Image):
    image_matrix = original_image.load()
    resulted_image = Image.new(
        mode=original_image.mode,
        size=(original_image.size[0] * 2, original_image.size[1] * 2),
        color=(256, 256, 256)
        )

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            value = image_matrix[x, y]

            resulted_image.putpixel(
                xy=(
                    2 * x,
                    2 * y
                    ),
                value=value
                )

            resulted_image.putpixel(
                xy=(
                    2 * x,
                    2 * y + 1
                    ),
                value=value
                )

            resulted_image.putpixel(
                xy=(
                    2 * x + 1,
                    2 * y
                    ),
                value=value
                )

            resulted_image.putpixel(
                xy=(
                    2 * x + 1,
                    2 * y + 1
                    ),
                value=value
                )

    return resulted_image, None

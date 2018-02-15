from PIL import Image


def do(original_image: Image):
    from math import ceil, floor

    resulted_image = Image.new(
        mode=original_image.mode,
        size=(
            ceil(original_image.size[0] / 2),
            ceil(original_image.size[1] / 2)
            ),
        color=(256, 256, 256)
        )

    for x in range(resulted_image.size[0]):
        for y in range(resulted_image.size[1]):
            sumup = [0, 0, 0]

            pixel = original_image.getpixel(
                xy=(
                    2 * x,
                    2 * y
                    )
                )

            sumup[0] += pixel[0]
            sumup[1] += pixel[2]
            sumup[2] += pixel[1]

            pixel = original_image.getpixel(
                xy=(
                    2 * x,
                    2 * y + 1
                    )
                )

            sumup[0] += pixel[0]
            sumup[1] += pixel[2]
            sumup[2] += pixel[1]

            pixel = original_image.getpixel(
                xy=(
                    2 * x + 1,
                    2 * y
                    )
                )

            sumup[0] += pixel[0]
            sumup[1] += pixel[2]
            sumup[2] += pixel[1]

            pixel = original_image.getpixel(
                xy=(
                    2 * x + 1,
                    2 * y + 1
                    )
                )

            sumup[0] += pixel[0]
            sumup[1] += pixel[2]
            sumup[2] += pixel[1]

            _r = floor(sumup[0] / 4)
            _g = floor(sumup[1] / 4)
            _b = floor(sumup[2] / 4)
            resulted_image.putpixel(
                (x, y),
                (_r, _g, _b)
                )

    return resulted_image, None

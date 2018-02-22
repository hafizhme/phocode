from PIL import Image


def do(original_image: Image, fr, to):
    resulted_image = Image.new(
        mode=original_image.mode,
        size=(
            to[0] - fr[0],
            to[1] - fr[1]
        ),
        color=(256, 256, 256)
    )

    for x in range(resulted_image.size[0]):
        for y in range(resulted_image.size[1]):
            xy = (fr[0] + x, fr[1] + y)
            resulted_image.putpixel(
                xy=(x, y),
                value=original_image.getpixel(xy)
            )

    return resulted_image, None

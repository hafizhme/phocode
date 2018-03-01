from PIL import Image


def do(original_image: Image, degree):
    size = (
        original_image.size[0],
        original_image.size[1]
    )
    if degree == 90 or degree == 270:
        size = (
            original_image.size[1],
            original_image.size[0]
        )
    resulted_image = Image.new(
        mode=original_image.mode,
        size=size,
        color=(256, 256, 256)
    )

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            xy_res = (x, y)
            xy_ori = (x, y)
            if degree == 90:
                xy_res = (original_image.size[1] - y - 1, x)
                xy_ori = (x, y)
            elif degree == 180:
                xy_res = (x, original_image.size[1] - y - 1)
                xy_ori = (x, y)
            elif degree == 270:
                xy_res = (y, original_image.size[0] - x - 1)
                xy_ori = (x, y)

            resulted_image.putpixel(
                xy=xy_res,
                value=original_image.getpixel(xy_ori)
            )

            # dest_buffer [ c ] [ m - r - 1 ] = source_buffer [ r ] [ c ];

    return resulted_image, None

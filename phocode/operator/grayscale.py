from PIL import Image


def do(original_image: Image):
    image_matrix = original_image.load()
    resulted_image = Image.new("L", original_image.size)

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            xy = (x, y)
            value = (image_matrix[x, y][0] * 0.33) \
                + (image_matrix[x, y][1] * 0.33) \
                + (image_matrix[x, y][2] * 0.34)
            resulted_image.putpixel(xy, int(value))

    return resulted_image, None

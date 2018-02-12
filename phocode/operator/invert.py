from PIL import Image


def invert(original_image):
    _r, _g, _b = original_image.split()

    out_r = _r.point(lambda p: 255 - p)
    out_g = _g.point(lambda p: 255 - p)
    out_b = _b.point(lambda p: 255 - p)

    _r.paste(out_r)
    _g.paste(out_g)
    _b.paste(out_b)

    resulted_image = Image.merge(original_image.mode, (_r, _g, _b))

    return resulted_image, None

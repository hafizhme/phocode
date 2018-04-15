from PIL import Image


def seed_region_growth(im: Image, se: (int, int), th: int):
    def in_threshold(se: (int, int, int, int), cu: (int, int, int, int), th):
        return (se[0] - th <= cu[0] and cu[0] <= se[0] + th) \
            and (se[1] - th <= cu[1] and cu[1] <= se[1] + th) \
            and (se[2] - th <= cu[2] and cu[2] <= se[2] + th)
    im = im.convert('RGBA')
    co = [
        [
            False for y in range(im.size[1])
        ] for x in range(im.size[0])
    ]

    st = [se]
    cu = se
    while len(st) > 0:
        co[cu[0]][cu[1]] = True

        found = False
        ne = (cu[0], cu[1] + 1)
        if 0 <= ne[0] and ne[0] < im.size[0] and 0 <= ne[1] and ne[1] < im.size[1]:
            if in_threshold(im.getpixel(se), im.getpixel(ne), th) and co[ne[0]][ne[1]] == False:
                found = True

        if not found:
            ne = (cu[0] + 1, cu[1])
            if 0 <= ne[0] and ne[0] < im.size[0] and 0 <= ne[1] and ne[1] < im.size[1]:
                if in_threshold(im.getpixel(se), im.getpixel(ne), th) and co[ne[0]][ne[1]] == False:
                    found = True

        if not found:
            ne = (cu[0], cu[1] - 1)
            if 0 <= ne[0] and ne[0] < im.size[0] and 0 <= ne[1] and ne[1] < im.size[1]:
                if in_threshold(im.getpixel(se), im.getpixel(ne), th) and co[ne[0]][ne[1]] == False:
                    found = True

        if not found:
            ne = (cu[0] - 1, cu[1])
            if 0 <= ne[0] and ne[0] < im.size[0] and 0 <= ne[1] and ne[1] < im.size[1]:
                if in_threshold(im.getpixel(se), im.getpixel(ne), th) and co[ne[0]][ne[1]] == False:
                    found = True

        if not found:
            cu = st.pop()
        else:
            st.append(cu)
            cu = ne

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            alpha = 0
            if co[x][y]:
                alpha = 255
            im_pe = im.getpixel((x, y))
            re_pe = (im_pe[0], im_pe[1], im_pe[2], alpha)
            im.putpixel((x, y), re_pe)
    return im, None


def threshold(im: Image, r_range: range, g_range: range, b_range: range):
    im = im.convert('RGBA')
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            px = im.getpixel((x, y))
            alpha = 0
            if px[0] in r_range and px[1] in g_range and px[2] in b_range:
                alpha = 255
            im.putpixel((x, y), (px[0], px[1], px[2], alpha))
    return im, None

from PIL import Image

import os
import uuid


def rle_compress(img: Image):
    def memoize(memo, buf, val):
        if memo[0] != val:
            buf += memo[0].to_bytes(1, 'big') + memo[1].to_bytes(3, 'big')
            memo[0] = val
            memo[1] = 1
        else:
            memo[1] += 1

    if img.mode != 'RGB':
        img = img.convert('RGB')

    filename = str(uuid.uuid4())
    filepath = os.path.join(
        '.', 'phocode', 'static', '.compression',
        filename
    )
    ofstream = open(filepath, 'wb+')

    ofstream.write(img.width.to_bytes(2, 'big'))
    ofstream.write(img.height.to_bytes(2, 'big'))

    buf = [bytearray(), bytearray(), bytearray()]
    memo = [[0, 0], [0, 0], [0, 0]]
    for x in range(img.width):
        for y in range(img.height):
            current_pixel = img.getpixel((x, y))
            for i, val in enumerate(current_pixel):
                memoize(memo[i], buf[i], val)

    buf[0] += memo[0][0].to_bytes(1, 'big') + memo[0][1].to_bytes(3, 'big')
    buf[1] += memo[1][0].to_bytes(1, 'big') + memo[1][1].to_bytes(3, 'big')
    buf[2] += memo[2][0].to_bytes(1, 'big') + memo[2][1].to_bytes(3, 'big')

    ofstream.write(buf[0])
    ofstream.write(buf[1])
    ofstream.write(buf[2])

    ofstream.close()
    return filename, None


def rle_decompress(ifstream):
    def to_buf(bf, stream, n_o_p):
        count = 0
        while (count < n_o_p):
            val = int.from_bytes(stream.read(1), 'big')
            num = int.from_bytes(stream.read(3), 'big')
            bf.append([
                val,
                num
            ])
            count += num

    def get_data(bf, dt):
        if dt[1] == 0:
            dt = bf.pop(0)
            dt[1] -= 1
        else:
            dt[1] -= 1
        return dt

    width = int.from_bytes(ifstream.read(2), 'big')
    height = int.from_bytes(ifstream.read(2), 'big')

    img = Image.new(
        mode='RGB',
        size=(width, height),
        color=(256, 256, 256)
    )

    number_of_pixel = width * height
    print(number_of_pixel)
    buf = [[], [], []]
    to_buf(buf[0], ifstream, number_of_pixel)
    to_buf(buf[1], ifstream, number_of_pixel)
    to_buf(buf[2], ifstream, number_of_pixel)
    ifstream.close()

    r = buf[0].pop(0)
    g = buf[1].pop(0)
    b = buf[2].pop(0)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r = get_data(buf[0], r)
            g = get_data(buf[1], g)
            b = get_data(buf[2], b)

            img.putpixel((x, y), (r[0], g[0], b[0]))
    return img, None

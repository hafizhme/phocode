from PIL import Image
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


def do(original_image: Image):
    freq = [
        [0 for x in range(256)],
        [0 for x in range(256)],
        [0 for x in range(256)],
    ]

    for x in range(original_image.size[0]):
        for y in range(original_image.size[1]):
            px = original_image.getpixel((x, y))
            freq[0][px[0]] += 1
            freq[1][px[1]] += 1
            freq[2][px[2]] += 1

    figure, axarr = plt.subplots(3)
    colors = ('red', 'green', 'blue')
    data = (freq[0], freq[1], freq[2])

    subplots = range(3)
    bands_range = range(256)
    for data, i, color in zip(data, subplots, colors):
        axarr[i].bar(
            bands_range,
            data,
            width=2,
            facecolor=color
        )
        axarr[i].set_xlim(
            (0, 255)
        )

    figure.subplots_adjust(hspace=0.3)

    return plt, None

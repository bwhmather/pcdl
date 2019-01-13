import PIL.Image
import PIL.ImageSequence

from pcdl.grid import Coordinate2
from pcdl.layers import Layer


def load_gif(filename):
    gif = PIL.Image.open(filename)
    layers = []
    for image in PIL.ImageSequence.Iterator(gif):
        width, height = image.size
        transparency = image.info['transparency']

        layer = Layer(width=width, height=height)
        for x in range(width):
            for y in range(height):
                if image.getpixel((x, y)) == transparency:
                    continue

                if x < 2 or x > width - 2 or y < 2 or x > height - 2:
                    raise Exception("out of bounds")

                above = image.getpixel((x, y - 1)) != transparency
                below = image.getpixel((x, y + 1)) != transparency
                left = image.getpixel((x - 1, y)) != transparency
                right = image.getpixel((x + 1, y)) != transparency

                # Pixel has no neighbours.
                if not any([above, below, left, right]):
                    layer.add_pin(Coordinate2(x, y))

                if right:
                    layer.add_link(
                        Coordinate2(x, y),
                        Coordinate2(x + 1, y),
                    )

                if below:
                    layer.add_link(
                        Coordinate2(x, y),
                        Coordinate2(x, y + 1),
                    )

        layers.append(layer)
    return layers

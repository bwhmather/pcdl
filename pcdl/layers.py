from typing import Set, Optional

from pcdl.grid import Coordinate2

_UNNAMED_LAYER_COUNT = 0


def _sign(i):
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0


class _Link(object):

    def __init__(self, layer, pin_a, pin_b):
        self.layer = layer
        self.pin_a = pin_a
        self.pin_b = pin_b

    def __eq__(self, other):
        return (
            self.pin_a == other.pin_a and
            self.pin_b == other.pin_b and
            self.layer == other.layer
        )

    def __hash__(self):
        return hash((self.pin_a, self.pin_b))

    def __str__(self):
        return "Link(({a_x}, {a_y}), ({b_x}, {b_y}), layer={layer!r})".format(
            a_x=self.pin_a.position.x,
            a_y=self.pin_a.position.y,
            b_x=self.pin_b.position.x,
            b_y=self.pin_b.position.y,
            layer=self.layer,
        )

    def __repr__(self):
        return str(self)


class _Pin(object):

    def __init__(self, layer, position):
        self.layer = layer
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.position == other.position and
            self.layer == other.layer
        )

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return "Pin(({x}, {y}), layer={layer!r})".format(
            x=self.position[0],
            y=self.position[1],
            layer=self.layer,
        )

    def __repr__(self):
        return str(self)


class Layer(object):

    def __init__(self, name: Optional[str] = None, thickness: float = 2.0):
        if name is None:
            global _UNNAMED_LAYER_COUNT
            _UNNAMED_LAYER_COUNT += 1
            name = f"Unnamed layer {_UNNAMED_LAYER_COUNT}"
        self.name: str = name

        self.thickness: float = thickness

        # The set of drilled nodes
        self.__pins: Set[Coordinate2] = set()

        # The set of nodes with a link to the node on their right
        self.__x_links: Set[Coordinate2] = set()

        # The set of nodes with a link going down
        self.__y_links: Set[Coordinate2] = set()

    def add_pin(self, position: Coordinate2):
        self.__pins.add(position)
        return _Pin(self, position)

    def pins(self):
        for pin in self.__pins:
            yield _Pin(self, pin)

    def add_link(self, pin_a, pin_b):
        """Adds a single step, horizontal or vertical link between two, drilled
        pins.
        """
        (a_x, a_y) = pin_a.position
        (b_x, b_y) = pin_b.position

        # Vertical link
        if a_x == b_x:
            if abs(b_y - a_y) != 1:
                raise ValueError("Can only link adjacent nodes")

            self.__y_links.add(Coordinate2(a_x, min(a_y, b_y)))

        # Horizontal link
        elif a_y == b_y:
            if abs(b_x - a_x) != 1:
                raise ValueError("Can only link adjacent nodes")

            self.__x_links.add(Coordinate2(min(a_x, b_x), a_y))

        else:
            raise ValueError("Links must be either horizontal or vertical")

    def neighbours(self, pos):
        """Returns an iterator over all coordinates adjacent to a point.

        These do not have to be linked.
        """
        x, y = pos
        return {
            Coordinate2(x - 1, y),
            Coordinate2(x, y - 1),
            Coordinate2(x + 1, y),
            Coordinate2(x, y + 1),
        }

    def connected(self, pos):
        """Returns an iterator over all of the points that are connected to the
        origin by a link.
        """
        connected = set()
        x, y = pos
        if Coordinate2(x - 1, y) in self.__x_links:
            connected.add(Coordinate2(x - 1, y))
        if Coordinate2(x, y - 1) in self.__y_links:
            connected.add(Coordinate2(x, y - 1))
        if Coordinate2(x, y) in self.__x_links:
            connected.add(Coordinate2(x + 1, y))
        if Coordinate2(x, y) in self.__y_links:
            connected.add(Coordinate2(x, y + 1))
        return connected

    def links(self):
        for origin in self.__x_links:
            yield _Link(
                self,
                _Pin(self, origin),
                _Pin(self, Coordinate2(origin.x + 1, origin.y)),
            )

        for origin in self.__y_links:
            yield _Link(
                self,
                _Pin(self, origin),
                _Pin(self, Coordinate2(origin.x, origin.y + 1)),
            )

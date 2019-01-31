from typing import Set, Optional

from pcdl.grid import Coordinate2

_UNNAMED_LAYER_COUNT = 0


class _Link(object):

    def __init__(self, layer, a, b):
        self.layer = layer
        self.a = a
        self.b = b

    def __eq__(self, other):
        return (
            self.a == other.a and
            self.b == other.b and
            self.layer == other.layer
        )

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        return "Link(({a_x}, {a_y}), ({b_x}, {b_y}), layer={layer!r})".format(
            a_x=self.a.x,
            a_y=self.a.y,
            b_x=self.b.x,
            b_y=self.b.y,
            layer=self.layer,
        )

    def __repr__(self):
        return str(self)


class _Pin(object):

    def __init__(self, layer, position, *, radius):
        self.layer = layer
        self.position = position
        self.radius = radius

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

    def __init__(
        self, *, name: Optional[str] = None,
        grid: float = 3.0, width: int, height: int,
        material: str = 'acrylic', thickness: float=2.0,
    ):
        if name is None:
            global _UNNAMED_LAYER_COUNT
            _UNNAMED_LAYER_COUNT += 1
            name = f"unknown{_UNNAMED_LAYER_COUNT}"
        self.name: str = name

        self.material: str = material
        self.thickness: float = thickness

        self.grid = grid
        self.width = width
        self.height = height

        # The set of drilled nodes
        self.__pins: Set[Coordinate2] = set()
        self.__pin_radiuses: Map[Coordinate2, float] = {}

        # The set of nodes with a link to the node on their right
        self.__x_links: Set[Coordinate2] = set()

        # The set of nodes with a link going down
        self.__y_links: Set[Coordinate2] = set()

    def add_pin(self, position: Coordinate2, radius):
        self.__pins.add(position)
        self.__pin_radiuses[position] = radius
        return _Pin(self, position, radius=radius)

    def pins(self):
        for pin in self.__pins:
            radius = self.__pin_radiuses[pin]
            yield _Pin(self, pin, radius=radius)

    def add_link(self, a: Coordinate2, b: Coordinate2):
        """Adds a single step, horizontal or vertical link between two, drilled
        pins.
        """
        # Vertical link
        if a.x == b.x:
            if abs(b.y - a.y) != 1:
                raise ValueError("Can only link adjacent nodes")

            self.__y_links.add(Coordinate2(a.x, min(a.y, b.y)))

        # Horizontal link
        elif a.y == b.y:
            if abs(b.x - a.x) != 1:
                raise ValueError("Can only link adjacent nodes")

            self.__x_links.add(Coordinate2(min(a.x, b.x), a.y))

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
            yield _Link(self, origin, Coordinate2(origin.x + 1, origin.y))

        for origin in self.__y_links:
            yield _Link(self, origin, Coordinate2(origin.x, origin.y + 1))

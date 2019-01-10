from typing import Set

from pcdl.grid import Coordinate2


def _sign(i):
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0


class _Contact(object):
    __slots__ = ['layer', 'position']

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
        return "Contact(({x}, {y}), layer={layer!r})".format(
            x=self.position.x,
            y=self.position.y,
            layer=self.layer,
        )

    def __repr__(self):
        return str(self)


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

    def contact(self):
        return _Contact(self.layer, self.position)

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


class _Transistor(object):
    def __init__(self, layer, start, stop, slots):
        self._start = start
        self._stop = stop
        self._slots = slots
        self.layer = layer

    def contact(self, identifier):
        contact_type, contact_index = identifier[0], int(identifier[1:])
        if contact_type == 'i':
            position = [self._start, self._stop][contact_index]
        elif contact_type == 'o':
            unit_vector = (
                _sign(self._stop[0] - self._start[0]),
                _sign(self._stop[1] - self._start[1]),
            )
            offset = contact_index + 2
            position = Coordinate2(
                offset * unit_vector[0] + self._start[0],
                offset * unit_vector[1] + self._start[1],
            )
        else:
            raise ValueError()

        return _Contact(self.layer, position)


class Layer(object):
    """
    types:
      - top layer with connections
      - routing layer
      - layer with holes
      - layer for transistors
    """
    def __init__(self):
        # The set of drilled nodes
        self._pins: Set[Coordinate2] = set()

        # The set of nodes with a link to the node on their right
        self._x_links: Set[Coordinate2] = set()

        # The set of nodes with a link going down
        self._y_links: Set[Coordinate2] = set()

        # The set of transistors
        self._transistors: Set[_Transistor] = []

    def thickness(self):
        # TODO decide how detailed the material description needs to be and
        # whether it belongs at this level of abstraction
        pass

    def add_pin(self, position: Coordinate2):
        self._pins.add(position)
        return _Pin(self, position)

    def pins(self):
        for pin in self._pins:
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

            self._y_links.add(Coordinate2(a_x, min(a_y, b_y)))

        # Horizontal link
        elif a_y == b_y:
            if abs(b_x - a_x) != 1:
                raise ValueError("Can only link adjacent nodes")

            self._x_links.add(Coordinate2(min(a_x, b_x), a_y))

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
        if Coordinate2(x - 1, y) in self._x_links:
            connected.add(Coordinate2(x - 1, y))
        if Coordinate2(x, y - 1) in self._y_links:
            connected.add(Coordinate2(x, y - 1))
        if Coordinate2(x, y) in self._x_links:
            connected.add(Coordinate2(x + 1, y))
        if Coordinate2(x, y) in self._y_links:
            connected.add(Coordinate2(x, y + 1))
        return connected

    def links(self):
        for origin in self._x_links:
            yield _Link(
                self,
                _Pin(self, origin),
                _Pin(self, Coordinate2(origin.x + 1, origin.y)),
            )

        for origin in self._y_links:
            yield _Link(
                self,
                _Pin(self, origin),
                _Pin(self, Coordinate2(origin.x, origin.y + 1)),
            )

    def add_transistor(self, start, stop, *, slots):
        if start.x == stop.x:
            length = abs(stop.y - start.y)
        elif start.y == stop.y:
            length = abs(start.x - stop.x)
        else:
            raise ValueError(
                "Transistor must be either horizontal or vertical",
            )

        # There must be at least one slot
        assert len(slots)

        # Slots must at least cover one pine, and must not overlap.
        next_free = 0
        for slot_start, slot_stop in slots:
            assert slot_start >= next_free
            assert slot_stop >= slot_start

            next_free = slot_stop + 1

        # The minimum length of the transistor is the number of holes covered
        # by slots, plus an extra unit at each end to cover the furthest
        # outputs, plus a unit for travel, plus one for each input.
        min_length = slots[-1][1] + 2 + 1 + 2

        assert length >= min_length

        self._transistors.append((start, stop, slots))

        return _Transistor(self, start, stop, slots)

    def transistors(self):
        for start, stop, slots in self._transistors:
            yield _Transistor(self, start, stop, slots)

    def __repr__(self):
        return "[{self}]".format(self=self)

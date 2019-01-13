from typing import Tuple

import xml.etree.ElementTree
from xml.etree.ElementTree import TreeBuilder

from pcdl.grid import (
    Vector2, Coordinate2,
    Direction, UP, RIGHT, DOWN, LEFT,
    Angle, R0, R90, R180, R270,
)
from pcdl.layers import Layer


GRID = 3
RADIUS = 0.5


class PathBuilder(object):
    def __init__(self):
        self._elements = []

    def close(self):
        return ' '.join(self._elements)

    def _write(self, element):
        self._elements.append(element)

    def move(self, dx, dy):
        self._write(f"m {dx},{dy}")

    def move_to(self, x, y):
        self._write(f"M {x},{y}")

    def line(self, dx, dy):
        self._write(f"l {dx},{dy}")

    def line_to(self, x, y):
        self._write(f"L {x},{y}")

    def quadratic(self, dcx, dcy, dx, dy):
        self._write(f"q {dcx},{dcy} {dx},{dy}")

    def quadratic_to(self, cx, cy, x, y):
        self._write(f"Q {cx},{cy} {x},{y}")

    def cubic(self, dcax, dcay, dcbx, dcby, dx, dy):
        self._write(f"c {dcax},{dcay} {dcbx},{dcby} {dx},{dy}")

    def cubic_to(self, cax, cay, cbx, cby, x, y):
        self._write(f"C {cax},{cay} {cbx},{cby} {x},{y}")

    def arc(self, dx, dy, rx, ry, axis=0, large=False, clockwise=True):
        large = 1 if large else 0
        clockwise = 1 if clockwise else 0

        self._write(f"a {rx},{rx} {axis} {large},{clockwise} {dx},{dy}")

    def arc_to(self, x, y, rx, ry, axis=0, large=False, clockwise=True):
        large = 1 if large else 0
        clockwise = 0 if clockwise else 1  # y axis is flipped in SVG

        self._write(f"A {rx},{rx} {axis} {large},{clockwise} {x},{y}")

    def close_path(self):
        self._write("Z")


class Transformation(object):
    """This would ideally just be an arbitrary 3x3 matrix but dealing with
    arcs makes this impossible
    """
    offset: Coordinate2
    scale: float
    rotation: Angle

    def __init__(
        self, offset: Coordinate2, scale: float, rotation: Angle,
    ) -> None:
        self.offset = offset
        self.scale = scale
        self.rotation = rotation

    def transform_point(
        self, position: Tuple[float, float],
    ) -> Tuple[float, float]:
        x, y = position
        x, y = {
            R0: (x, y),
            R90: (y, -x),
            R180: (-x, -y),
            R270: (-y, x),
        }[self.rotation]

        x += self.offset.x
        y += self.offset.y
        x *= self.scale
        y *= self.scale

        return x, y

    def transform_distance(self, distance: float) -> float:
        return self.scale * distance


def _grid_position_to_svg(position: Coordinate2) -> Tuple[float, float]:
    x, y = position

    return ((GRID * x), (GRID * y))


def _render_pins(svg: TreeBuilder, layer: Layer) -> None:
    # Sort the pins left to right then up and down to avoid any pathological
    # movement of the cutting head.
    pins = sorted(layer.pins(), key=lambda pin: tuple(pin.position))

    r = GRID * RADIUS

    for pin in pins:
        if layer.connected(pin.position):
            continue
        x, y = _grid_position_to_svg(pin.position)

        path = PathBuilder()
        path.move_to(x, y + r)
        path.arc_to(x + r, y, rx=r, ry=r)
        path.arc_to(x, y - r, rx=r, ry=r)
        path.arc_to(x - r, y, rx=r, ry=r)
        path.arc_to(x, y + r, rx=r, ry=r)
        path.close_path()  # TODO

        path = path.close()

        svg.start("path", {
            "d": str(path),
            "stroke": "black",
            "stroke-width": "0.25",
            "fill": "none",
        })
        svg.end("path")


class _HalfEdge(object):
    __slots__ = ['src', 'tgt', 'direction']

    src: Coordinate2
    tgt: Coordinate2
    direction: Direction

    def __init__(self, src: Coordinate2, tgt: Coordinate2) -> None:
        if not isinstance(src, Coordinate2):
            raise TypeError()

        if not isinstance(tgt, Coordinate2):
            raise TypeError()

        direction = {
            Vector2(1, 0): RIGHT,
            Vector2(0, -1): DOWN,
            Vector2(-1, 0): LEFT,
            Vector2(0, 1): UP,
        }.get(tgt - src)

        if direction is None:
            raise ValueError("Source and target are not adjacent")

        self.src = src
        self.tgt = tgt
        self.direction = direction

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return (
            self.src == other.src and
            self.tgt == other.tgt
        )

    def __hash__(self):
        return hash((self.src, self.tgt))

    def __getitem__(self, index):
        # needed for unpacking
        return [self.src, self.tgt][index]

    def __str__(self):
        return f"HalfEdge({self.src}, {self.tgt})"

    def __repr__(self):
        return str(self)


def _turn_right(half_edge: _HalfEdge) -> _HalfEdge:
    return _HalfEdge(
        half_edge.tgt,
        half_edge.tgt + Vector2.unit_vector(half_edge.direction + R90),
    )


def _turn_ahead(half_edge: _HalfEdge) -> _HalfEdge:
    return _HalfEdge(
        half_edge.tgt,
        half_edge.tgt + Vector2.unit_vector(half_edge.direction),
    )


def _turn_left(half_edge: _HalfEdge) -> _HalfEdge:
    return _HalfEdge(
        half_edge.tgt,
        half_edge.tgt + Vector2.unit_vector(half_edge.direction - R90),
    )


def _turn_back(half_edge: _HalfEdge) -> _HalfEdge:
    return _HalfEdge(
        half_edge.tgt,
        half_edge.src,
    )


def _render_0(path: PathBuilder, transformation: Transformation) -> None:
    path.line_to(*transformation.transform_point((-RADIUS, 0.0)))


def _render_90(path: PathBuilder, transformation: Transformation) -> None:
    r = transformation.transform_distance(RADIUS)

    path.line_to(*transformation.transform_point((-RADIUS, 0.0)))
    path.arc_to(*transformation.transform_point((0.0, RADIUS)), rx=r, ry=r)


def _render_270(path: PathBuilder, transformation: Transformation) -> None:
    path.line_to(*transformation.transform_point((-RADIUS, -RADIUS)))


def _render_180(path: PathBuilder, transformation: Transformation) -> None:
    r = transformation.transform_distance(RADIUS)

    path.line_to(*transformation.transform_point((-RADIUS, 0)))
    path.arc_to(*transformation.transform_point((RADIUS, 0.0)), rx=r, ry=r)


def _render_routes(svg: TreeBuilder, layer: Layer) -> None:
    # Turn list of routes in the layer into a set of unvisited half edges.
    hedges = set()
    for link in layer.links():
        hedges.add(_HalfEdge(link.pin_a.position, link.pin_b.position))
        hedges.add(_HalfEdge(link.pin_b.position, link.pin_a.position))

    # Eliminate pairs of half edges that back onto each other.
    for hedge in list(hedges):
        if hedge in hedges:
            redge = _turn_left(_turn_left(hedge))
            if redge in hedges:
                hedges.remove(hedge)
                hedges.remove(redge)

    # Draw routes clockwise.
    while hedges:
        # Pick a random half edge off the list as the starting point.
        nedge = next(iter(hedges))

        transformation = Transformation(
            offset=nedge.tgt, scale=GRID, rotation=nedge.direction - UP,
        )
        path = PathBuilder()
        path.move_to(*transformation.transform_point((-RADIUS, -0.5)))
        while True:
            transformation = Transformation(
                offset=nedge.tgt, scale=GRID, rotation=nedge.direction - UP,
            )
            if _turn_left(nedge) in hedges:
                nedge = _turn_left(nedge)
                _render_270(path, transformation)
            elif _turn_ahead(nedge) in hedges:
                nedge = _turn_ahead(nedge)
                _render_0(path, transformation)
            elif _turn_right(nedge) in hedges:
                nedge = _turn_right(nedge)
                _render_90(path, transformation)
            elif _turn_back(nedge) in hedges:
                nedge = _turn_back(nedge)
                _render_180(path, transformation)
            else:
                # We should be back at the beginning
                break

            hedges.remove(nedge)

        path.close_path()
        path = path.close()

        svg.start("path", {
            "d": str(path),
            "stroke": "red",
            "stroke-width": "0.25",
            "fill": "none",
        })
        svg.end("path")


def render_layer(layer, output):
    svg = xml.etree.ElementTree.TreeBuilder()
    width = layer.width
    height = layer.height
    grid = layer.grid

    svg.start("svg", {
        "version": "1.1",
        "baseProfile": "full",
        "width": f"{grid * width}mm",
        "height": f"{ grid * height}mm",
        "viewBox": f"0 0 {grid * width} {grid * height}",
        "xmlns": "http://www.w3.org/2000/svg",
    })

    svg.start("g", {"id": "root"})
    _render_routes(svg, layer)
    _render_pins(svg, layer)
    svg.end("g")

    svg.end("svg")
    element = svg.close()
    element_tree = xml.etree.ElementTree.ElementTree(element)

    element_tree.write(output)


def render_composite(filenames, output):
    svg = xml.etree.ElementTree.TreeBuilder()
    width = 31
    height = 40

    svg.start("svg", {
        "version": "1.1",
        "baseProfile": "full",
        "width": f"{GRID*width}mm",
        "height": f"{GRID*height}mm",
        "viewBox": f"0 0 {GRID*width} {GRID*height}",
        "xmlns": "http://www.w3.org/2000/svg",
    })

    svg.start("defs", {})
    svg.start("pattern", {
        "id": "GridPattern",
        "x": str(GRID / 2), "y": str(GRID / 2),
        "width": str(GRID), "height": str(GRID),
        "patternUnits": "userSpaceOnUse",
    })

    svg.start("rect", {
        "x": "0", "y": "0",
        "width": str(GRID), "height": str(GRID),
        "fill": "none",
        "stroke": "lightGrey",
        "stroke-width": "1px"
    })
    svg.end("rect")

    svg.end("pattern")
    svg.end("defs")

    svg.start("rect", {
        "width": "100%",
        "height": "100%",
        "fill": "url(#GridPattern)",
    })
    svg.end("rect")

    for filename in filenames:
        svg.start("use", {
            "href": f"{filename}#root",
        })
        svg.end("use")

    svg.end("svg")
    element = svg.close()
    element_tree = xml.etree.ElementTree.ElementTree(element)

    element_tree.write(output)

from typing import Union, Optional
from pcdl.grid import Coordinate2


class BoundingBox(object):
    __slots__ = ['l', 'b', 'r', 't']

    l: int
    b: int
    r: int
    t: int

    def __init__(self, *, l: int, b: int, r: int, t: int) -> None:
        if l > r:
            raise ValueError("box is back-to-front")
        if b > t:
            raise ValueError("box is upside-down")

        super().__setattr__('l', l)
        super().__setattr__('b', b)
        super().__setattr__('r', r)
        super().__setattr__('t', t)

    def __contains_coord(self, coord: Coordinate2) -> bool:
        return (
            self.l <= coord.x and
            self.b <= coord.y and
            self.r >= coord.x and
            self.t >= coord.y
        )

    def __contains_box(self, other: 'BoundingBox') -> bool:
        return (
            self.l <= other.l and
            self.b <= other.b and
            self.r >= other.r and
            self.t >= other.t
        )

    def contains(self, other: Union['BoundingBox', Coordinate2]) -> bool:
        if isinstance(other, Coordinate2):
            return self.__contains_coord(other)

        if isinstance(other, BoundingBox):
            return self.__contains_box(other)

        raise TypeError()

    def expand(self, coord: Coordinate2) -> 'BoundingBox':
        pass

    def __hash__(self):
        return hash((self.l, self.b, self.r, self.t))

    def __eq__(self, other):
        if not isinstance(other, BoundingBox):
            return NotImplemented

        return (
            self.l == other.l and
            self.b == other.b and
            self.r == other.r and
            self.t == other.t
        )

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError((
                '{cls!r} attribute {name!r} is read-only'
            ).format(cls=self.__class__.__name__, name=str(name)))

        else:
            raise AttributeError((
                '{cls!r} object has no attribute {name!r}'
            ).format(cls=self.__class__.__name__, name=str(name)))

    def __repr__(self):
        return 'BoundingBox(l={l!r}, b={b!r}, r={r!r}, t={t!r})'.format(
            l=self.l, b=self.b, r=self.r, t=self.t,
        )


def intersects(box_a: BoundingBox, box_b: BoundingBox) -> bool:
    return (
        box_a.l <= box_b.r and
        box_b.l <= box_a.r and
        box_a.b <= box_b.t and
        box_b.b <= box_a.t
    )


def intersect(box_a: BoundingBox, box_b: BoundingBox) -> Optional[BoundingBox]:
    if not intersects(box_a, box_b):
        return None

    return BoundingBox(
        l=max(box_a.l, box_b.l),
        b=max(box_a.b, box_b.b),
        r=min(box_a.r, box_b.r),
        t=min(box_a.t, box_b.t),
    )


def merge(box_a: BoundingBox, box_b: BoundingBox) -> BoundingBox:
    return BoundingBox(
        l=min(box_a.l, box_b.l),
        b=min(box_a.b, box_b.b),
        r=max(box_a.r, box_b.r),
        t=max(box_a.t, box_b.t),
    )

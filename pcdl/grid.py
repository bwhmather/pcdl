"""
Datatypes for describing the position and orientation of features on the PCDL
grid.

For convenience, PCDL uses the same coordinate system as SVG and GIF with the
origin in the top left and y increasing in the downwards direction.

PCDL uses the type checker to enforce a strict separation between absolute and
relative measurements.  Absolute measurements can be subtracted to get a
relative difference, but cannot be added.  Relative measurements cannot be used
for output.
"""
import numbers
import enum
import collections.abc
from dataclasses import dataclass


class Angle(enum.Enum):
    """
    Describes a rotation by a multiple of 90 degrees.
    """

    R0 = 'R0'
    R90 = 'R90'
    R180 = 'R180'
    R270 = 'R270'

    @classmethod
    def _from_int(cls, integer):
        return [
            Angle.R0,
            Angle.R90,
            Angle.R180,
            Angle.R270,
        ][integer % 4]

    def _to_int(self):
        return {
            Angle.R0: 0,
            Angle.R90: 1,
            Angle.R180: 2,
            Angle.R270: 3,
        }[self]

    def __neg__(self):
        return {
            Angle.R0: Angle.R0,
            Angle.R90: Angle.R270,
            Angle.R180: Angle.R180,
            Angle.R270: Angle.R90,
        }[self]

    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle._from_int(
                self._to_int() + other._to_int(),
            )

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle._from_int(
                self._to_int() - other._to_int(),
            )

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            return Angle._from_int(self._to_int() * other)

        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return self.name


R0 = Angle.R0
R90 = Angle.R90
R180 = Angle.R180
R270 = Angle.R270


class Direction(enum.Enum):
    """
    Describes an absolute direction.
    """

    UP = 'UP'
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    LEFT = 'LEFT'

    @classmethod
    def _from_angle(cls, angle):
        return {
            Angle.R0: Direction.UP,
            Angle.R90: Direction.RIGHT,
            Angle.R180: Direction.DOWN,
            Angle.R270: Direction.LEFT,
        }[angle]

    def _to_angle(self):
        return {
            Direction.UP: Angle.R0,
            Direction.RIGHT: Angle.R90,
            Direction.DOWN: Angle.R180,
            Direction.LEFT: Angle.R270,
        }[self]

    def __add__(self, other):
        if isinstance(other, Angle):
            return Direction._from_angle(
                self._to_angle() + other,
            )

        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Direction):
            return self._to_angle() - other._to_angle()

        if isinstance(other, Angle):
            return Direction._from_angle(
                self._to_angle() - other,
            )

        return NotImplemented

    def __repr__(self):
        return self.name


UP = Direction.UP
RIGHT = Direction.RIGHT
DOWN = Direction.DOWN
LEFT = Direction.LEFT


@dataclass(frozen=True)
class Vector2(collections.abc.Iterable):
    """
    Describes a difference between two coordinates.
    """

    __slots__ = ['x', 'y']

    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __bool__(self):
        return self.x and self.y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        if isinstance(other, numbers.Number):
            return Vector2(self.x * other, self.y * other)

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector2(other * self.x, other * self.y)

        return NotImplemented

    def rotate(self, angle):
        return {
            R0: Vector2(self.x, self.y),
            R90: Vector2(self.y, -self.x),
            R180: Vector2(-self.x, -self.y),
            R270: Vector2(-self.y, self.x),
        }[angle]

    @classmethod
    def unit_vector(cls, direction):
        return {
            Direction.UP: Vector2(0, 1),
            Direction.RIGHT: Vector2(1, 0),
            Direction.DOWN: Vector2(0, -1),
            Direction.LEFT: Vector2(-1, 0),
        }[direction]


@dataclass(frozen=True)
class Coordinate2(collections.abc.Iterable):
    """
    Describes an absolute position on the PCDL grid.
    """

    __slots__ = ['x', 'y']

    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Coordinate2(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Vector2):
            return Coordinate2(self.x + other.x, self.y + other.y)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Coordinate2):
            return Vector2(self.x - other.x, self.y - other.y)

        if isinstance(other, Vector2):
            return Coordinate2(self.x - other.x, self.y - other.y)

        return NotImplemented

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
        if not isinstance(other, Angle):
            return NotImplemented

        return Angle._from_int(
            self._to_int() + other._to_int(),
        )

    def __sub__(self, other):
        if not isinstance(other, Angle):
            return NotImplemented

        return Angle._from_int(
            self._to_int() - other._to_int(),
        )

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return Angle._from_int(self._to_int() * other)

    def __rmul__(self, other):
        return self * other


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
        if not isinstance(other, Angle):
            return NotImplemented

        return Direction._from_angle(
            self._to_angle() + other,
        )

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


UP = Direction.UP
RIGHT = Direction.RIGHT
DOWN = Direction.DOWN
LEFT = Direction.LEFT


class Vector2(collections.abc.Iterable):
    """
    Describes a difference between two coordinates.
    """

    __slots__ = ['x', 'y']

    x: int
    y: int

    def __init__(self, x, y):
        super().__setattr__('x', x)
        super().__setattr__('y', y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented

        return (
            self.x == other.x and
            self.y == other.y
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
        return 'Vector2(x={x!r}, y={y!r})'.format(x=self.x, y=self.y)

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


class Coordinate2(collections.abc.Iterable):
    """
    Describes an absolute position on the PCDL grid.
    """

    __slots__ = ['x', 'y']

    x: int
    y: int

    def __init__(self, x, y):
        super().__setattr__('x', x)
        super().__setattr__('y', y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Coordinate2):
            return NotImplemented

        return (
            self.x == other.x and
            self.y == other.y
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
        return 'Coordinate2(x={x!r}, y={y!r})'.format(x=self.x, y=self.y)

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


class Position(object):
    __slots__ = ['x', 'y', 'z', 'd']

    def __init__(self, x, y, z=0, *, d=R0):
        self.x = x
        self.y = y
        self.z = z
        self.d = d

    def __add__(self, other: 'Position') -> 'Position':
        if not isinstance(other, Position):
            return NotImplemented

        x, y = (
            Vector2(self.x, self.y).rotate(self.d) +
            Vector2(other.x, other.y).rotate(self.d + other.d)
        )
        z = self.z + other.z
        d = self.d + other.d

        return Position(x, y, z, d=d)

    def __str__(self):
        return "Position(x={x}, y={y}, z={z}, d={d})".format(
            x=self.x, y=self.y, z=self.z, d=self.d,
        )

    def __repr__(self):
        return str(self)

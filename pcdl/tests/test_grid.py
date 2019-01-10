import unittest

from pcdl.grid import (
    Vector2, Coordinate2,
    R0, R90, R180, R270,
    UP, RIGHT, DOWN, LEFT,
)


class AngleTestCase(unittest.TestCase):
    def test_negate(self):
        self.assertEqual(-R0, R0)
        self.assertEqual(-R90, R270)
        self.assertEqual(-R180, R180)
        self.assertEqual(-R270, R90)

    def test_add_angle(self):
        self.assertEqual(R0 + R0, R0)
        self.assertEqual(R0 + R90, R90)
        self.assertEqual(R0 + R180, R180)
        self.assertEqual(R0 + R270, R270)
        self.assertEqual(R90 + R0, R90)
        self.assertEqual(R90 + R90, R180)
        self.assertEqual(R90 + R180, R270)
        self.assertEqual(R90 + R270, R0)
        self.assertEqual(R180 + R0, R180)
        self.assertEqual(R180 + R90, R270)
        self.assertEqual(R180 + R180, R0)
        self.assertEqual(R180 + R270, R90)
        self.assertEqual(R270 + R0, R270)
        self.assertEqual(R270 + R90, R0)
        self.assertEqual(R270 + R180, R90)
        self.assertEqual(R270 + R270, R180)

    def test_subtract_angle(self):
        self.assertEqual(R0 - R0, R0)
        self.assertEqual(R0 - R90, R270)
        self.assertEqual(R0 - R180, R180)
        self.assertEqual(R0 - R270, R90)
        self.assertEqual(R90 - R0, R90)
        self.assertEqual(R90 - R90, R0)
        self.assertEqual(R90 - R180, R270)
        self.assertEqual(R90 - R270, R180)
        self.assertEqual(R180 - R0, R180)
        self.assertEqual(R180 - R90, R90)
        self.assertEqual(R180 - R180, R0)
        self.assertEqual(R180 - R270, R270)
        self.assertEqual(R270 - R0, R270)
        self.assertEqual(R270 - R90, R180)
        self.assertEqual(R270 - R180, R90)
        self.assertEqual(R270 - R270, R0)

    def test_multiply(self):
        self.assertEqual(-4 * R0, R0)
        self.assertEqual(-3 * R0, R0)
        self.assertEqual(-2 * R0, R0)
        self.assertEqual(-1 * R0, R0)
        self.assertEqual(0 * R0, R0)
        self.assertEqual(1 * R0, R0)
        self.assertEqual(2 * R0, R0)
        self.assertEqual(3 * R0, R0)
        self.assertEqual(4 * R0, R0)

        self.assertEqual(-4 * R90, R0)
        self.assertEqual(-3 * R90, R90)
        self.assertEqual(-2 * R90, R180)
        self.assertEqual(-1 * R90, R270)
        self.assertEqual(0 * R90, R0)
        self.assertEqual(1 * R90, R90)
        self.assertEqual(2 * R90, R180)
        self.assertEqual(3 * R90, R270)
        self.assertEqual(4 * R90, R0)

        self.assertEqual(-4 * R180, R0)
        self.assertEqual(-3 * R180, R180)
        self.assertEqual(-2 * R180, R0)
        self.assertEqual(-1 * R180, R180)
        self.assertEqual(0 * R180, R0)
        self.assertEqual(1 * R180, R180)
        self.assertEqual(2 * R180, R0)
        self.assertEqual(3 * R180, R180)
        self.assertEqual(4 * R180, R0)

        self.assertEqual(-4 * R270, R0)
        self.assertEqual(-3 * R270, R270)
        self.assertEqual(-2 * R270, R180)
        self.assertEqual(-1 * R270, R90)
        self.assertEqual(0 * R270, R0)
        self.assertEqual(1 * R270, R270)
        self.assertEqual(2 * R270, R180)
        self.assertEqual(3 * R270, R90)
        self.assertEqual(4 * R270, R0)


class DirectionTestCase(unittest.TestCase):
    def test_add_angle(self):
        self.assertEqual(UP + R0, UP)
        self.assertEqual(UP + R90, RIGHT)
        self.assertEqual(UP + R180, DOWN)
        self.assertEqual(UP + R270, LEFT)
        self.assertEqual(RIGHT + R0, RIGHT)
        self.assertEqual(RIGHT + R90, DOWN)
        self.assertEqual(RIGHT + R180, LEFT)
        self.assertEqual(RIGHT + R270, UP)
        self.assertEqual(DOWN + R0, DOWN)
        self.assertEqual(DOWN + R90, LEFT)
        self.assertEqual(DOWN + R180, UP)
        self.assertEqual(DOWN + R270, RIGHT)
        self.assertEqual(LEFT + R0, LEFT)
        self.assertEqual(LEFT + R90, UP)
        self.assertEqual(LEFT + R180, RIGHT)
        self.assertEqual(LEFT + R270, DOWN)

    def test_subtract_angle(self):
        self.assertEqual(UP - R0, UP)
        self.assertEqual(UP - R90, LEFT)
        self.assertEqual(UP - R180, DOWN)
        self.assertEqual(UP - R270, RIGHT)
        self.assertEqual(RIGHT - R0, RIGHT)
        self.assertEqual(RIGHT - R90, UP)
        self.assertEqual(RIGHT - R180, LEFT)
        self.assertEqual(RIGHT - R270, DOWN)
        self.assertEqual(DOWN - R0, DOWN)
        self.assertEqual(DOWN - R90, RIGHT)
        self.assertEqual(DOWN - R180, UP)
        self.assertEqual(DOWN - R270, LEFT)
        self.assertEqual(LEFT - R0, LEFT)
        self.assertEqual(LEFT - R90, DOWN)
        self.assertEqual(LEFT - R180, RIGHT)
        self.assertEqual(LEFT - R270, UP)

    def test_subtract_direction(self):
        self.assertEqual(UP - UP, R0)
        self.assertEqual(UP - RIGHT, R270)
        self.assertEqual(UP - DOWN, R180)
        self.assertEqual(UP - LEFT, R90)
        self.assertEqual(RIGHT - UP, R90)
        self.assertEqual(RIGHT - RIGHT, R0)
        self.assertEqual(RIGHT - DOWN, R270)
        self.assertEqual(RIGHT - LEFT, R180)
        self.assertEqual(DOWN - UP, R180)
        self.assertEqual(DOWN - RIGHT, R90)
        self.assertEqual(DOWN - DOWN, R0)
        self.assertEqual(DOWN - LEFT, R270)
        self.assertEqual(LEFT - UP, R270)
        self.assertEqual(LEFT - RIGHT, R180)
        self.assertEqual(LEFT - DOWN, R90)
        self.assertEqual(LEFT - LEFT, R0)


class Vector2TestCase(unittest.TestCase):

    def test_negate(self):
        self.assertEqual(-Vector2(1, 3), Vector2(-1, -3))

    def test_add_vector(self):
        a = Vector2(1, 2)
        b = Vector2(3, 5)

        self.assertEqual(a + b, Vector2(4, 7))

    def test_subtract_vector(self):
        a = Vector2(3, 5)
        b = Vector2(7, 11)

        self.assertEqual(b - a, Vector2(4, 6))

    def test_dot_product(self):
        a = Vector2(2, 3)
        b = Vector2(4, 5)

        self.assertEqual(a * b, Vector2(8, 15))

    def test_left_scalar_product(self):
        self.assertEqual(Vector2(2, 3) * 2, Vector2(4, 6))

    def test_right_scalar_product(self):
        self.assertEqual(2 * Vector2(2, 3), Vector2(4, 6))

    def test_rotate(self):
        a = Vector2(6, 2)

        self.assertEqual(a.rotate(R0), a)
        self.assertEqual(a.rotate(R90), Vector2(2, -6))
        self.assertEqual(a.rotate(R180), Vector2(-6, -2))
        self.assertEqual(a.rotate(R270), Vector2(-2, 6))

    def test_repeat_rotate(self):
        a = Vector2(5, 7)

        self.assertEqual(
            a.rotate(R90).rotate(R90).rotate(R90).rotate(R90), a,
        )
        self.assertEqual(
            a.rotate(R270).rotate(R270).rotate(R270).rotate(R270), a,
        )

    def test_equality(self):
        a = Vector2(1, 2)
        b = Vector2(1, 2)

        self.assertTrue(a == b)

    def test_inequality(self):
        a = Vector2(1, 2)
        b = Vector2(3, 2)
        c = Vector2(1, 4)

        self.assertTrue(a != b)
        self.assertTrue(a != c)

    def test_hash(self):
        a = Vector2(1, 2)
        b = Vector2(1, 2)

        self.assertTrue(hash(a) == hash(b))


class Coordinate2TestCase(unittest.TestCase):

    def test_construct_from_args(self):
        c = Coordinate2(1, 2)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)

    def test_construct_from_kwargs(self):
        c = Coordinate2(x=1, y=2)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)

    def test_negate(self):
        c = Coordinate2(12, 12)
        with self.assertRaises(TypeError):
            -c  # pylint: disable=invalid-unary-operand-type

    def test_add_coordinate(self):
        a = Coordinate2(1, 2)
        b = Coordinate2(3, 5)

        with self.assertRaises(TypeError):
            a + b

    def test_add_vector(self):
        a = Coordinate2(100, 50)
        b = Vector2(1, 1)

        self.assertEqual(a + b, Coordinate2(101, 51))
        self.assertEqual(b + a, Coordinate2(101, 51))

    def test_subtract_coordinate(self):
        a = Coordinate2(1, 2)
        b = Coordinate2(3, 5)

        self.assertEqual(b - a, Vector2(2, 3))

    def test_subtract_vector(self):
        c = Coordinate2(1, 2)
        v = Vector2(3, 5)

        self.assertEqual(c - v, Coordinate2(-2, -3))

    def test_subtract_from_vector(self):
        c = Coordinate2(1, 2)
        v = Vector2(3, 5)

        with self.assertRaises(TypeError):
            v - c

    def test_equality(self):
        a = Coordinate2(1, 2)
        b = Coordinate2(1, 2)

        self.assertTrue(a == b)

    def test_inequality(self):
        a = Coordinate2(1, 2)
        b = Coordinate2(3, 2)
        c = Coordinate2(1, 4)

        self.assertTrue(a != b)
        self.assertTrue(a != c)

    def test_hash(self):
        a = Coordinate2(1, 2)
        b = Coordinate2(1, 2)

        self.assertTrue(hash(a) == hash(b))

from pcdl.grid import Coordinate2
from pcdl.svg import _HalfEdge

import unittest


class HalfEdgeTestCase(unittest.TestCase):
    def test_equality(self):
        a = _HalfEdge(Coordinate2(1, 2), Coordinate2(1, 3))
        b = _HalfEdge(Coordinate2(1, 2), Coordinate2(1, 3))

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

    def test_lookup(self):
        s = {_HalfEdge(Coordinate2(1, 2), Coordinate2(1, 3))}
        self.assertIn(_HalfEdge(Coordinate2(1, 2), Coordinate2(1, 3)), s)

    def test_direction(self):
        pass

import unittest

from pcdl.grid import Coordinate2
from pcdl.bounding_box import BoundingBox, intersect, merge


class BoundingBoxInitTestCase(unittest.TestCase):
    def test_init_valid(self):
        bb = BoundingBox(l=1, b=2, r=3, t=4)
        self.assertEqual(bb.l, 1)
        self.assertEqual(bb.b, 2)
        self.assertEqual(bb.r, 3)
        self.assertEqual(bb.t, 4)

    def test_init_upside_down(self):
        with self.assertRaises(ValueError):
            BoundingBox(b=1, t=0, l=-1, r=1)

    def test_init_back_to_front(self):
        with self.assertRaises(ValueError):
            BoundingBox(l=1, r=0, b=-1, t=1)

    def test_immutable_after_init(self):
        bb = BoundingBox(l=1, b=2, r=3, t=4)

        with self.assertRaises(AttributeError):
            bb.l = 5
        self.assertEqual(bb.l, 1)

        with self.assertRaises(AttributeError):
            bb.nonexistant  # pylint: disable=no-member
        self.assertFalse(hasattr(bb, 'nonexistant'))


class BoundingBoxContainsCoordTestCase(unittest.TestCase):
    def test_contains_coord(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(0, 0)

        self.assertTrue(bb.contains(coord))

    def test_contains_coord_aligned_left(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(-1, 0)

        self.assertTrue(bb.contains(coord))

    def test_contains_coord_aligned_bottom(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(0, -1)

        self.assertTrue(bb.contains(coord))

    def test_contains_coord_aligned_right(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(1, 0)

        self.assertTrue(bb.contains(coord))

    def test_contains_coord_aligned_top(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(0, 1)

        self.assertTrue(bb.contains(coord))

    def test_does_not_contain_coord_left(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(-2, 0)

        self.assertFalse(bb.contains(coord))

    def test_does_not_contain_coord_bottom(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(0, -2)

        self.assertFalse(bb.contains(coord))

    def test_does_not_contain_coord_right(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(2, 0)

        self.assertFalse(bb.contains(coord))

    def test_does_not_contain_coord_top(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        coord = Coordinate2(0, 2)

        self.assertFalse(bb.contains(coord))


class BoundingBoxContainsBoxTestCase(unittest.TestCase):
    def test_contains_box(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=1, t=1)

        self.assertTrue(container.contains(contained))

    def test_contains_box_aligned_left(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-2, b=-1, r=1, t=1)

        self.assertTrue(container.contains(contained))

    def test_contains_box_aligned_bottom(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-2, r=1, t=1)

        self.assertTrue(container.contains(contained))

    def test_contains_box_aligned_right(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=2, t=1)

        self.assertTrue(container.contains(contained))

    def test_contains_box_aligned_top(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=1, t=2)

        self.assertTrue(container.contains(contained))

    def test_contains_self(self):
        container = BoundingBox(l=-1, b=-1, r=1, t=1)

        self.assertTrue(container.contains(container))

    def test_does_not_contain_container(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=1, t=1)

        self.assertFalse(contained.contains(container))

    def test_does_not_contain_box_left(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        overlapping = BoundingBox(l=-3, b=-1, r=1, t=1)

        self.assertFalse(container.contains(overlapping))

    def test_does_not_contain_box_bottom(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        overlapping = BoundingBox(l=-1, b=-3, r=1, t=1)

        self.assertFalse(container.contains(overlapping))

    def test_does_not_contain_box_right(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        overlapping = BoundingBox(l=-1, b=-1, r=3, t=1)

        self.assertFalse(container.contains(overlapping))

    def test_does_not_contain_box_top(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        overlapping = BoundingBox(l=-1, b=-1, r=1, t=3)

        self.assertFalse(container.contains(overlapping))


class BoundingBoxIntersectionTestCase(unittest.TestCase):
    def test_intersect_self(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        self.assertEqual(intersect(bb, bb), bb)

    def test_intersect_contained(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=1, t=1)

        self.assertEqual(intersect(container, contained), contained)

    def test_intersect_nonoverlapping(self):
        bb_a = BoundingBox(l=-3, b=-1, r=-1, t=1)
        bb_b = BoundingBox(l=1, b=-1, r=3, t=1)

        self.assertIsNone(intersect(bb_a, bb_b))


class BoundingBoxMergeTestCase(unittest.TestCase):
    def test_merge_self(self):
        bb = BoundingBox(l=-1, b=-1, r=1, t=1)
        self.assertEqual(merge(bb, bb), bb)

    def test_merge_contained(self):
        container = BoundingBox(l=-2, b=-2, r=2, t=2)
        contained = BoundingBox(l=-1, b=-1, r=1, t=1)

        self.assertEqual(merge(container, contained), container)

    def test_merge_nonoverlapping(self):
        bb_a = BoundingBox(l=-3, b=-1, r=-1, t=1)
        bb_b = BoundingBox(l=1, b=-1, r=3, t=1)

        self.assertEqual(merge(bb_a, bb_b), BoundingBox(l=-3, b=-1, r=3, t=1))

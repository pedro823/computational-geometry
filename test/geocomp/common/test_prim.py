import math
import unittest

import geocomp.common.prim as prim


class TestPrim(unittest.TestCase):

    def test_angleCCW_withNoneTypeArgument_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            prim.ccw_angle(None, [0, 0])

        with self.assertRaises(ValueError):
            prim.ccw_angle([0, 0], None)

    def test_angleCCW_withCollinearVectors_shouldReturnZero(self):
        self.assertEqual(0, prim.ccw_angle([0, 1], [0, 1]))

    def test_angleCCW_withNotCollinearVectors_shouldReturnClockWiseAngleBetweenThem(self):
        self.assertEqual(math.pi / 2, prim.ccw_angle([1, 0], [0, 1]))
        self.assertEqual(math.pi, prim.ccw_angle([1, 0], [-1, 0]))
        self.assertEqual(3 * math.pi / 2, prim.ccw_angle([1, 0], [0, -1]))


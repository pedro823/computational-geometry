import unittest

from geocomp.common.io      import read
from geocomp.common.point   import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment

import test.helper.reader as reader


class TestIO(unittest.TestCase):

    def test_read_withNoneTypeArgument_shouldRaiseTypeError(self):
        with self.assertRaises(TypeError):
            read(None)

    def test_read_withNonexistentFile_shouldRaiseFileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            read("nonexistent")

    def test_read_withFileContainingInvalidInput_shouldRaiseValueError(self):
        with self.assertRaises(ValueError):
            read("data/test/geocomp/common/io/error_file.txt")

    def test_read_withEmptyFile_shouldReturnEmptyList(self):
        self.assertEqual([], read("data/test/geocomp/common/io/empty_file.txt"))

    def test_read_withFileContainingOnlyCommentaries_shouldReturnEmptyList(self):
        self.assertEqual([], read("data/test/geocomp/common/io/only_commentaries.txt"))

    def test_read_withFileContainingOnlyPoints_shouldReturnListOfPoints(self):
        expected = reader.read_points("data/test/geocomp/common/io/only_points_expected.txt")
        self.assertCountEqual(expected, read("data/test/geocomp/common/io/only_points.txt"))

    def test_read_withFileContainingOnlySegments_shouldReturnListOfSegments(self):
        expected = reader.read_segments("data/test/geocomp/common/io/only_segments_expected.txt")
        self.assertCountEqual(expected, read("data/test/geocomp/common/io/only_segments.txt"))

    def test_read_withFileContainingOnlyPolygons_shouldReturnListOfPolygons(self):
        expected = reader.read_polygons("data/test/geocomp/common/io/only_polygons_expected.txt")
        self.assertCountEqual(expected, read("data/test/geocomp/common/io/only_polygons.txt"))

    def test_read_withFileContainingPointsSegmentsPolygons_shouldReturnListOfElements(self):
        expected_points   = reader.read_points("data/test/geocomp/common/io/only_points_expected.txt")
        expected_segments = reader.read_segments("data/test/geocomp/common/io/only_segments_expected.txt")
        expected_polygons = reader.read_polygons("data/test/geocomp/common/io/only_polygons_expected.txt")

        actual = read("data/test/geocomp/common/io/pt_seg_poly.txt")
        for e in actual:
            if type(e) is Point:
                self.assertIn(e, expected_points)
            if type(e) is Segment:
                self.assertIn(e, expected_segments)
            if type(e) is Polygon:
                self.assertIn(e, expected_polygons)

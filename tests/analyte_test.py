"""Function tests of analyte class"""

# std import
from unittest import TestCase

# local import
from macdii.analyte import Analyte  # type: ignore


class AnalyteTests(TestCase):
    """Function tests of Analyte class"""

    def test_calc_mz_range(self):
        """Tests the calc_mz_range function."""
        mz = 50.0
        ppm = 5
        expected_lower = mz - (0.00005 * ppm)
        expected_upper = mz + (0.00005 * ppm)

        lower, upper = Analyte.calc_mz_range(mz, ppm, ppm)

        self.assertEqual(lower, expected_lower)
        self.assertEqual(upper, expected_upper)

    def test_contains(self):
        """tests the contains functions"""
        mz = 50.0
        ppm = 5
        expected_lower = mz - (0.00005 * ppm)
        expected_upper = mz + (0.00005 * ppm)

        analyte = Analyte("test", mz, mz, mz, ppm, ppm, ppm, ppm)

        # Too low
        self.assertFalse(analyte.precursor_contains(expected_lower - 0.00001))
        # on lower limit
        self.assertTrue(analyte.precursor_contains(expected_lower))
        # in range
        self.assertTrue(analyte.precursor_contains(mz))
        # on upper limit
        self.assertTrue(analyte.precursor_contains(expected_upper))
        # Too high
        self.assertFalse(analyte.precursor_contains(expected_upper + 0.00001))

        # Too low
        self.assertFalse(analyte.quantifier_contains(expected_lower - 0.00001))
        # on lower limit
        self.assertTrue(analyte.quantifier_contains(expected_lower))
        # in range
        self.assertTrue(analyte.quantifier_contains(mz))
        # on upper limit
        self.assertTrue(analyte.quantifier_contains(expected_upper))
        # Too high
        self.assertFalse(analyte.quantifier_contains(expected_upper + 0.00001))

        # Too low
        self.assertFalse(analyte.qualifier_contains(expected_lower - 0.00001))
        # on lower limit
        self.assertTrue(analyte.qualifier_contains(expected_lower))
        # in range
        self.assertTrue(analyte.qualifier_contains(mz))
        # on upper limit
        self.assertTrue(analyte.qualifier_contains(expected_upper))
        # Too high
        self.assertFalse(analyte.qualifier_contains(expected_upper + 0.00001))

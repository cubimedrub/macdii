"""Test for Peak class"""
from functools import reduce
from unittest import TestCase

from macdii.analyte_match import Peak


class PeakTests(TestCase):
    """Test critical peak functions"""

    def test_iadd(self):
        peak0 = Peak(100, 10)
        peak1 = Peak(105, 15)
        peak0 += peak1

        self.assertEqual(peak0.mz, 205)
        self.assertEqual(peak0.intensity, 25)

"""Function tests of analyte match class"""
from unittest import TestCase

from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch, Peak, Precursor
from macdii.analyte_quantification import AnalyteQuantification


class AnalyteQuantificationTests(TestCase):
    """Test critical operations on AnalyteMatch"""


    def test_grouping_by_analyte(self):
        analyte0 = Analyte("test0", 50.0, 50.0, 50.0, 5, 5, 5, 5)
        analyte1 = Analyte("test1", 50.0, 50.0, 50.0, 5, 5, 5, 5)


        match0 = AnalyteMatch(
            analyte0,
            "foo.mzML",
            "scan=0",
            Precursor(10.0, 2),
            Peak(20.0, 100),
            None
        )
        match1 = AnalyteMatch(
            analyte1,
            "foo.mzML",
            "scan=1",
            Precursor(20.0, 2),
            Peak(30.0, 100),
            None
        )
        match2 = AnalyteMatch(
            analyte1,
            "foo.mzML",
            "scan=2",
            Precursor(30.0, 2),
            Peak(40.0, 100),
            None
        )
        match3 = AnalyteMatch(
            analyte0,
            "foo.mzML",
            "scan=3",
            Precursor(40.0, 2),
            Peak(50.0, 100),
            None
        )
        match4 = AnalyteMatch(
            analyte1,
            "foo.mzML",
            "scan=4",
            Precursor(50.0, 2),
            Peak(60.0, 100),
            None
        )

        matches = [match0, match1, match2, match3, match4]

        quantifiations = AnalyteQuantification.from_matches(matches)

        # self.assertEqual(len(quantifiations), 2)

        for quant in quantifiations:
            if quant.analyte == analyte0:
                self.assertEqual(quant.count, 2)
                self.assertEqual(quant.average_mz, 35)
                self.assertEqual(quant.average_intensity, 100)

            elif quant.analyte == analyte1:
                self.assertEqual(quant.count, 3)
                self.assertAlmostEqual(quant.average_mz, 43.33, 2)
                self.assertEqual(quant.average_intensity, 100)
            else:
                self.fail("Unexpected analyte in quantification")

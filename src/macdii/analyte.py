# std imports
import csv
from typing import List, TextIO, Tuple


class Analyte:
    """Analyte to be quantified and qualified."""

    def __init__(
        self,
        name: str,
        precursor_mz: float,
        quantifier_mz: float,
        qualifier_mz: float,
        precursor_mz_tolerance_lower: float,
        precursor_mz_tolerance_upper: float,
        fragment_mz_tolerance_lower: float,
        fragment_mz_tolerance_upper: float,
    ):
        self.name = name
        """Name of the analyte."""

        self.precursor_mz = precursor_mz
        """The precursor m/z of the analyte."""

        self.quantifier_mz = quantifier_mz
        """Fragment ion m/z for quantification."""

        self.qualifier_mz = qualifier_mz
        """Fragment ion m/z for qualification."""

        self.precursor_mz_range = self.__class__.calc_mz_range(
            precursor_mz, precursor_mz_tolerance_upper, precursor_mz_tolerance_lower
        )
        """The precursor m/z +/- tolerance for the analyte."""

        self.quantifier_mz_range = self.__class__.calc_mz_range(
            quantifier_mz, fragment_mz_tolerance_upper, fragment_mz_tolerance_lower
        )
        """Fragment ion m/z +/- tolerance for quantification."""

        self.qualifier_mz_range = self.__class__.calc_mz_range(
            qualifier_mz, fragment_mz_tolerance_upper, fragment_mz_tolerance_lower
        )
        """Fragment ion m/z +/- tolerance for qualification."""

    @classmethod
    def calc_mz_range(
        cls, mz: float, tolerance_upper_ppm: float, tolerance_lower_ppm: float
    ) -> Tuple[float, float]:
        """Calculate the m/z range given a tolerance."""
        tol_lower = mz / 1000000 * tolerance_lower_ppm
        tol_upper = mz / 1000000 * tolerance_upper_ppm
        return mz - tol_lower, mz + tol_upper

    def __str__(self) -> str:
        """Return a string representation of the analyte."""
        return (
            f"{self.name}: {self.precursor_mz} {self.quantifier_mz} {self.qualifier_mz}"
        )

    def precursor_contains(self, mz: float) -> bool:
        """Check if the precursor m/z range contains a given m/z."""
        return self.precursor_mz_range[0] <= mz <= self.precursor_mz_range[1]

    def quantifier_contains(self, mz: float) -> bool:
        """Check if the quantifier m/z range contains a given m/z."""
        return self.quantifier_mz_range[0] <= mz <= self.quantifier_mz_range[1]

    def qualifier_contains(self, mz: float) -> bool:
        """Check if the qualifier m/z range contains a given m/z."""
        return self.qualifier_mz_range[0] <= mz <= self.qualifier_mz_range[1]

    @classmethod
    def from_csv(
        cls,
        csv_content: TextIO,
        precursor_tolerance_lower: float,
        precursor_tolerance_upper: float,
        fragment_tolerance_lower: float,
        fragment_tolerance_upper: float,
    ) -> List["Analyte"]:
        """Read analytes from a CSV file."""
        analytes = []
        reader = csv.reader(
            csv_content,
        )
        # skip header
        next(reader)

        for row in reader:
            analytes.append(
                cls(
                    row[0],
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    precursor_tolerance_lower,
                    precursor_tolerance_upper,
                    fragment_tolerance_lower,
                    fragment_tolerance_upper,
                )
            )
        return analytes

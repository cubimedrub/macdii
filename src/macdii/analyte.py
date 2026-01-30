"""Functions for working with analytes."""

# std imports
import csv
from typing import List, Self, TextIO, Tuple


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
            precursor_mz, precursor_mz_tolerance_lower, precursor_mz_tolerance_upper
        )
        """The precursor m/z +/- tolerance for the analyte."""

        self.quantifier_mz_range = self.__class__.calc_mz_range(
            quantifier_mz, fragment_mz_tolerance_lower, fragment_mz_tolerance_upper
        )
        """Fragment ion m/z +/- tolerance for quantification."""

        self.qualifier_mz_range = self.__class__.calc_mz_range(
            qualifier_mz, fragment_mz_tolerance_lower, fragment_mz_tolerance_upper
        )
        """Fragment ion m/z +/- tolerance for qualification."""

    @classmethod
    def calc_mz_range(
        cls, mz: float, tolerance_lower_ppm: float, tolerance_upper_ppm: float
    ) -> Tuple[float, float]:
        """
        Calculate the m/z range given a tolerance.

        Parameters
        ----------
        mz : float
            The m/z value.
        tolerance_lower_ppm : float
            The lower tolerance in ppm.
        tolerance_upper_ppm : float
            The upper tolerance in ppm.
        """
        tol_lower = mz / 1000000 * tolerance_lower_ppm
        tol_upper = mz / 1000000 * tolerance_upper_ppm
        return mz - tol_lower, mz + tol_upper

    def __str__(self) -> str:
        """Return a string representation of the analyte."""
        return f"{self.name}"

    def precursor_contains(self, mz: float) -> bool:
        """
        Check if the precursor m/z range contains a given m/z.

        Parameters
        ----------
        mz : float
            The m/z to check.
        """
        return self.precursor_mz_range[0] <= mz <= self.precursor_mz_range[1]

    def quantifier_contains(self, mz: float) -> bool:
        """
        Check if the quantifier m/z range contains a given m/z.

        Parameters
        ----------
        mz : float
            The m/z to check.
        """
        return self.quantifier_mz_range[0] <= mz <= self.quantifier_mz_range[1]

    def qualifier_contains(self, mz: float) -> bool:
        """
        Check if the qualifier m/z range contains a given m/z.

        Parameters
        ----------
        mz : float
            The m/z to check.
        """
        return self.qualifier_mz_range[0] <= mz <= self.qualifier_mz_range[1]

    @classmethod
    def from_tsv(
        cls,
        csv_content: TextIO,
        precursor_tolerance_lower: float,
        precursor_tolerance_upper: float,
        fragment_tolerance_lower: float,
        fragment_tolerance_upper: float,
    ) -> List[Self]:
        """
        Read analytes from a TSV file.

        Parameters
        ----------
        csv_content : TextIO
            The CSV file or buffer
        precursor_tolerance_lower : float
            The lower precursor tolerance in ppm.
        precursor_tolerance_upper : float
            The upper precursor tolerance in ppm.
        fragment_tolerance_lower : float
            The lower fragment tolerance in ppm.
        fragment_tolerance_upper : float
            The upper fragment tolerance in ppm.
        """
        reader = csv.reader(
            csv_content,
            delimiter="\t"
        )
        # skip header
        next(reader)

        return [
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
            for row in reader
        ]

"""Module for a match between a targeted m/z and an observed m/z in a spectrum."""

# std imports
import csv
from typing import ClassVar, List, Self, TextIO, Tuple

# internal imports
from macdii.analyte import Analyte


class AnalyteMatch:
    """Represents a match between a targeted m/z and an observed m/z in a spectrum."""

    CSV_HEADER: ClassVar[Tuple[str, str, str, str, str]] = (
        "analyte",
        "filename",
        "spectrum_id",
        "mz",
        "intensity",
    )
    """Header for the TSV output."""

    def __init__(
        self,
        analyte: Analyte,
        filename: str,
        spectrum_id: str,
        mz: float,
        intensity: float,
    ):
        """Create a new match between a targeted m/z and an observed m/z in a spectrum.

        Parameters
        ----------
        analyte : Analyte
            Analyte.
        filename : str
            Filename of the mzML file containing the spectrum.
        spectrum_id : str
            ID of the spectrum.
        mz : float
            Observed m/z.
        intensity : float
            Intensity of the observed m/z.
        targeted_mz : float
            Targeted m/z for grouping
        """
        self.analyte = analyte
        self.filename = filename
        self.spectrum_id = spectrum_id
        self.mz = mz
        self.intensity = intensity

    def __str__(self) -> str:
        """Returns a TSV representation of the match."""
        return f"{self.analyte.name}\t{self.filename}\t{self.spectrum_id}\t{self.mz}\t{self.intensity}"

    @classmethod
    def to_tsv(cls, file: TextIO, matches: List[Self], add_header=False) -> None:
        """Write a list of AnalyteMatch objects to a TSV file."""
        writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
        if add_header:
            writer.writerow(cls.CSV_HEADER)
        for m in matches:
            writer.writerow(
                [m.analyte.name, m.filename, m.spectrum_id, m.mz, m.intensity]
            )


class Ms2AnalyteMatch(AnalyteMatch):
    """
    Represents a match between a targeted m/z and an observed m/z in a spectrum.
    In addition to the parent class, it also contains the experimental precursor m/z and a flag indicating if
    the analytes precursor m/z is matching the experimental one.
    """

    ADDITIONAL_CSV_HEADER: ClassVar[Tuple[str, str]] = (
        "experimental_precursor",
        "is_precursor_matching",
    )
    """Header for the TSV output."""

    def __init__(
        self,
        analyte: Analyte,
        filename: str,
        spectrum_id: str,
        mz: float,
        intensity: float,
        experimental_precursor: float,
    ):
        """Create a new match between a targeted m/z and an observed m/z in a spectrum.

        Parameters
        ----------
        analyte : Analyte
            Analyte.
        filename : str
            Filename of the mzML file containing the spectrum.
        spectrum_id : str
            ID of the spectrum.
        mz : float
            Observed m/z.
        intensity : float
            Intensity of the observed m/z.
        targeted_mz : float
            Targeted m/z for grouping
        experimental_precursor : float
            Experimental precursor m/z
        """
        super().__init__(analyte, filename, spectrum_id, mz, intensity)
        self.experimental_precursor = experimental_precursor
        self.is_precursor_matching = self.analyte.precursor_contains(
            self.experimental_precursor
        )

    @classmethod
    def to_tsv(
        cls,
        file: TextIO,
        matches: List[Self],
        add_header=False,
    ) -> None:
        """Write a list of AnalyteMatch objects to a TSV file."""
        writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
        if add_header:
            writer.writerow(list(cls.CSV_HEADER) + list(cls.ADDITIONAL_CSV_HEADER))
        for m in matches:
            writer.writerow(
                [
                    m.analyte.name,
                    m.filename,
                    m.spectrum_id,
                    m.mz,
                    m.intensity,
                    m.experimental_precursor,
                    m.is_precursor_matching,
                ]
            )

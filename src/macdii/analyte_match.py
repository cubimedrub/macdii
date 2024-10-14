"""Matches between analytes and MS1 and MS2 spectra."""

# std imports
from dataclasses import dataclass
from pathlib import Path
from typing import List, Self

# external imports
import pandas as pd

# internal imports
from macdii.analyte import Analyte
from macdii.utils import dataframe_to_file


@dataclass
class AnalyteMatch:
    """Match between analyte and MS1 spectrum."""

    analyte: Analyte
    """Analyte."""

    filename: str
    """Filename of the mzML file containing the spectrum."""

    spectrum_id: str
    """ID of the spectrum."""

    mz: float
    """Observed m/z."""

    intensity: float
    """Intensity of the observed m/z."""

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
    def to_file(cls, file_path: Path, matches: List[Self]) -> None:
        """Write a list of matches to a file."""
        df = pd.DataFrame(matches)
        dataframe_to_file(df, file_path)


@dataclass
class Ms2AnalyteMatch(AnalyteMatch):
    """
    Represents a match between a targeted m/z and an observed m/z in a spectrum.
    In addition to the parent class, it also contains the experimental precursor m/z and a flag indicating if
    the analytes precursor m/z is matching the experimental one.
    """

    analyte: Analyte
    """Analyte."""

    filename: str
    """Filename of the mzML file containing the spectrum."""

    spectrum_id: str
    """ID of the spectrum."""

    mz: float
    """Observed m/z."""

    intensity: float
    """Intensity of the observed m/z."""

    experimental_precursor: float
    """Experimental precursor m/z."""

    is_precursor_matching: bool
    """Flag indicating if the analytes precursor m/z is matching the experimental one."""

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
    def to_file(cls, file_path: Path, matches: List[Self]) -> None:
        """Write a list of matches to a file."""
        df = pd.DataFrame(matches)
        dataframe_to_file(df, file_path)

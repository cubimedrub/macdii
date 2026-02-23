"""Matches between analytes and MS1 and MS2 spectra."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, LiteralString, Optional, Self, Tuple

import pandas as pd

from macdii.analyte import Analyte
from macdii.utils import dataframe_to_file

DF_COLUMNS: Tuple[LiteralString, ...] = (
    "analyte",
    "filename",
    "spectrum_id",
    "theoretical_precursor_mz",
    "experimental_precursor_mz",
    "experimental_precursor_charge",
    "theoretical_quantifier_mz",
    "experimental_quantifier_mz",
    "experimental_quantifier_intensity",
    "theoretical_qualifier_mz",
    "experimental_qualifier_mz",
    "experimental_qualifier_intensity",
)


@dataclass
class Peak:
    mz: float
    intensity: int

    def __init__(self, mz: float, intensity: int):
        self.mz = mz
        self.intensity = intensity

    def to_tsv(self) -> str:
        return f"{self.mz}\t{self.intensity}"

    def __iadd__(self, value: Self):
        self.mz += value.mz
        self.intensity += value.intensity
        return self


@dataclass
class Precursor:
    mz: float
    charge: Optional[int]

    def __init__(self, mz: float, charge: Optional[int]):
        self.mz = mz
        self.charge = charge

    def to_tsv(self) -> str:
        return f"{self.mz}\t{self.charge}"

@dataclass
class AnalyteMatch:
    """Match between analyte and MS2 spectrum."""

    analyte: Analyte
    """Analyte."""

    filename: str
    """Filename of the mzML file containing the spectrum."""

    spectrum_id: str
    """ID of the spectrum."""

    experimental_precursor: Precursor
    """Experimental precursor m/z and charge."""

    experimental_quantifier: Peak
    """Experimental quantifier m/z and intensity."""

    experimental_qualifier: Optional[Peak]
    """Experimental qualifier m/z and intensity."""

    def __init__(
        self,
        analyte: Analyte,
        filename: str,
        spectrum_id: str,
        experimental_precursor: Precursor,
        experimental_quantifier: Peak,
        experimental_qualifier: Optional[Peak]
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
        experimental_precursor: Precursor
            Experimental precursor m/z and charge.
        experimental_quantifier: Peak
            Experimental quantifier m/z and intensity.
        experimental_qualifier: Optional[Peak]
            Experimental qualifier m/z and intensity.

        """
        self.analyte = analyte
        self.filename = filename
        self.spectrum_id = spectrum_id
        self.experimental_precursor = experimental_precursor
        self.experimental_quantifier = experimental_quantifier
        self.experimental_qualifier = experimental_qualifier

    def __str__(self) -> str:
        """Returns a TSV representation of the match."""
        experimental_qualifier = str(self.experimental_qualifier) if self.experimental_qualifier else ""
        return (
            f"{self.analyte.name}\t{self.filename}\t{self.spectrum_id}\t"
            f"{self.analyte.precursor_mz}\t{self.experimental_precursor}\t"
            f"{self.analyte.quantifier_mz}\t{self.experimental_quantifier}\t"
            f"{self.analyte.qualifier_mz}\t{experimental_qualifier}"
        )

    @classmethod
    def to_file(cls, file_path: Path, matches: List[Self]) -> None:
        """Write a list of matches to a file."""

        df_data = [
            [
                match.analyte.name,
                match.filename,
                match.spectrum_id,
                match.analyte.precursor_mz,
                match.experimental_precursor.mz,
                match.experimental_precursor.charge,
                match.analyte.quantifier_mz,
                match.experimental_quantifier.mz,
                match.experimental_quantifier.intensity,
                match.analyte.qualifier_mz,
                match.experimental_qualifier.mz if match.experimental_qualifier else None,
                match.experimental_qualifier.intensity if match.experimental_qualifier else None,
            ]
            for match in matches
        ]

        df = pd.DataFrame(df_data, columns=DF_COLUMNS)
        dataframe_to_file(df, file_path)

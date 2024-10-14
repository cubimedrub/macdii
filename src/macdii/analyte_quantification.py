"""Simple quantification of analytes."""

# std imports
from dataclasses import dataclass
from pathlib import Path
from typing import List, Self

# external imports
import pandas as pd

# internal imports
from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch
from macdii.utils import dataframe_to_file


@dataclass
class AnalyteQuantification:
    """Simple quantification of an analyte. Calculates the average m/z and intensity of a set of matches."""

    analyte: Analyte
    """Analyte."""

    mz_average: float
    """Average m/z of the matches."""

    intensity_average: float
    """Average intensity of the matches."""

    def __init__(self, matches: List[AnalyteMatch]):
        """
        Create a new quantification of an analyte.

        Parameters
        ----------
        matches : List[AnalyteMatch]
            List of matches between analytes quantifier and MS2 spectra

        Raises
        ------
        ValueError
            In case matches of different analytes are passed
        """

        # Checks that all matches have the same analyte
        if not all([matches[0].analyte.name == m.analyte.name for m in matches]):
            raise ValueError("All matches must have the same analyte.")

        self.analyte = matches[0].analyte
        self.mz_average = sum(m.mz for m in matches) / len(matches)
        self.intensity_average = sum(m.intensity for m in matches) / len(matches)

    def __str__(self) -> str:
        return f"{self.analyte.name}\t{self.mz_average}\t{self.intensity_average}"

    @classmethod
    def to_file(
        cls,
        file_path: Path,
        quantifications: List[Self],
    ) -> None:
        """Writes a list of AnalyteQuantification objects to a file.

        Parameters
        ----------
        file : BinaryIO
            Open file or buffer
        quantifications : List[&quot;AnalyteQuantification&quot;]
            List of quantifications to be written to the file
        """
        df = pd.DataFrame(quantifications)
        dataframe_to_file(df, file_path)

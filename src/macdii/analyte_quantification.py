"""Simple quantification of analytes."""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, LiteralString, Self, Tuple

import pandas as pd

from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch, Peak
from macdii.utils import dataframe_to_file

DF_COLUMNS: Tuple[LiteralString, ...] = (
    "analyte",
    "average_quantifier_mz",
    "average_quantifier_intensity",
    "count",
)

@dataclass
class AnalyteQuantification:
    """Simple quantification of an analyte. Calculates the average m/z and intensity of a set of matches."""

    analyte : Analyte
    """Analyte."""

    average_mz : float
    """Average m/z of the matches."""

    average_intensity : float
    """Average intensity of the matches."""

    count : int
    """Number of matches used for quantification."""

    def __init__(self, analyte: Analyte, sum_quantifier: Peak, count: int) -> None:
        """
        Create a new quantification of an analyte.

        Parameters
        ----------
        analyte : Analyte
            Analyte to be quantified
        sum_quantifier : Peak
            Peak quantifier to be used for quantification
        count : int
            Number of matches to be used for quantification
        """

        self.analyte = analyte
        self.average_mz = sum_quantifier.mz / count
        self.average_intensity = sum_quantifier.intensity / count
        self.count = count

    def __str__(self) -> str:
        return f"{self.analyte.name}\t{self.average_mz}\t{self.average_intensity}\t{self.count}"

    @classmethod
    def from_matches(cls, matches: List[AnalyteMatch]) -> List["AnalyteQuantification"]:
        """
        Create a new quantification of an analyte from a list of matches.

        Parameters
        ----------
        matches : List[AnalyteMatch]
            List of matches to be used for quantification

        Returns
        -------
        AnalyteQuantification
            New quantification of the analyte
        """

        quantifications: List[AnalyteQuantification] = []

        grouped_matches: Dict[str, List[AnalyteMatch]] = defaultdict(list)

        for match in matches:
            grouped_matches[match.analyte.name].append(match)

        for group in grouped_matches.values():
            sum_quantifier_peak = Peak(0, 0)
            for match in group:
                sum_quantifier_peak += match.experimental_quantifier

            quantifications.append(
                AnalyteQuantification(
                    group[0].analyte,
                    sum_quantifier_peak,
                    count = len(group)
                )
            )
        return quantifications

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

        df_data = [
            [
                quant.analyte.name,
                quant.average_mz,
                quant.average_intensity,
                quant.count
            ]
            for quant in quantifications
        ]


        df = pd.DataFrame(df_data, columns=DF_COLUMNS)
        dataframe_to_file(df, file_path)

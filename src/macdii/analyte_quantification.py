"""Simple quantification of analytes."""

# std imports
import csv
from typing import ClassVar, List, TextIO, Tuple

# internal imports
from macdii.analyte_match import AnalyteMatch


class AnalyteQuantification:
    """Simple quantification of an analyte. Calculates the average m/z and intensity of a set of matches."""

    CSV_HEADER: ClassVar[Tuple[str, str, str]] = (
        "analyte",
        "mz_average",
        "intensity_average",
    )
    """Header for the TSV output."""

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
    def to_tsv(
        cls,
        file: TextIO,
        quantifications: List["AnalyteQuantification"],
        add_header=False,
    ) -> None:
        """Writes a list of AnalyteQuantification objects to a TSV file.

        Parameters
        ----------
        file : TextIO
            Open file or buffer
        quantifications : List[&quot;AnalyteQuantification&quot;]
            List of quantifications to be written to the file
        add_header : bool, optional
            In case multiple quantifications needs to be written to the same file, this can be enables only for the first analyte, by default False
        """

        writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
        if add_header:
            writer.writerow(cls.CSV_HEADER)
        for q in quantifications:
            writer.writerow([q.analyte.name, q.mz_average, q.intensity_average])

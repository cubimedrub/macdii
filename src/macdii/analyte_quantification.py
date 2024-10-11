# std imports
import csv
from typing import ClassVar, List, TextIO, Tuple

# internal imports
from macdii.analyte_match import AnalyteMatch


class AnalyteQuantification:
    CSV_HEADER: ClassVar[Tuple[str, str, str]] = (
        "analyte",
        "mz_average",
        "intensity_average",
    )
    """Header for the TSV output."""

    def __init__(self, matches: List[AnalyteMatch]):
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
        writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC)
        if add_header:
            writer.writerow(cls.CSV_HEADER)
        for q in quantifications:
            writer.writerow([q.analyte.name, q.mz_average, q.intensity_average])

"""Various utility functions."""

# std imports
import csv
from pathlib import Path

# external imports
import pandas as pd


def time_to_seconds(time: float, unit_type: str) -> float:
    """Convert time to seconds.

    Parameters
    ----------
    time : float
        Time
    unit_type : str
        Source time unit, as described in UO ontology

    Returns
    -------
    float
        Time in seconds

    Raises
    ------
    ValueError
        If the time unit is unknown
    """
    match unit_type:
        case "second":
            return time
        case "minute":
            return time * 60
        case "hour":
            return time * 3600
        case _:
            raise ValueError(f"Unknown time unit `{unit_type}`")


def dataframe_to_file(dataframe: pd.DataFrame, file_path: Path) -> None:
    """Write a DataFrame to a file.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame
    file : Path
        File path

    Raises
    ------
    ValueError
        If the file type is unknown
    """
    match file_path.suffix:
        case ".tsv":
            dataframe.to_csv(
                file_path, sep="\t", quoting=csv.QUOTE_NONNUMERIC, index=False
            )
        case ".xlsx":
            dataframe.to_excel(file_path, index=False)
        case _:
            raise ValueError(f"Unknown file type `{file_path.suffix}`")

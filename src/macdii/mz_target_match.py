"""Module for a match between a targeted m/z and an observed m/z in a spectrum."""

# std imports
from typing import ClassVar


class MzTargetMatch:
    """Represents a match between a targeted m/z and an observed m/z in a spectrum."""

    CSV_HEADER: ClassVar[str] = (
        "filename\tspectrum_id\tms_level\trt\tmz\tintensity\ttargeted_mz"
    )
    """Header for the TSV output."""

    def __init__(
        self,
        filename: str,
        spectrum_id: str,
        ms_level: int,
        rt: float,
        mz: float,
        intensity: float,
        targeted_mz: float,
    ):
        """Create a new match between a targeted m/z and an observed m/z in a spectrum.

        Parameters
        ----------
        filename : str
            Filename of the mzML file containing the spectrum.
        spectrum_id : str
            ID of the spectrum.
        ms_level : int
            MS level of the spectrum.
        rt : float
            Retention time of the spectrum.
        mz : float
            Observed m/z.
        intensity : float
            Intensity of the observed m/z.
        targeted_mz : float
            Targeted m/z for grouping
        """
        self.filename = filename
        self.spectrum_id = spectrum_id
        self.ms_level = ms_level
        self.rt = rt
        self.mz = mz
        self.intensity = intensity
        self.targeted_mz = targeted_mz

    def __str__(self) -> str:
        """Returns a TSV representation of the match."""
        return f"{self.filename}\t{self.spectrum_id}\t{self.ms_level}\t{self.mz}\t{self.rt}\t{self.intensity}\t{self.targeted_mz}"

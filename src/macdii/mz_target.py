"""Module for representing a targeted m/z with a tolerance."""


class MzTarget:
    """Represents a targeted m/z with a tolerance."""

    def __init__(self, mz: float, tol_lower_ppm: float, tol_upper_ppm: float):
        """Create a new targeted m/z with a tolerance."""
        tol_lower = mz / 1000000 * tol_lower_ppm
        tol_upper = mz / 1000000 * tol_upper_ppm

        self.mz = mz
        self.mz_lower = mz - tol_lower
        self.mz_upper = mz + tol_upper

    def __contains__(self, mz: float) -> bool:
        return self.mz_lower <= mz <= self.mz_upper

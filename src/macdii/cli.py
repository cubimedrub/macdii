"""Command line interface for MaCDII."""

# std imports
import argparse
from pathlib import Path


class Cli:
    """Command line interface for MaCDII."""

    def __init__(self):
        """Create a new command line interface for MaCDII."""
        self.parser = argparse.ArgumentParser(
            prog="MaCDII",
            description=(
                "Mass Centric Direct Infusion Inspector "
                "for searching targeted m/z in mzML files."
            ),
        )

        self.parser.add_argument(
            "precursor_tol_lower",
            type=float,
            help="Lower precursor tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "precursor_tol_upper",
            type=float,
            help="Upper precursor tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "fragment_tol_lower",
            type=float,
            help="Lower fragment tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "fragment_tol_upper",
            type=float,
            help="Upper fragment tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "analytes_file",
            type=Path,
            help=(
                "CSV files with analytes. Columns: name, precursor mz, fragment quantifier mz, fragment qualifier mz"
            ),
        )

        self.parser.add_argument(
            "mzml_paths",
            type=Path,
            nargs="+",
            help="Paths to mzML files to search for targeted m/z.",
        )

    def parse(self) -> argparse.Namespace:
        """Parse the command line arguments."""
        return self.parser.parse_args()

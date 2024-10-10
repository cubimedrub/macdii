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
            "tol_lower",
            type=float,
            help="Lower tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "tol_upper",
            type=float,
            help="Upper tolerance in ppm for targeted m/z.",
        )

        self.parser.add_argument(
            "mz_target_list_path",
            type=Path,
            help=(
                "Path to a file containing a list of targeted m/z values. "
                "Simple txt files with one m/z value per line."
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

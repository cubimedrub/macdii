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
            "--output-type",
            type=str,
            default="tsv",
            choices=["tsv", "xlsx"],
            help="Output file type [default=tsv].",
        )

        self.parser.add_argument(
            "rt_start",
            type=float,
            help="Retention time start in seconds.",
        )

        self.parser.add_argument(
            "rt_stop",
            type=float,
            help="Retention time stop in seconds.",
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
                "TSV files with analytes. Columns: name, precursor mz, quantifier_mz, qualifier_mz"
            ),
        )

        self.parser.add_argument(
            "output_folder",
            type=Path,
            help=("Output folder to save the results."),
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

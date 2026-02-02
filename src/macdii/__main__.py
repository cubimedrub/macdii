"""Mass Centric Direct Infusion Inspector for searching targeted m/z in mzML files.
"""
from typing import List, Optional

from pyteomics.mzml import read as read_mzml

from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch, Peak, Precursor
from macdii.analyte_quantification import AnalyteQuantification
from macdii.cli import Cli
from macdii.utils import time_to_seconds


def main():
    """Main function for the MaCDII command line tool."""

    # Parse command line arguments
    args = Cli().parse()

    analytes = []
    with open(args.analytes_file, "r", encoding="utf-8") as file:
        analytes = Analyte.from_tsv(
            file,
            args.precursor_tol_lower,
            args.precursor_tol_upper,
            args.fragment_tol_lower,
            args.fragment_tol_upper,
        )

    # Create dictionaries to store matches for precursors, quantifiers, and qualifiers
    matching_fragments: List[AnalyteMatch] = []

    # Iterate over all mzML files and open them
    for mzml_path in args.mzml_paths:
        with mzml_path.open("rb") as mzml_file:
            mzml = read_mzml(mzml_file)
            # Iterate over all spectra in the mzML file
            for spectrum in mzml:
                # Get scan start time and check if it is within the specified range
                scan_start_time = time_to_seconds(
                    spectrum["scanList"]["scan"][0]["scan start time"],
                    spectrum["scanList"]["scan"][0]["scan start time"].unit_info,
                )
                if not args.rt_start <= scan_start_time <= args.rt_stop:
                    continue

                if spectrum["ms level"] != 2:
                    continue

                if len(spectrum["precursorList"])== 0:
                    continue

                precursor = Precursor(
                    spectrum["precursorList"]["precursor"][0][
                        "selectedIonList"
                    ]["selectedIon"][0]["selected ion m/z"],
                    spectrum["precursorList"]["precursor"][0][
                        "selectedIonList"
                    ]["selectedIon"][0]["charge state"],
                )

                # Check if any analyte matches on of the measured ions
                for analyte in analytes:
                    if not analyte.precursor_contains(precursor.mz):
                        continue

                    quantifier_peak: Optional[Peak] = None
                    qualifier_peak: Optional[Peak] = None

                    for ion_idx, ion in enumerate(spectrum["m/z array"]):
                        if analyte.quantifier_contains(ion):
                            quantifier_peak = Peak(
                                ion,
                                spectrum["intensity array"][ion_idx],
                            )
                        elif analyte.qualifier_contains(ion):
                            qualifier_peak = Peak(
                                ion,
                                spectrum["intensity array"][ion_idx],
                            )

                    if quantifier_peak is not None:
                        matching_fragments.append(
                            AnalyteMatch(
                                analyte,
                                mzml_path.name,
                                spectrum["id"],
                                precursor,
                                quantifier_peak,
                                qualifier_peak,
                            )
                        )

    # Write the matches to TSV files

    AnalyteMatch.to_file(
        args.output_folder.joinpath(f"quanitfier_matches.{args.output_type}"),
        matching_fragments
    )

    analyte_quantifications = AnalyteQuantification.from_matches(matching_fragments)

    AnalyteQuantification.to_file(args.output_folder.joinpath(f"quantification.{args.output_type}"), analyte_quantifications)


if __name__ == "__main__":
    main()

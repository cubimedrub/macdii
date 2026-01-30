"""Mass Centric Direct Infusion Inspector for searching targeted m/z in mzML files.
"""

# std imports
from collections import defaultdict
from pathlib import Path

# 3rd party imports
from pyteomics.mzml import read as read_mzml  # type: ignore[import-untyped]

# internal imports
from macdii.analyte_quantification import AnalyteQuantification
from macdii.cli import Cli
from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch, Ms2AnalyteMatch
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
    matching_precursors = defaultdict(list)
    matching_quantifiers = defaultdict(list)
    matching_qualifiers = defaultdict(list)

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
                # Check if any analyte matches on of the measured ions
                for analyte in analytes:
                    for ion_idx, ion in enumerate(spectrum["m/z array"]):
                        match spectrum["ms level"]:
                            case 1:
                                if not analyte.precursor_contains(ion):
                                    continue
                                # Add the match to the list of precursor matches
                                matching_precursors[analyte.name].append(
                                    AnalyteMatch(
                                        analyte,
                                        mzml_path.name,
                                        spectrum["id"],
                                        ion,
                                        spectrum["intensity array"][ion_idx],
                                    )
                                )
                            case 2:
                                if analyte.quantifier_contains(ion):
                                    # Add the match to the list of quantifier matches
                                    matching_quantifiers[analyte.name].append(
                                        Ms2AnalyteMatch(
                                            analyte,
                                            mzml_path.name,
                                            spectrum["id"],
                                            ion,
                                            spectrum["intensity array"][ion_idx],
                                            spectrum["precursorList"]["precursor"][0][
                                                "selectedIonList"
                                            ]["selectedIon"][0]["selected ion m/z"],
                                        )
                                    )
                                elif analyte.qualifier_contains(ion):
                                    # Add the match to the list of qualifier matches
                                    matching_qualifiers[analyte.name].append(
                                        Ms2AnalyteMatch(
                                            analyte,
                                            mzml_path.name,
                                            spectrum["id"],
                                            ion,
                                            spectrum["intensity array"][ion_idx],
                                            spectrum["precursorList"]["precursor"][0][
                                                "selectedIonList"
                                            ]["selectedIon"][0]["selected ion m/z"],
                                        )
                                    )

    # Write the matches to TSV files

    AnalyteMatch.to_file(
        args.output_folder.joinpath(f"precursor_matches.{args.output_type}"),
        [match for matches in matching_precursors.values() for match in matches],
    )

    Ms2AnalyteMatch.to_file(
        args.output_folder.joinpath(f"quantifier_matches.{args.output_type}"),
        [match for matches in matching_quantifiers.values() for match in matches],
    )

    Ms2AnalyteMatch.to_file(
        args.output_folder.joinpath(f"qualifier_matches.{args.output_type}"),
        [match for matches in matching_qualifiers.values() for match in matches],
    )

    AnalyteQuantification.to_file(
        args.output_folder.joinpath(f"quantification.{args.output_type}"),
        [
            AnalyteQuantification(matches)
            for matches in matching_quantifiers.values()
            if len(matches) > 0
        ],
    )


if __name__ == "__main__":
    main()

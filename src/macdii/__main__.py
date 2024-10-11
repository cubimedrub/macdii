"""Mass Centric Direct Infusion Inspector for searching targeted m/z in mzML files.
"""

# std imports
from collections import defaultdict
import csv
from pathlib import Path
from typing import DefaultDict, List

# 3rd party imports
from pyteomics.mzml import read as read_mzml  # type: ignore[import-untyped]

# internal imports
from macdii.analyte_quantification import AnalyteQuantification
from macdii.cli import Cli
from macdii.analyte import Analyte
from macdii.analyte_match import AnalyteMatch, Ms2AnalyteMatch

# from macdii.mz_target_matches_grouped import MzTargetMatchesGrouped


def main():
    """Main function for the MaCDII command line tool."""

    # Parse command line arguments
    args = Cli().parse()

    analytes = []
    with open(args.analytes_file, "r", encoding="utf-8") as file:
        analytes = Analyte.from_csv(
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
                                            spectrum["selectedIonList"][0][
                                                "selected ion m/z"
                                            ],
                                        )
                                    )

    # Write the matches to TSV files
    with Path("./precursor_matches.tsv").open("w", encoding="utf-8") as file:
        add_header = True
        for values in matching_precursors.values():
            AnalyteMatch.to_tsv(file, values, add_header)
            add_header = False

    with Path("./quantifier_matches.tsv").open("w", encoding="utf-8") as file:
        add_header = True
        for values in matching_quantifiers.values():
            Ms2AnalyteMatch.to_tsv(file, values, add_header)
            add_header = False

    with Path("./qualifier_matches.tsv").open("w", encoding="utf-8") as file:
        add_header = True
        for values in matching_qualifiers.values():
            Ms2AnalyteMatch.to_tsv(file, values, add_header)
            add_header = False

    with Path("./quantification.tsv").open("w", encoding="utf-8") as file:
        quantifications = [
            AnalyteQuantification(matches)
            for matches in matching_quantifiers.values()
            if len(matches) > 0
        ]

        AnalyteQuantification.to_tsv(file, quantifications, add_header=True)


if __name__ == "__main__":
    main()

"""Mass Centric Direct Infusion Inspector for searching targeted m/z in mzML files.
"""

# std imports
from pathlib import Path
from typing import List

# 3rd party imports
from pyteomics.mzml import read as read_mzml  # type: ignore[import-untyped]

# internal imports
from macdii.cli import Cli
from macdii.mz_target import MzTarget
from macdii.mz_target_match import MzTargetMatch
from macdii.mz_target_matches_grouped import MzTargetMatchesGrouped


def main():
    """Main function for the MaCDII command line tool."""

    # Parse command line arguments
    args = Cli().parse()

    # Read mz_target_list, remove empty lines and duplicates and convert to float

    mz_target_list = args.mz_target_list_path.read_text(encoding="utf-8").split("\n")
    mz_target_list = list(filter(lambda x: x != "", mz_target_list))
    mz_target_list = list({float(mz) for mz in mz_target_list})

    # Create MzTarget objects
    mz_target_list = [
        MzTarget(mz, args.tol_lower, args.tol_upper) for mz in mz_target_list
    ]

    # Read mzML files and search for matches
    target_matches: List[MzTargetMatch] = []  # type: ignore[annotation-unchecked]

    # Iterate over all mzML files and open them
    for mzml_path in args.mzml_paths:
        with mzml_path.open("rb") as mzml_file:
            mzml = read_mzml(mzml_file)
            # Iterate over all spectra in the mzML file
            for spectrum in mzml:
                # Check each ion in the spectrum for a match with the targeted m/z
                for mz_target in mz_target_list:
                    for ion_idx, ion in enumerate(spectrum["m/z array"]):
                        if ion not in mz_target:
                            continue
                        target_matches.append(
                            MzTargetMatch(
                                mzml_path.name,
                                spectrum["id"],
                                spectrum["ms level"],
                                spectrum["scanList"]["scan"][0]["scan start time"],
                                ion,
                                spectrum["intensity array"][ion_idx],
                                mz_target.mz,
                            )
                        )

    # Write target_matches to a TSV file
    with Path("./target_matches.tsv").open(
        "w", encoding="utf-8"
    ) as target_matches_file:
        target_matches_file.write(MzTargetMatch.CSV_HEADER + "\n")
        for target_match in target_matches:
            target_matches_file.write(str(target_match) + "\n")

    # Group target_matches by targeted m/z and write to a TSV file
    target_matches_grouped = MzTargetMatchesGrouped(target_matches)
    keys = target_matches_grouped.keys()
    keys.sort()

    # Write average m/z, average intensity and count for each targeted m/z
    with Path("./target_matches_grouped.tsv").open(
        "w", encoding="utf-8"
    ) as target_matches_grouped_file:
        target_matches_grouped_file.write(MzTargetMatchesGrouped.TSV_HEADER + "\n")
        for key in keys:
            average_mz = sum(
                target_matches.mz for target_matches in target_matches_grouped[key]
            ) / len(target_matches_grouped[key])
            average_intensity = sum(
                target_matches.intensity
                for target_matches in target_matches_grouped[key]
            ) / len(target_matches_grouped[key])

            target_matches_grouped_file.write(
                f"{key}\t{average_mz}\t{average_intensity}\t{len(target_matches_grouped[key])}\n"
            )


if __name__ == "__main__":
    main()

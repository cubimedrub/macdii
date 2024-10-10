"""Grouped MzTargetMatch objects by targeted m/z."""

# std imports
from collections import defaultdict
from typing import ClassVar, DefaultDict, List

# internal imports
from macdii.mz_target_match import MzTargetMatch


class MzTargetMatchesGrouped:
    """MzTargetMatch objects grouped by targeted m/z."""

    TSV_HEADER: ClassVar[str] = "targeted_mz\taverage_mz\taverage_intensity\tcount"
    """Header for the TSV output."""

    def __init__(self, target_matches: List[MzTargetMatch]):
        """Create a new group of MzTargetMatch objects.

        Parameters
        ----------
        targeted_mz : float
            Targeted m/z for the group.
        """
        self.target_matches_grouped: DefaultDict[float, List[MzTargetMatch]] = (
            defaultdict(list)
        )

        for target_match in target_matches:
            self.target_matches_grouped[target_match.targeted_mz].append(target_match)

    def keys(self) -> List[float]:
        """Return the targeted m/z values of the group."""
        return list(self.target_matches_grouped.keys())

    def __getitem__(self, targeted_mz: float) -> List[MzTargetMatch]:
        """Return the MzTargetMatch objects for a targeted m/z."""
        return self.target_matches_grouped[targeted_mz]

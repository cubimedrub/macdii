"""Various utility functions."""


def time_to_seconds(time: float, unit_type: str) -> float:
    """Convert time to seconds.

    Parameters
    ----------
    time : float
        Time
    unit_type : str
        Source time unit, as described in UO ontology

    Returns
    -------
    float
        Time in seconds

    Raises
    ------
    ValueError
        If the time unit is unknown
    """
    match unit_type:
        case "second":
            return time
        case "minute":
            return time * 60
        case "hour":
            return time * 3600
        case _:
            raise ValueError(f"Unknown time unit `{unit_type}`")

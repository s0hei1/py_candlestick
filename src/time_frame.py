from dataclasses import dataclass

@dataclass(frozen=True)
class TimeFrame:
    name : str
    included_m1 : int | None

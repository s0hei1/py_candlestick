from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TimeFrame:
    name: str
    included_m1: int
    mt5_value: int | None = None
    fractal_value: int | None = None


    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, TimeFrame):
            raise TypeError

        return self.included_m1 == other.included_m1

    def __lt__(self, other):
        if not isinstance(other, TimeFrame):
            raise TypeError
        return self.included_m1 < other.included_m1

    def __gt__(self, other):
        if not isinstance(other, TimeFrame):
            raise TypeError
        return self.included_m1 > other.included_m1

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
from dataclasses import dataclass
from typing import Sequence

@dataclass
class Indicator:
    name : str
    values : Sequence[float]

    def __len__(self):
        return len(self.values)

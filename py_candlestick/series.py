from collections.abc import Callable
from dataclasses import dataclass
from numpy._typing import NDArray

@dataclass
class Series:
    name : str
    values : NDArray

    def __len__(self):
        return len(self.values)

@dataclass
class Indicator(Series):

    calculator_method : Callable




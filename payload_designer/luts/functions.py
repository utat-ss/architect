"""Lookup table (LUT) utilities."""

# stdlib
import logging
from pathlib import Path

# external
import astropy.units as unit
import numpy as np
import pandas as pd

LOG = logging.getLogger(__name__)

index = {}


class LUT:
    """A lookup table implementation. Initialized from a csv file containing x
    data in the first column, f(x) data in the second column. The header should
    contain the units of the x and y data.

    Args:
        path: The path to the CSV data file containing LUT data.

    """

    def __init__(self, path: Path, name: str = None):
        data = pd.read_csv(path, skipinitialspace=True)

        unit_x = data.columns[0] if data.columns[0].lower() != "none" else ""
        unit_y = data.columns[1] if data.columns[1].lower() != "none" else ""

        self.x = unit.Quantity(value=data.iloc[:, 0], unit=unit_x)
        self.y = unit.Quantity(value=data.iloc[:, 1], unit=unit_y)
        self.name = name

    def get_table(self):
        assert self.x is not None, "x must be specified."
        assert self.y is not None, "y must be specified."
        
        data = {f"X [{self.x.unit}]": self.x.value, f"Y [{self.y.unit}]": self.y.value}

        df = pd.DataFrame.from_dict(data)

        return df

    def __str__(self):
        df = self.get_table()
        return f"LUT ({self.name})\n{df.to_string(index=False)}"

    def _repr_html_(self):
        assert self.name is not None, "Name must be specified."
        df = self.get_table()
        return f"LUT ({self.name})\n{df.to_html(index=False)}"

    def __call__(self, x):
        """Linearly interpolate the LUT at given x value(s).

        Args:
            x (array-like): The x value(s) to interpolate at.

        Returns:
            array-like: The interpolated y values.

        """
        assert self.x is not None, "x must be specified."
        assert self.y is not None, "y must be specified."
        return np.interp(x=x, xp=self.x, fp=self.y)


def build_index(search_path: Path):
    for item in search_path.iterdir():
        if item.is_file() and item.suffix == ".csv":
            name = item.relative_to(Path(__file__).parent).with_suffix("").as_posix()
            index[name] = item

        elif item.is_dir():
            build_index(search_path=item)

        else:
            LOG.debug(
                f"{item} is not a recognzied LUT filetype or directory. Ignoring."
            )


def load(name: str):
    lut = LUT(path=index[name], name=name)
    return lut


build_index(Path(__file__).parent)

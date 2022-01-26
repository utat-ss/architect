"""An assortment of utilities and classes for scientific computing."""

# external
import numpy as np


class LUT:
    """A lookup table implementation. Initialized from a csv file containing x
    data in the first column, f(x) data in the second column.

    Args:
        data_path (path-like): The path to the CSV data file containing LUT data.

    """

    def __init__(self, data_path):
        data = np.genfromtxt(fname=data_path, delimiter=",")
        self.x = data[:, 0]
        self.y = data[:, 1]

    def __call__(self, x):
        """Interpolate the LUT at a given x value(s).

        Args:
            x (array-like): The x value to interpolate at.

        Returns:
            array-like: The interpolated y values.

        """
        return np.interp(x=x, xp=self.x, fp=self.y)
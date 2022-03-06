"""An assortment of utilities and classes for scientific computing."""

# external
import numpy as np


class LUT:
    """A lookup table implementation. Initialized from a csv file containing x
    data in the first column, f(x) data in the second column.

    Args:
        path (path-like): The path to the CSV data file containing LUT data.
        scale (float): The scale factor to apply to the LUT data.

    """

    def __init__(self, path, scale=(1, 1)):
        data = np.genfromtxt(fname=path, delimiter=",")
        self.x = data[:, 0]
        self.y = data[:, 1]
        self.scale(scale[0], scale[1])

    def scale(self, scl_x, scl_y):
        """Scale the LUT data by a given factor.

        Args:
            scl (tuple[float, float]): The scale factor to apply to the LUT x and y data.

        """
        self.x *= scl_x
        self.y *= scl_y

    def __call__(self, x):
        """Interpolate the LUT at a given x value(s).

        Args:
            x (array-like): The x value(s) to interpolate at.

        Returns:
            array-like: The interpolated y values.

        """
        return np.interp(x=x, xp=self.x, fp=self.y)


def orient_tensor(a, dim: int, dims: int) -> np.ndarray:
    """Orient a tensor in a given dimensionality.

    Args:
        a: array tensor.
        dim: index of the dimension axis on which to orient the tensor.
        dims: dimensionality of the tensor space.

    Returns:
        The oriented tensor.

    """
    shape = [1] * dims
    shape[dim] = -1

    return np.reshape(a=a, newshape=shape)


def orient_and_broadcast(a, dim: int, shape) -> np.ndarray:
    """Orient and broadcast a tensor into a given dimensionality.

    Args:
        a: array tensor.
        dim: index of the dimension axis on which to orient the tensor.
        shape: dimensionality and size of broadcasted tensor.

    Returns:
        The broadcasted tensor.

    """

    a = orient_tensor(a=a, dim=dim, dims=len(shape))
    a = np.broadcast_to(array=a, shape=shape)

    return a


def convert_dark_current_density_to_dark_current(i_dark, p):
    """Convert dark current density to dark current.

    Args:
        i_A: dark current density [nA/cm^2].
        p: pixel pitch [um].

    Returns:
        dark current in ke-/px/s

    """
    p *= 1e-6  # um to m
    p = p ** 2  # m to m^2/px

    i_dark *= 1e-9  # nA/cm^2 to A/cm^2
    i_dark *= 1e4  # A/cm^2 to A/m^2

    i_dark *= 6.242e18  # A/m^2 to e-/m^2/s
    i_dark *= p  # e-/m^2/s to e-/px/s

    i_dark *= 1e-3  # e-/px/s to ke-/px/s

    return i_dark

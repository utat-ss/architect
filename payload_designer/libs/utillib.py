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

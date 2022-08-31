"""An assortment of utilities and classes for scientific computing."""
# external
import numpy as np
from astropy.units.quantity import Quantity


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

    a_oriented = orient_tensor(a=a, dim=dim, dims=len(shape))
    a_broadcasted = np.broadcast_to(array=a_oriented, shape=shape)

    if isinstance(a, Quantity):
        a_broadcasted *= a.unit

    return a_broadcasted

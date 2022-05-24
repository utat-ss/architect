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


def convert_dark_current_density_to_dark_current(i_dark, p):
    """Convert dark current density to dark current.

    Args:
        i_A: dark current density [nA/cm^2].
        p: pixel pitch [um].

    Returns:
        dark current in ke-/px/s

    """
    p *= 1e-6  # um to m
    p = p**2  # m to m^2/px

    i_dark *= 1e-9  # nA/cm^2 to A/cm^2
    i_dark *= 1e4  # A/cm^2 to A/m^2

    i_dark *= 6.242e18  # A/m^2 to e-/m^2/s
    i_dark *= p  # e-/m^2/s to e-/px/s

    i_dark *= 1e-3  # e-/px/s to ke-/px/s

    return i_dark

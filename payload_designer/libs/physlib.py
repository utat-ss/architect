"""Physics-related helper functions."""

# external
import numpy as np


def snell_angle_2(angle_1, n_1, n_2):
    """Calculate the angle of refraction of a ray travelling between two mediums
    according to Snell's law.

    Args:
        angle_1 (array_like[float]): angle of incidence with respect to surface normal
            in radians.
        n_1 (float): index of refraction in first medium.
        n_2 (float): index of refraction in second medium.

    Returns:
        float: angle of refraction in radians.
    """
    angle_2 = np.arcsin(n_1 / n_2 * np.sin(angle_1))

    return angle_2

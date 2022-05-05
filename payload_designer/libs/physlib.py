"""Physics-related helper functions."""

# external
import numpy as np


def snell(angle, n_1, n_2):
    """Calculate the angle of refraction of a ray travelling between two mediums
    according to Snell's law.

    Args:
        angle: Angle of incidence with respect to surface normal.
        n_1: Index of refraction in first medium.
        n_2: Index of refraction in second medium.

    """
    angle_2 = np.arcsin(n_1 / n_2 * np.sin(angle))

    return angle_2

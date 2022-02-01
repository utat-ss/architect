"""Foreoptics components."""

# stdlib
import logging
import math
from pathlib import Path

# external
import numpy as np
import scipy.constants as sc

# project
from payload_designer.libs import utillib

LOG = logging.getLogger(__name__)


class Foreoptic:
    """Foreoptic component.

    Args:
        a_in_max (float, optional): maximum angle of incidence in degrees. Defaults to None.
        b (float, optional): source radiance. Defaults to None.
        dm_a (float, optional): aperture diameter. Defaults to None.
        ds_i (float, optional): image distance. Defaults to None.
        ds_o (float, optional): object distance. Defaults to None.
        eta (LUT, optional) transmittace LUT object. Defaults to None.
        g (float, optional): geometric etendue. Defaults to None.
        n (float, optional): f-number. Defaults to None.
        na (float, optional): numerical aperture. Defaults to None.
        s (float, optional): area of emitting source. Defaults to None.

    """

    def __init__(
        self,
        a_in_max=None,
        b=None,
        dm_a=None,
        ds_i=None,
        ds_o=None,
        eta=None,
        g=None,
        n=None,
        na=None,
        s=None,
    ):
        self.a_in_max = a_in_max
        self.b = b
        self.dm_a = dm_a
        self.ds_i = ds_i
        self.ds_o = ds_o
        self.eta = eta
        self.g = g
        self.n = n
        self.na = na
        self.s = s

    def get_aperture_diameter(self):
        """Calculate the aperture diamter.

        Returns:
            float: aperture diameter (mm).

        """
        assert self.ds_i is not None, "ds_i is not set."

        if self.n is not None:
            dm_a = np.divide(self.ds_i, self.n)
        elif self.na is not None:
            dm_a = 2 * np.multiply(self.ds_i, self.na)
        else:
            raise ValueError("n or na must be set.")

        return dm_a

    def get_magnification(self):
        """Calculate the magnification of the foreoptics.

        Returns:
            float: magnification (unitless).

        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        m = np.divide(self.ds_i, self.ds_o)

        return m

    def get_f_number(self):
        """Calculate the f number (f/#).

        Returns:
            float: f/# (unitless).

        """
        if self.na is not None:
            n = np.divide(1, 2 * self.na)
        elif self.ds_i is not None and self.dm_a is not None:
            n = np.divide(self.ds_i, self.dm_a)
        else:
            raise ValueError("ds_i and dm_a or na must be set.")

        return n

    def get_effective_focal_length(self):
        """Calculate the effective focal length.

        Returns:
            float: effective focal length (length).

        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        efl = np.divide(self.ds_o + self.ds_i, np.multiply(self.ds_o, self.ds_i))

        return efl

    def get_numerical_aperture(self):
        """Calculate the numerical aperture.

        Returns:
            float: numerical aperture (unitless).

        """

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion

        if a_in_max is not None:
            na = np.sin(a_in_max)
        elif self.n is not None:
            na = np.divide(1, 2 * self.n)
        else:
            raise ValueError("a_in_max or n must be set.")

        return na

    def get_geometric_etendue(self):
        """Calculate the geometric etendue.

        Returns:
            float: geometric etendue (length^2).

        """
        assert self.s is not None, "s is not set."
        assert self.a_in_max is not None, "a_in_max is not set."

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion

        g = np.multiply(np.pi, np.multiply(self.s, np.power(np.sin(a_in_max), 2)))

        return g

    def get_radiant_flux(self):
        """Calculate the flux.

        Returns:
            float: flux (watt).

        """
        assert self.b is not None, "b is not set."
        assert self.g is not None, "g is not set."

        f = np.multiply(self.b, self.g)

        return f

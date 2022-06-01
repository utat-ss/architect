"""Foreoptic component classes."""

# stdlib
import logging
import math

# external
import astropy.constants as const
import astropy.units as unit
import numpy as np

# project
from payload_designer import luts
from payload_designer.components import Component
from payload_designer.luts import LUT

LOG = logging.getLogger(__name__)


class Foreoptic(Component):
    """Foreoptic component."""

    def __init__(
        self,
        diameter=None,
        focal_length=None,
        mass=None,
        length=None,
        transmittance: LUT = None,
    ):
        super().__init__(mass=mass, dimensions=(diameter, diameter, length))

        self.diameter = diameter
        self.focal_length = focal_length
        self.length = length
        self.transmittance = transmittance

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

    def get_image_area(self):
        """Calculate the image area.

        Returns:
            float: image area [mm^2].

        """
        assert self.d_i is not None, "d_i is not set."

        a_i = math.pi * (self.d_i / 2) ** 2

        return a_i


class Chromar(Foreoptic):
    def __init__(self):
        super().__init__(
            diameter=80 * unit.mm,
            focal_length=100 * unit.mm,
            mass=250 * unit.g,
            length=100 * unit.mm,
            transmittance=None,
        )

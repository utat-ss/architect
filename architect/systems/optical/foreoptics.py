"""Foreoptic component classes."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np
from astropy.units import Quantity

# project
from architect.luts import LUT
from architect.systems.optical.lenses import Lens

LOG = logging.getLogger(__name__)


class Foreoptic(Lens):
    """Foreoptic component."""

    def __init__(
        self,
        diameter: unit.m = None,
        image_diameter: unit.m = None,
        focal_length: unit.m = None,
        mass: unit.kg = None,
        length: unit.m = None,
        transmittance: Quantity[unit.percent] | LUT = None,
    ):
        super().__init__(
            diameter=diameter,
            focal_length=focal_length,
            mass=mass,
            thickness=length,
            transmittance=transmittance,
        )
        self.image_diameter = image_diameter

    def get_diameter(self):
        """Get the diameter."""

        if self.diameter is not None:
            return self.diameter
        else:
            raise ValueError("Diameter is not set.")

    def get_image_diameter(self):
        """Get the image diameter."""
        if self.image_diameter is not None:
            return self.image_diameter
        else:
            raise ValueError("Image diameter is not set.")

    def get_image_area(self):
        """Calculate the image area from the image diameter."""
        assert self.image_diameter is not None, "image_diameter must be set."

        area = np.pi * (self.image_diameter / 2) ** 2

        return area

    def get_f_number(self):
        """Calculate the f number (f/#).

        Returns:
            float: f/# (unitless).

        """
        assert self.focal_length is not None, "focal_length must be set."
        assert self.diameter is not None, "diameter must be set."

        n = self.focal_length / self.diameter

        return n

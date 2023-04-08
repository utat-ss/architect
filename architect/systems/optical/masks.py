"""Slit component classes."""

# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.systems import Component

LOG = logging.getLogger(__name__)


class RectSlit(Component):
    """Rectangular slit component."""

    def __init__(
        self,
        mass=None,
        diameter=None,
        thickness=None,
        size: tuple = None,
        clear_area: unit.m**2 = None,
    ):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.size = size
        self.thickness = thickness
        self.diameter = diameter
        self.clear_area = clear_area

    def get_size(self):
        """Get the size of the slit."""
        if self.size is not None:
            return self.size
        else:
            raise ValueError("Size must be set.")

    def get_clear_area(self):
        """Get the clear aperture slit area."""
        if self.clear_area is not None:
            area = self.clear_area
        else:
            area = self.get_size()[0] * self.get_size()[1]

        return area.flatten()

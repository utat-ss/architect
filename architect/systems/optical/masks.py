"""Slit component classes."""

# stdlib
import logging

# project
from architect.systems import Component

LOG = logging.getLogger(__name__)


class RectSlit(Component):
    """Rectangular slit component."""

    def __init__(self, mass=None, diameter=None, thickness=None, size: tuple = None):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.size = size
        self.thickness = thickness
        self.diameter = diameter

    def get_size(self):
        """Get the size of the slit."""
        if self.size is not None:
            return self.size
        else:
            raise ValueError("Slit size not set.")

    def get_clear_area(self):
        """Get the clear aperture slit area."""
        assert self.size is not None, "Size must be specified."

        area = self.size[0] * self.size[1]

        return area

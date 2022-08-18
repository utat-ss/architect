"""Slit component classes."""

# stdlib
import logging
import math

# external
import numpy as np

# project
from payload_designer.components import Component

LOG = logging.getLogger(__name__)


class RectSlit(Component):
    """Rectangular slit component.

    Args:
        size: dimensions of slit (width, height) in satelite reference frame.

    """

    def __init__(self, mass=None, diameter=None, thickness=None, size: tuple = None):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.size = size
        self.thickness = thickness
        self.diameter = diameter

    def get_clear_area(self):
        """Get the clear aperture slit area."""
        assert self.size is not None, "Size must be specified."
        
        area = self.size[0] * self.size[1]

        return area

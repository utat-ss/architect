"""Lens component classes."""

# stdlib
import logging

# external
import astropy.constants as const
import numpy as np

# project
from payload_designer.components import Component
from payload_designer.luts import LUT

LOG = logging.getLogger(__name__)


class Lens(Component):
    """Generic lens component.

    Modelled using thin lens (paraxial) approximations.

    Args:
        index: Index of refraction of the lens.

    """

    def __init__(
        self,
        diameter=None,
        focal_length=None,
        index=None,
        mass=None,
        thickness=None,
        transmittance: LUT = None,
    ):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.focal_length = focal_length
        self.index = index
        self.transmittance = transmittance
        self.diameter = diameter
        self.thickness = thickness

    def get_image_height(self, incident_angle):
        """Get the height of the image formed above or below the optical axis of
        the lens for an incoming beam of collimated light."""
        assert self.focal_length is not None, "Focal length must be specified."
        
        image_height = self.focal_length * np.tan(incident_angle)

        return image_height

    def get_volume(self):
        """Get the volume of the lens."""
        assert self.diameter is not None, "Diameter must be specified."
        
        volume = const.pi * (self.diameter / 2) ** 2 * self.thickness

        return volume

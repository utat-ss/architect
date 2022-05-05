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

    """

    def __init__(
        self,
        mass=None,
        diameter=None,
        thickness=None,
        transmittace: LUT = None,
        focal_length=None,
    ):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.transmittace = transmittace
        self.focal_length = focal_length

    def get_image_height(self, incident_angle):
        """Get the height of the image formed above or below the optical axis of
        the lens for an incoming beam of collimated light."""

        image_height = self.focal_length * np.tan(incident_angle)

        return image_height

    def get_volume(self):
        """Get the volume of the lens."""

        volume = const.pi * (self.diameter / 2) ** 2 * self.thickness

        return volume

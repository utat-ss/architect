"""Lens component classes."""

# stdlib
import logging

# external
import astropy.constants as const
import numpy as np

# project
from architect.components import Component
from architect.luts import LUT

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
        transmittance: int | LUT = None,
    ):
        super().__init__(mass=mass, dimensions=(diameter, diameter, thickness))
        self.focal_length = focal_length
        self.index = index
        self.transmittance = transmittance
        self.diameter = diameter
        self.thickness = thickness

    def get_image_height(self, incident_angle):
        """Get the height of the image formed above or below the optical axis of
        the lens for an incoming beam of collimated light.

        Ref: https://www.notion.so/utat-ss/Image-Height-2533dc2983e742148c80ea44b2c11d5c

        """
        assert self.focal_length is not None, "Focal length must be specified."

        image_height = self.focal_length * np.tan(incident_angle)

        return image_height

    def get_focal_length(self):
        """Get the focal length."""
        if self.focal_length is not None:
            return self.focal_length
        else:
            raise ValueError("Focal length not set.")

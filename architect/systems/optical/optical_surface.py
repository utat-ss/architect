"""An optical surface component."""

# external
import astropy.units as unit
import numpy as np

# project
from architect.systems import Component


class OpticalSurface(Component):
    """An optical surface is a component that can refract light."""

    def __init__(self, medium_index=None):
        super().__init__()
        self.medium_index = medium_index

    def angle_of_refraction(self, incident_angle: unit.deg, incident_index) -> unit.deg:
        """Get the angle of refraction for a given incident angle.

        Ref: https://www.notion.so/utat-ss/Angle-of-Refraction-a4c5f3235ad941398137dd3560eec717

        """
        assert self.medium_index is not None, "medium_index must be set."

        angle_of_refraction = np.arcsin(
            incident_index * np.sin(incident_angle) / self.medium_index
        )

        return angle_of_refraction.to(unit.deg)

"""Filter component classes."""

# stdlib
import logging

# external
import numpy as np

# project
from architect.components.lenses import Lens
from architect.luts import LUT

LOG = logging.getLogger(__name__)


class DichroicBandFilter(Lens):
    """Dichroic bandpass filter component."""

    def __init__(
        self,
        diameter=None,
        index=None,
        mass=None,
        thickness=None,
        transmittance: LUT = None,
    ):
        super().__init__(
            diameter=diameter,
            focal_length=None,
            index=index,
            mass=mass,
            thickness=thickness,
            transmittance=transmittance,
        ),

    def get_phase_shift(self, wavelength, angle_in, index_in=1):
        """Get the phase shift of the filter."""
        assert self.index is not None, "Index must be specified."
        
        wavelength_shifted = wavelength * np.sqrt(
            1 - ((index_in, self.index) * np.sin(angle_in) ** 2)
        )

        return wavelength_shifted

    def get_reflectance(self, index_in=1):
        """Get the reflectance of the filter."""
        assert self.index is not None, "Index must be specified."

        reflectance = ((self.index - index_in) / (self.index + index_in)) ** 2

        return reflectance

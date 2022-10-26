"""Optical component class."""
# external
import astropy.units as unit
import numpy as np
from astropy.units import Quantity

# project
from architect.luts import LUT
from architect.systems import Component, System


class OpticalComponent(Component):
    """A component with optical properties."""

    def __init__(
        self,
        dimensions: tuple[unit.m, unit.m, unit.m] = None,
        mass: unit.kg = None,
        volume: unit.m**3 = None,
        density: unit.kg / unit.m**3 = None,
        index=None,
        transmittance: Quantity[unit.pct] | LUT = None,
        **systems: System
    ):
        super().__init__(
            dimensions=dimensions, mass=mass, volume=volume, density=density, **systems
        )
        self.index = index
        self.transmittance = transmittance

    def get_transmittance(self, wavelength=None):
        """Get the transmittance."""
        if self.transmittance is not None:
            if isinstance(self.transmittance, LUT):
                transmittance = self.transmittance(wavelength)
            else:
                transmittance = self.transmittance

            transmittance = transmittance * np.prod(
                [
                    component.get_transmittance(wavelength)
                    for component in self.systems
                    if isinstance(component, OpticalComponent)
                ]
            )
            return transmittance
        else:
            raise ValueError("transmittance is not set.")

    def get_index(self):
        """Get the index of refraction."""
        if self.index is not None:
            return self.index
        else:
            raise ValueError("index is not set.")

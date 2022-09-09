"""Sensor component classes."""

# stdlib
import logging
import math

# external
import astropy.units as unit
import numpy as np

# project
from architect import luts
from architect.components import Component
from architect.luts import LUT

LOG = logging.getLogger(__name__)


class Sensor(Component):
    """Generic focal plane array sensor component.

    Args:
        dimensions: Dimensions of component bounding box. Elements are ordered as (x, y, z) in the cubesat frame.
        dt: Integration time.
        efficiency: Quantum efficiency of the sensor.
        i_dark: Dark current.
        mass: Component mass.
        n_bin: Number of binning operations performed on image aquisition.
        n_bit: Sensor bit depth.
        n_px: Pixel count in the (x, y) dimensions in cubesat frame.
        n_well: Sensor well depth.
        noise_read: Readout noise.
        pitch: Pixel pitch. The distance between the centerpoints of adjacent pixels.

    """

    def __init__(
        self,
        dimensions: tuple = None,
        dt=None,
        efficiency: LUT = None,
        i_dark=None,
        mass=None,
        n_bin=None,
        n_bit=None,
        n_px: tuple = None,
        n_well=None,
        noise_read=None,
        pitch=None,
    ):
        super().__init__(dimensions, mass)
        self.dt = dt
        self.efficiency = efficiency
        self.i_dark = i_dark
        self.n_bin = n_bin
        self.n_bit = n_bit
        self.n_px = n_px
        self.n_well = n_well
        self.noise_read = noise_read
        self.pitch = pitch

    def get_shape(self) -> tuple:
        """Get the dimensions of the sensor face."""
        assert self.n_px is not None, "n_px must be specified."
        assert self.pitch is not None, "Pitch must be specified."

        size = (self.n_px[0] * self.pitch, self.n_px[1] * self.pitch)

        return size

    def get_area(self):
        """Get the area of the sensor face."""

        shape = self.get_shape()

        area = shape[0] * shape[1]

        return area

    def get_pixel_area(self):
        """Get the area of a single detector element (pixel).

        Assumes square pixels.

        """
        assert self.pitch is not None, "Pitch must be specified."

        pixel_area = self.pitch**2

        return pixel_area

    def get_dark_noise(self):
        """Get the dark noise of the sensor."""
        assert self.i_dark is not None, "i_dark must be specified."
        assert self.dt is not None, "dt amplitude must be specified."

        dark_noise = self.i_dark * self.dt

        return dark_noise

    def get_quantization_noise(self):
        """Get the quantization noise of the sensor."""
        assert self.n_well is not None, "n_well must be specified."
        assert self.n_bit is not None, "n_bit must be specified."

        quant_noise = (1 / math.sqrt(12)) * self.n_well / 2**self.n_bit.value

        return quant_noise

    def get_noise(self, signal):
        """Get the net noise of the sensor."""
        assert self.n_bin is not None, "n_bin must be specified."
        assert self.noise_read is not None, "noise_read must be specified."

        noise = np.sqrt(
            signal
            + self.n_bin * self.get_dark_noise() ** 2
            + self.get_quantization_noise() ** 2
            + self.n_bin * self.noise_read**2
        )

        return noise


class TauSWIR(Sensor):
    """Teledyne FLIR Tau SWIR sensor.

    Ref: https://www.notion.so/utat-ss/FLIR-Tau-SWIR-407ea145ffea4d188c777f3b17a9be2b

    """

    def __init__(self):
        ke = 1e3 * unit.electron
        super().__init__(
            dimensions=(38, 38, 36) * unit.mm,
            dt=166.7 * unit.ms,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            i_dark=140 * (ke / unit.pix / unit.s),
            mass=81 * unit.g,
            n_bin=1 * unit.dimensionless_unscaled,
            n_bit=14 * unit.bit,
            n_px=(640, 512) * unit.pix,
            n_well=19 * ke,
            noise_read=500 * unit.electron,
            pitch=15 * unit.um,
        )

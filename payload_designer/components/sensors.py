"""Sensor components."""

# stdlib
import logging
import math
from pathlib import Path

# external
import numpy as np
import scipy.constants as sc
from payload_designer.components.basecomponent import BaseComponent

# project
from payload_designer.libs import utillib

LOG = logging.getLogger(__name__)


class Sensor(BaseComponent):
    """Sensor component model.

    Args:
        M (float, optional): Mass [g]. Defaults to None.
        V (tuple[float, float, float], optional): Volume envelope in x,y,z [mm]. Defaults to None.
        dt (float, optional): Integration time [ms]. Defaults to None.
        eta_sensor (LUT, optional): quantum efficiency LUT object. Defaults to None.
        i_dark (int, optional): Dark current [ke-/px/s]. Defaults to None.
        n_bin (int, optional): Number of binning operations performed on image aquisition. Defaults to None.
        n_bit (int, optional): Sensor bit depth. Defaults to None.
        n_well (int, optional): Well depth [e-/px]. Defaults to None.
        p (float, optional): Pixel pitch [µm]. Defaults to None.
        px_x (int, optional): Pixel count in cross-track direction [px]. Defaults to None.
        px_y (int, optional): Pixel count in along-track direction [px]. Defaults to None.
        sigma_read (int, optional): Readout noise [e-/px]. Defaults to None.

    """

    def __init__(
        self,
        M=None,
        V=None,
        dt=None,
        eta_sensor=None,
        i_dark=None,
        n_bin=None,
        n_bit=None,
        n_well=None,
        p=None,
        px_x=None,
        px_y=None,
        sigma_read=None,
    ):
        self.M = M
        self.V = V
        self.dt = dt
        self.eta_sensor = eta_sensor
        self.i_dark = i_dark
        self.n_bin = n_bin
        self.n_bit = n_bit
        self.n_well = n_well
        self.p = p
        self.px_x = px_x
        self.px_y = px_y
        self.sigma_read = sigma_read

    def get_snr(self, L_target, eta_optics, f_n, lmbda):
        """Calculates the signal to noise ratio from the sensor and system
        parameters.

        Args:
            L_target (LUT): atmospheric radiance LUT object [nm, W/sr/m2/nm].
            eta_optics (array-like[float]): transmittance of the optical system by wavelength [nm].
            f_n (float): f-number of optical system.
            lmbda (array-like[float]): wavelengths at which to evaluate SNR [nm].

        Returns:
            array-like[float]: SNR by wavelength.

        """
        assert self.n_bin is not None, "n_bin is not set."
        assert self.dt is not None, "dt is not set."
        assert self.eta_sensor is not None, "eta_sensor is not set."
        assert self.i_dark is not None, "i_dark is not set."
        assert self.n_bit is not None, "n_bit is not set."
        assert self.n_well is not None, "n_well is not set."
        assert self.p is not None, "p is not set."
        assert self.sigma_read is not None, "sigma_read is not set."

        # region unit conversions
        L_target.scale(1e-9, 1e9)  # (nm, W/sr/m2/nm) to (m, W/sr/m2/m)
        dt = self.dt * 1e-3  # ms to s
        i_dark = self.i_dark * 1e3  # ke-/px/s to e-/px/s
        lmbda = lmbda * 1e-9  # nm to m
        n_well = self.n_well * 1e3  # ke- to e-
        p = self.p * 1e-6  # µm to m
        self.eta_sensor.scale(1e-9, 1)  # nm to m
        # endregion

        # region signal
        A_d = p ** 2

        s_target = (
            (sc.pi / 4)
            * (lmbda / (sc.h * sc.c))
            * (A_d / f_n ** 2)
            * self.eta_sensor(lmbda)
            * eta_optics
            * L_target(lmbda)
            * dt
        )
        print(f"Signal: {s_target}")
        # endregion

        # region noise
        sigma_dark = i_dark * dt
        LOG.debug(f"Dark noise: {sigma_dark} [e-/px]")

        sigma_quantization = (1 / math.sqrt(12)) * n_well / 2**self.n_bit
        LOG.debug(f"Quantization noise: {sigma_quantization} [e-/px]")

        noise = np.sqrt(
            s_target
            + self.n_bin * sigma_dark ** 2
            + sigma_quantization ** 2
            + self.n_bin * self.sigma_read ** 2
        )
        LOG.debug(f"Noise: {noise}")
        # endregion

        snr = s_target / noise

        return snr, s_target, noise


class TauSWIR(Sensor):
    """Tau SWIR sensor class."""

    def __init__(self):
        super().__init__(
            self,
            eta_sensor=utillib.LUT(Path("data/sensor_tauswir_quantum_efficiency.csv")),
            p=15,
            i_dark=140,
            dt=166.7,
            n_bin=1,
            n_bit=14,
            n_well=19,
            sigma_read=500,
        )

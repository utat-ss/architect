# stdlib
import math

# external
import astropy.constants as const
import astropy.units as unit
import numpy as np
import pandas as pd

# project
from payload_designer import components
from payload_designer.components import Component
from payload_designer.components.lenses import Lens
from payload_designer.luts import LUT
from payload_designer.systems import System


class Payload(System):
    def __init__(self, **components: Component):

        for name, component in components.items():
            setattr(self, name, component)

        self.components = list(components.values())

    def get_mass(self):
        """Get the mass of the system."""
        mass = 0
        for component in self.components:
            mass += component.mass

        return mass

    def get_volume(self):
        """Get the net volume of the system."""
        volume = 0
        for component in self.components:
            volume += component.get_volume()

        return volume


class HyperspectralImager(Payload):
    def __init__(
        self,
        sensor: Component = None,
        foreoptic: Component = None,
        slit: Component = None,
        **components: Component,
    ):
        super().__init__(sensor=sensor, foreoptic=foreoptic, slit=slit, **components)

    def get_specification_tables(self):
        pass

    def get_transmittance(self):
        """Get the net optical transmittance of the system by accounting for the
        transmittance losses of all lens components."""
        transmittance = 1
        for component in self.components:
            if isinstance(component, Lens):
                transmittance *= component.transmittance

        return transmittance

    def get_ratio_cropped_light_through_slit(self):
        """Get the ratio of the light passing through slit to the image of the
        foreoptic."""
        assert (
            self.foreoptic.image_diameter is not None
        ), "Foreoptic image diameter must be set."

        effective_width = min(self.slit.size[0], self.foreoptic.image_diameter)
        effective_slit_area = effective_width * self.slit.size[1]
        ratio = effective_slit_area / self.foreoptic.get_image_area()

        return ratio

    def get_signal_to_noise(self, radiance: LUT, wavelength):
        """Get the signal to noise ratio of the system.

        Args:
            radiance: Atmospheric radiance incident on the system by wavelength.
            wavelength: Wavelength(s) at which to evaluate SNR.

        """

        # print("wavelength", wavelength)
        # print("ratio", self.get_ratio_cropped_light_through_slit())
        # print("pixel area", self.sensor.get_pixel_area())
        # print("f num", self.foreoptic.get_f_number())
        # print("QE", self.sensor.efficiency(wavelength).decompose() * unit.electron)
        # print("efficiency", self.sensor.efficiency(wavelength))
        # print("transmittance", self.get_transmittance())
        # print("area", self.slit.get_area())
        # print("radiance", radiance(wavelength))
        # print("sensor dt", self.sensor.dt)
        # print("n bin", self.sensor.n_bin)
        # print("dark noise", self.sensor.get_dark_noise())
        # print("quantization noise", self.sensor.get_quantization_noise())
        # print("noise read", self.sensor.noise_read)

        signal1 = (
            (wavelength / (const.h * const.c))
            * radiance(wavelength)
            * (math.pi / 4)
            * self.sensor.dt
        )  # [sr-1 m-3]
        signal2 = self.sensor.get_pixel_area() / (
            ((self.foreoptic.get_f_number()).decompose()) ** 2 * 1 / unit.sr
        )  # [m2 sr]
        signal3 = (
            (self.sensor.efficiency(wavelength)).decompose()
            * unit.electron
            * self.get_transmittance()
        )  # [electrons]
        signal4 = (
            self.get_ratio_cropped_light_through_slit() * 800 * 10 ** (-9) * unit.meter
        )  # [dimensionless]

        signal = signal1 * signal2 * signal3 * signal4

        print("signal", signal.decompose())

        print("shot noise sqr", signal.decompose() * unit.electron)
        print(
            "dark noise sqr",
            self.sensor.n_bin * (self.sensor.get_dark_noise() * unit.pix) ** 2,
        )
        print("quantization noise sqr", self.sensor.get_quantization_noise() ** 2)
        print("read noise sqr", self.sensor.n_bin * self.sensor.noise_read**2)

        noise = np.sqrt(
            (signal * unit.electron)
            + self.sensor.n_bin * (self.sensor.get_dark_noise() * unit.pix) ** 2
            + self.sensor.get_quantization_noise() ** 2
            + self.sensor.n_bin * self.sensor.noise_read**2
        )

        snr = signal / noise

        return snr.decompose()

    def get_FOV(self) -> np.ndarray[float, float]:
        """Get the field of view vector.

        A vector that defines the angular extent that can be imaged by the payload in
        the along-track and the across-track directions.

        """

        fov = 2 * np.arctan(self.slit.size / (2 * self.foreoptic.focal_length))

        return fov

    def get_iFOV(self) -> np.ndarray[float, float]:
        """Get the instantaneous field of view."""
        iFOV = 2 * np.arctan(self.sensor.pitch / (2 * self.foreoptic.focal_length))

        return iFOV

    def get_sensor_spatial_resolution(self, target_distance, skew_angle):
        """Get the sensor-limited spatial resolution."""

        iFOV = self.get_iFOV()

        spatial_resolution = target_distance * (
            np.tan(skew_angle + 1 / 2 * iFOV) - np.tan(skew_angle - 1 / 2 * iFOV)
        )

        return spatial_resolution

    def get_swath(
        self, altitude, skew_angle: np.ndarray[float, float]
    ) -> np.ndarray[float, float]:
        """Get the swath vector.

        Args:
            altitude: the orbital altitude.
            skew_angle: the skew angles in the across and along-track directions.

        """

        fov = self.get_FOV()

        swath = altitude * (
            np.tan(skew_angle + 0.5 * fov) - np.tan(skew_angle - 0.5 * fov)
        )

        return swath

    def get_optical_spatial_resolution(self, wavelength, target_distance, skew_angle):
        """Get the optically-limited spatial resolution."""

        optical_spatial_resolution = (
            1.22
            * (wavelength * target_distance)
            / (self.foreoptic.diameter * np.cos(skew_angle))
        )

        return optical_spatial_resolution

    def get_spatial_resolution(self, wavelength, target_distance, skew_angle):
        """Get the spatial resolution or ground sample distance of the
        system."""

        sensor_spatial_resolution = self.get_sensor_spatial_resolution(
            target_distance=target_distance, skew_angle=skew_angle
        )
        optical_spatial_resolution = self.get_optical_spatial_resolution(
            wavelength=wavelength,
            target_distance=target_distance,
            skew_angle=skew_angle,
        )

        spatial_resolution = np.max(
            sensor_spatial_resolution, optical_spatial_resolution
        )

        return spatial_resolution


class FINCHEye(HyperspectralImager):
    def __init__(
        self,
        foreoptic: Component,
        slit: Component,
        collimator: Component,
        bandfilter: Component,
        grism: Component,
        focuser: Component,
    ):
        super().__init__(
            foreoptic=foreoptic,
            slit=slit,
            collimator=collimator,
            bandfilter=bandfilter,
            grism=grism,
            focuser=focuser,
            sensor=components.sensors.TauSWIR(),
        )

    def get_dimensions(self):
        """Get the dimensions of the net bounding box of the system.

        Assumes in-line configuration with respect to z-axis of satellite frame.

        """

        dim_x = max(component.dimension[0] for component in self.components)
        dim_y = max(component.dimension[1] for component in self.components)
        dim_z = sum(component.dimension[2] for component in self.components)

        dimensions = (dim_x, dim_y, dim_z)

        return dimensions

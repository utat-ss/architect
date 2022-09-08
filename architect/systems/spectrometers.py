# stdlib
import math

# external
import astropy.constants as const
import astropy.units as unit
import numpy as np

# project
from architect import components
from architect.components import Component
from architect.components.lenses import Lens
from architect.luts import LUT
from architect.systems import System


class HyperspectralImager(System):
    """A hyperspectral imager class.

    A hyperspectral imager captures light and diffracts it into a spectrum which is then
    imaged.

    """

    def __init__(
        self,
        foreoptic: Lens = None,
        slit: Component = None,
        diffractor: Component = None,
        sensor: Component = None,
        **components: Component,
    ):
        super().__init__(
            foreoptic=foreoptic,
            slit=slit,
            diffractor=diffractor,
            sensor=sensor,
            **components,
        )

    def get_transmittance(self):
        """Get the net optical transmittance of the system by accounting for the
        transmittance losses of all lens components."""

        transmittance = 100 * unit.percent
        for component in self.components:
            if isinstance(component, Lens):
                transmittance *= component.transmittance

        return transmittance

    def get_ratio_cropped_light_through_slit(self):
        """Get the ratio of the light area passing through the slit to the area
        of the image of the foreoptic."""
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
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."
        assert self.slit is not None, "A slit component must be specified."

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
        )  # [electron]
        signal4 = (
            self.get_ratio_cropped_light_through_slit()
            * (800 * 10 ** (-9))
            * unit.meter
        )  # [dimensionless * m]

        signal = signal1 * signal2 * signal3 * signal4

        print("signal", signal.decompose())

        print("shot noise sqr", signal.decompose() * unit.electron)
        print(
            "dark noise sqr",
            self.sensor.n_bin * (self.sensor.get_dark_noise() * unit.pix) ** 2,
        )
        print("quantization noise sqr", (self.sensor.get_quantization_noise()) ** 2)
        print("read noise sqr", self.sensor.n_bin * (self.sensor.noise_read) ** 2)

        noise = np.sqrt(
            (signal * unit.electron)
            + self.sensor.n_bin * (self.sensor.get_dark_noise() * unit.pix) ** 2
            + self.sensor.get_quantization_noise() ** 2
            + self.sensor.n_bin * self.sensor.noise_read**2
        )

        snr = signal / noise

        return snr.decompose()

    def get_FOV(self):
        """Get the field of view vector.

        A vector that defines the angular extent that can be imaged by the payload in
        the along-track and the across-track directions.

        """
        assert self.slit is not None, "A slit component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        fov = 2 * np.arctan(self.slit.size / (2 * self.foreoptic.focal_length))

        return fov

    def get_iFOV(self):
        """Get the instantaneous field of view."""
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        iFOV = 2 * np.arctan(self.sensor.pitch / (2 * self.foreoptic.focal_length))

        return iFOV

    def get_sensor_spatial_resolution(self, target_distance):
        """Get the sensor-limited spatial resolution."""

        spatial_resolution = (
            target_distance * self.sensor.pitch / self.foreoptic.focal_length
        )

        return spatial_resolution.decompose()

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

    def get_optical_spatial_resolution(self, wavelength, target_distance, skew_angle=0):
        """Get the optically-limited spatial resolution.

        Aka GRD (ground-resolved distance)

        """
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        optical_spatial_resolution = (
            1.22
            * (wavelength * target_distance)
            / (self.foreoptic.diameter * np.cos(skew_angle))
        )

        return optical_spatial_resolution

    def get_spatial_resolution(self, wavelength, target_distance, skew_angle=0):
        """Get the spatial resolution of the system."""
        if self.spatial_resolution is not None:
            return self.spatial_resolution

        sensor_spatial_resolution = self.get_sensor_spatial_resolution(
            target_distance=target_distance
        )

        optical_spatial_resolution = self.get_optical_spatial_resolution(
            wavelength=wavelength,
            target_distance=target_distance,
            skew_angle=skew_angle,
        )

        spatial_resolution = np.maximum(
            sensor_spatial_resolution, optical_spatial_resolution
        )

        return spatial_resolution

    def get_sensor_spectral_resolution(self, upper_wavelength, lower_wavelength):
        """Get the sensor-limited spectral resolution."""
        assert self.sensor is not None, "A sensor component must be specified."

        sensor_spectral_resolution = (upper_wavelength - lower_wavelength) / (
            (1 / self.sensor.n_bin) * self.sensor.n_px[1]
        )

        return sensor_spectral_resolution

    def get_optical_spectral_resolution(self, target_wavelength, beam_diameter):
        """Get the optically-limited spectral resolution."""
        assert self.diffractor is not None, "A diffractor component must be specified."

        optical_spectral_resolution = (
            target_wavelength
            / self.diffractor.get_resolvance(beam_diameter=beam_diameter)
        )

        return optical_spectral_resolution

    def get_spectral_resolution(
        self,
        upper_wavelength,
        lower_wavelength,
        target_wavelength,
        beam_diameter,
    ):
        """Get the spectral resolution (from the optical and sensor spectral
        resolutions)"""

        sensor_spectral_resolution = self.get_sensor_spectral_resolution(
            upper_wavelength=upper_wavelength,
            lower_wavelength=lower_wavelength,
        )

        optical_spectral_resolution = self.get_optical_spectral_resolution(
            target_wavelength=target_wavelength, beam_diameter=beam_diameter
        )

        print("Optical spectral resolution: ", optical_spectral_resolution)
        print("Sensor spectral resolution: ", sensor_spectral_resolution)
        spectral_resolution = np.maximum(
            optical_spectral_resolution, sensor_spectral_resolution * unit.pix
        )

        return spectral_resolution

    def get_pointing_accuracy_constraint(
        self, wavelength, target_distance, tolerance=0.5
    ):
        """Get the pointing accuracy constraint."""

        spatial_resolution = self.get_spatial_resolution(
            wavelength=wavelength, target_distance=target_distance
        )

        constraint_angle = np.arctan((tolerance * spatial_resolution) / target_distance)

        return constraint_angle


class FINCHEye(HyperspectralImager):
    """A compact hyperspectral imaging payload."""

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

    def get_mapped_height_sensor(self, wavelength):
        """Get height on sensor that given wavelength hits."""

        incident_angle = self.grism.get_emergent_angle(
            incident_angle=0, wavelength=wavelength, order=1
        )
        image_height = self.focuser.get_image_height(incident_angle=incident_angle)

        return image_height
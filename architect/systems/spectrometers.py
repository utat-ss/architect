# stdlib
import logging
import math

# external
import astropy.constants as const
import astropy.units as unit
import numpy as np

# project
from architect.components import Component
from architect.components.lenses import Lens
from architect.components.sensors import Sensor, TauSWIR
from architect.luts import LUT
from architect.systems import System

LOG = logging.getLogger(__name__)


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
        sensor: Sensor = None,
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
                transmittance *= (
                    component.transmittance
                    if component.transmittance is not None
                    else 1
                )

        return transmittance

    def get_ratio_cropped_light_through_slit(self):
        """Get the ratio of the light area passing through the slit to the area
        of the image of the foreoptic.

        Ref: https://www.notion.so/utat-ss/Ratio-of-Cropped-Light-through-Slit-d49a933b72fe40738c3ebeecd5b37491

        """
        assert self.foreoptic is not None, "Foreoptic must be set"
        assert self.slit is not None, "Slit must be set"

        effective_width = min(
            self.slit.get_size()[0], self.foreoptic.get_image_diameter()
        )

        effective_slit_area = effective_width * self.slit.get_size()[1]
        ratio = effective_slit_area / self.foreoptic.get_image_area()

        return ratio

    def get_signal_to_noise(self, radiance: LUT, wavelength):
        """Get the signal to noise ratio of the system.

        Ref: https://www.notion.so/utat-ss/Signal-to-Noise-6a3a5b8b744d41ada40410d5251cc8ac

        """

        snr = signal / self.get_noise()

        return snr

    def get_signal(wavelength):
        """Get the signal.

        Ref: https://www.notion.so/utat-ss/Signal-1819461a3a2b4fdeab8b9c26133ff8e2

        """
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."
        assert self.slit is not None, "A slit component must be specified."

        signal1 = (
            (wavelength / (const.h * const.c))
            * radiance(wavelength)
            * (math.pi / 4)
            * self.sensor.get_integration_time()
        )  # [sr-1 m-3]
        assert signal1.unit == unit.sr**-1 * unit.m**-3
        signal2 = self.sensor.get_pixel_area() / (
            ((self.foreoptic.get_f_number()).decompose()) ** 2 * 1 / unit.sr
        )  # [m2 sr]
        assert signal2.unit == unit.m**2 * unit.sr
        signal3 = (
            (self.sensor.get_efficiency(wavelength)).decompose()
            * unit.electron
            * self.get_transmittance()
        )  # [electron]
        assert signal3.unit == unit.electron
        signal4 = (
            self.get_ratio_cropped_light_through_slit()
            * (800 * 10 ** (-9))
            * unit.meter
        )  # [dimensionless * m]
        assert signal4.unit == unit.m

        signal = signal1 * signal2 * signal3 * signal4
        LOG.info(f"Signal: {signal.decompose()}")

        return signal

    def get_noise(self):
        """Get the noise.

        Ref: https://www.notion.so/utat-ss/Noise-21ff532ac4334fbeab4aabf6372c9848

        """
        noise = np.sqrt(
            (signal.decompose() * unit.electron)
            + self.sensor.get_n_bin() * (self.sensor.get_dark_noise() * unit.pix) ** 2
            + self.sensor.get_quantization_noise() ** 2
            + self.sensor.get_n_bin() * self.sensor.get_noise_read() ** 2
        )

        return noise

    def get_FOV(self):
        """Get the field of view vector.

        A vector that defines the angular extent that can be imaged by the payload in
        the along-track and the across-track directions.

        """
        assert self.slit is not None, "A slit component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        fov = 2 * np.arctan(self.slit.get_size() / (2 * self.foreoptic.focal_length))

        return fov

    def get_iFOV(self):
        """Get the instantaneous field of view."""
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        iFOV = 2 * np.arctan(self.sensor.pitch / (2 * self.foreoptic.focal_length))

        return iFOV

    def get_sensor_spatial_resolution(self, target_distance):
        """Get the sensor-limited spatial resolution.

        Ref: https://www.notion.so/utat-ss/Sensor-Limited-Spectral-Resolution-5071f076997f4b59851f73127822fb23

        """
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        spatial_resolution = (
            target_distance
            * self.sensor.get_pitch()
            / self.foreoptic.get_focal_length()
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

    def get_optical_spatial_resolution(self, wavelength, target_distance, skew_angle=0):
        """Get the optically-limited spatial resolution.

        Ref: https://www.notion.so/utat-ss/Optically-Limited-Spatial-Resolution-3216b483a563420fa1f5bd0e74e2fe8e

        """
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        optical_spatial_resolution = (
            1.22
            * (wavelength * target_distance)
            / (self.foreoptic.get_diameter() * np.cos(skew_angle))
        )

        return optical_spatial_resolution

    def get_spatial_resolution(self, wavelength, target_distance, skew_angle=0):
        """Get the spatial resolution of the system.

        Ref: https://www.notion.so/utat-ss/Absolute-Spatial-Resolution-bd475362664e46578b113ff3bfb51e76

        """

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
        """Get the sensor-limited spectral resolution.

        Ref: https://www.notion.so/utat-ss/Sensor-Limited-Spectral-Resolution-5071f076997f4b59851f73127822fb23

        """
        assert self.sensor is not None, "A sensor component must be specified."

        sensor_spectral_resolution = (upper_wavelength - lower_wavelength) / (
            (1 / self.sensor.get_n_bin()) * self.sensor.get_n_px()[1]
        )

        return sensor_spectral_resolution

    def get_optical_spectral_resolution(self, target_wavelength, beam_diameter):
        """Get the optically-limited spectral resolution.

        Ref: https://www.notion.so/utat-ss/Optically-Limited-Spectral-Resolution-97de793cf58b477584bf363937d2e3e4

        """
        assert self.diffractor is not None, "A diffractor component must be specified."

        optical_spectral_resolution = (
            target_wavelength
            / self.diffractor.get_resolvance(beam_diameter=beam_diameter)
        )

        return optical_spectral_resolution

    def get_spectral_resolution(
        self,
        lower_wavelength,
        upper_wavelength,
        target_wavelength,
        beam_diameter,
    ):
        """Get the spectral resolution (from the optical and sensor spectral
        resolutions)

        Ref: https://www.notion.so/utat-ss/Absolute-Spectral-Resolution-214e60ee8ad144c0b0b2af577a383f9d

        """

        sensor_spectral_resolution = self.get_sensor_spectral_resolution(
            upper_wavelength=upper_wavelength,
            lower_wavelength=lower_wavelength,
        )

        optical_spectral_resolution = self.get_optical_spectral_resolution(
            target_wavelength=target_wavelength, beam_diameter=beam_diameter
        )

        spectral_resolution = np.maximum(
            optical_spectral_resolution, sensor_spectral_resolution * unit.pix
        )

        return spectral_resolution

    def get_pointing_accuracy_constraint(
        self, wavelength, target_distance, tolerance=0.5
    ):
        """Get the pointing accuracy constraint.

        Ref: https://www.notion.so/utat-ss/Pointing-Accuracy-vs-Spatial-Resolution-0a257bf7271142548f57bf220ca4af36

        """

        spatial_resolution = self.get_spatial_resolution(
            wavelength=wavelength, target_distance=target_distance
        )

        constraint_angle = np.arctan((tolerance * spatial_resolution) / target_distance)

        return constraint_angle


class FINCHEye(HyperspectralImager):
    """A compact hyperspectral imaging payload."""

    def __init__(
        self,
        foreoptic: Component = None,
        slit: Component = None,
        collimator: Component = None,
        bandfilter: Component = None,
        grism: Component = None,
        focuser: Component = None,
    ):
        super().__init__(
            foreoptic=foreoptic,
            slit=slit,
            collimator=collimator,
            bandfilter=bandfilter,
            diffractor=grism,
            focuser=focuser,
            sensor=TauSWIR(),
        )
        self.grism = grism

    def get_dimensions(self):
        """Get the dimensions of the net bounding box of the system.

        Assumes in-line configuration with respect to z-axis of satellite frame.

        """

        dim_x = max(
            component.dimensions[0]
            for component in self.components
            if component is not None
        )
        dim_y = max(
            component.dimensions[1]
            for component in self.components
            if component is not None
        )
        dim_z = sum(
            component.dimensions[2]
            for component in self.components
            if component is not None
        )

        dimensions = (dim_x, dim_y, dim_z)

        return dimensions

    def get_sensor_wavelength_mapping(self, wavelength):
        """Get height on sensor that given wavelength hits.

        Ref: https://www.notion.so/utat-ss/Sensor-Wavelength-Mapping-d700d47e877a43e097ab6095eb3da62d

        """
        assert self.grism is not None, "A grism component must be set."
        assert self.focuser is not None, "A focuser component must be set."

        incident_angle = self.grism.get_diffraction_angle(
            incident_angle=0, wavelength=wavelength, order=1
        )
        image_height = self.focuser.get_image_height(incident_angle=incident_angle)

        return image_height

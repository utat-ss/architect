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
        spatial_resolution=None,
        sensor: Component = None,
        foreoptic: Component = None,
        slit: Component = None,
        diffractor: Component = None,
        **components: Component,
    ):
        self.spatial_resolution = spatial_resolution
        super().__init__(
            sensor=sensor,
            foreoptic=foreoptic,
            slit=slit,
            diffractor=diffractor,
            **components,
        )

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

    def get_signal_to_noise(self, radiance: LUT, wavelength):
        """Get the signal to noise ratio of the system.

        Args:
            radiance: Atmospheric radiance incident on the system by wavelength.
            wavelength: Wavelength(s) at which to evaluate SNR.

        """

        signal = (
            (const.pi / 4)
            * (wavelength / (const.h * const.c))
            * (self.sensor.get_pixel_area() / self.foreoptic.f_number**2)
            * self.sensor.efficiency(wavelength)
            * self.get_transmittance()
            * self.slit.get_aperture_area()
            * radiance(wavelength)
            * self.sensor.dt
        )

        noise = self.sensor.get_noise(signal)

        snr = signal / noise

        return snr

    def get_FOV(self) -> np.ndarray[float, float]:
        """Get the field of view vector.

        A vector that defines the angular extent that can be imaged by the payload in
        the along-track and the across-track directions.

        """

        fov = 2 * np.arctan(self.slit.size / (2 * self.foreoptic.focal_length))

        return fov

    def get_iFOV(self) -> np.ndarray[float, float]:
        """Get the instantaneous field of view."""
        assert self.sensor is not None, "A sensor component must be specified."
        assert self.foreoptic is not None, "A foreoptic component must be specified."

        iFOV = 2 * np.arctan(self.sensor.pitch / (2 * self.foreoptic.focal_length))

        return iFOV

    def get_sensor_spatial_resolution(self, target_distance, skew_angle=0):
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

    def get_optical_spatial_resolution(self, wavelength, target_distance, skew_angle=0):
        """Get the optically-limited spatial resolution."""
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
            target_distance=target_distance, skew_angle=skew_angle
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

    def get_incident_angle(self, wavelength):
        """Get incident angle of grism light hitting lens."""

        emergent_angle = components.diffractors.VPHGrism.get_emergent_angle(
            angle_in=0, wavelength=wavelength, index_in=1, index_out=1, order=1
        )
        incident_angle = (
            components.diffractors.VPHGrism.apex_angle - emergent_angle - 90
        )

        return incident_angle

    def get_image_height(self, wavelength):
        """Get height on sensor that given wavelength hits."""

        incident_angle = self.get_incident_angle(wavelength=wavelength)
        image_height = 19 + components.lenses.Lens.get_image_height(
            incident_angle=incident_angle
        )

        return image_height


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

    def get_incident_angle(self, wavelength):
        """Get incident angle of grism light hitting lens."""
        # emergent_angle = components.diffractors.VPHGrism.get_emergent_angle(
        #     angle_in=0, wavelength=wavelength, index_in=1, index_out=1, order=1
        # )

        emergent_angle = self.grism.get_emergent_angle(angle_in=0, wavelength=wavelength, index_in=1, index_out=1, order=1)

        incident_angle = (
            self.grism.apex_angle - emergent_angle - 90
        )

        return incident_angle

    def get_mapped_height_sensor(self, wavelength):
        """Get height on sensor that given wavelength hits."""

        incident_angle = self.get_incident_angle(wavelength=wavelength)
        image_height = 19 + self.focuser.get_image_height(
            incident_angle=incident_angle
        )

        return image_height
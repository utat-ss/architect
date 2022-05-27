# external
import astropy.constants as const
import astropy.units as unit
import numpy as np
import pandas as pd

# project
from payload_designer.components import Component
from payload_designer import components
from payload_designer.components.lenses import Lens
from payload_designer.luts import LUT

class Payload:
    def __init__(self, **components: Component):

        for name, component in components.items():
            setattr(self, name, component)

        self.components = list(components.values())

    def get_property_table(self):
        """Get a table of system parameters."""  # TODO: make it print list of parameters + components

        properties = {}

        for key, value in self.__dict__.items():

            if type(value) == unit.Quantity:
                properties[key] = [value.value, value.unit]

            elif type(value) == LUT:
                properties[key] = [f"LUT ({value.name})", [value.x.unit, value.y.unit]]

            else:
                properties[key] = [value, None]

        df = pd.DataFrame.from_dict(
            data=properties, orient="index", columns=["Value", "Units"]
        )

        return df

    def __str__(self):
        df = self.get_property_table()

        return f"{type(self).__name__} Payload\n{df.to_string()}"

    def _repr_html_(self):
        df = self.get_property_table()

        return f"{type(self).__name__} Payload\n{df.to_html()}"

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
        sensor: Component,
        foreoptic: Component,
        slit: Component,
        **components: Component,
    ):
        super().__init__(sensor=sensor, foreoptic=foreoptic, slit=slit, **components)

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
            sensor=components.sensors.TauSWIR()
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


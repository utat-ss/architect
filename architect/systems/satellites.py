# external
import astropy.constants as const
import astropy.units as unit
import numpy as np
import pandas as pd
from astropy.units import Quantity

# project
from architect.systems import System
from architect.systems.payloads import FINCHEye, Payload


class Satellite(System):
    def __init__(self, altitude: Quantity[unit.m] = None):
        self.altitude = altitude

    def get_attrs_table(self):
        """Get a table of satellite parameters."""

        orbit_radius = self.get_orbit_radius()
        orbit_velocity = self.get_orbit_velocity()
        orbit_angular_velocity = self.get_orbit_angular_velocity()
        orbit_ground_projected_velocity = self.get_orbit_ground_projected_velocity()

        attributes = {
            "Altitude": [self.altitude.value, self.altitude.unit],
            "Orbit Radius": [orbit_radius.value, orbit_radius.unit],
            "Orbit Velocity": [orbit_velocity.value, orbit_velocity.unit],
            "Orbit Angular Velocity": [
                orbit_angular_velocity.value,
                orbit_angular_velocity.unit,
            ],
            "Orbit Ground Projected Velocity": [
                orbit_ground_projected_velocity.value,
                orbit_ground_projected_velocity.unit,
            ],
        }

        df = pd.DataFrame.from_dict(
            data=attributes, orient="index", columns=["Value", "Units"]
        )

        return df

    def get_orbit_radius(self):
        """Get the orbital radius.

        Ref: https://www.notion.so/utat-ss/Orbital-Radius-b07adc4a1a7543b2bceebf4fbeb61098

        """
        assert self.altitude is not None, "Altitude must be specified."

        R_orbit = const.R_earth + self.altitude

        return R_orbit

    def get_orbit_velocity(self):
        """Get the orbital velocity.

        Ref: https://www.notion.so/utat-ss/Orbital-Velocity-1cf0834326664872a1682db4bcd3a610

        """
        v_orbit = np.sqrt(const.G * const.M_earth / self.get_orbit_radius())

        return v_orbit

    def get_orbit_angular_velocity(self):
        """Get the orbital angular velocity.

        Ref: https://www.notion.so/utat-ss/Orbital-Angular-Velocity-40aba4f9348b4c01a0ae0ecd1ac17d8f

        """
        w_orbit = self.get_orbit_velocity() / self.get_orbit_radius() * unit.rad

        return w_orbit.to(unit.deg / unit.s)

    def get_orbit_ground_projected_velocity(self):
        """Get the orbital ground projected velocity.

        Ref: https://www.notion.so/utat-ss/Ground-Projected-Orbital-Velocity-4248ebec57634a42beebf619b0db1793

        """
        v_ground = self.get_orbit_angular_velocity() * const.R_earth

        return v_ground


class CubeSat(Satellite):
    def __init__(self, payload: Payload, altitude, U):
        super().__init__(altitude=altitude)
        self.U = U
        self.payload = payload

    def get_dimensions(self):
        return (10 * unit.cm, 10 * unit.cm, self.U * (10 * unit.cm))

    def get_volume(self):
        dims = self.get_dimensions()

        volume = dims[0] * dims[1] * dims[2]

        return volume


class FINCH(CubeSat):
    def __init__(self, payload: FINCHEye, altitude):
        super().__init__(payload=payload, altitude=altitude, U=3)

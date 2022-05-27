# external
import astropy.constants as const
import astropy.units as unit
import numpy as np

# project
from payload_designer.systems.payloads import FINCHEye, Payload


class Satellite:
    def __init__(self, altitude):
        self.altitude = altitude

    def get_orbit_radius(self):
        """Get the orbital radius."""

        R_orbit = const.R_earth + self.altitude

        return R_orbit

    def get_orbit_velocity(self):
        """Get the orbital velocity."""
        v_orbit = np.sqrt(const.G * const.M_earth / self.get_orbit_radius())

        return v_orbit

    def get_orbit_angular_velocity(self):
        """Get the orbital angular velocity."""
        w_orbit = self.get_orbit_velocity() / self.get_orbit_radius()

        return w_orbit

    def get_orbit_ground_projected_velocity(self):
        """Get the orbital ground projected velocity.

        This is effectively the velocity of the satellite's shadow on the ground if the
        sun were directly above it.

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

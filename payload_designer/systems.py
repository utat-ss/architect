# external
import astropy.constants as const
import numpy as np
import pandas as pd


class BaseSystemV3:
    def __init__(self, params, components):
        self.params = params
        self.components = components

    def report(self):

        # compute metrics
        R_orbit = self.get_orbit_radius()
        v_orbit = self.get_orbit_velocity()
        w_orbit = self.get_orbit_angular_velocity()
        v_ground = self.get_orbit_ground_projected_velocity()

        data = {}
        data["v_orbit"] = [round(v_orbit.value, 2), v_orbit.unit]
        data["w_orbit"] = [round(w_orbit.value, 2), w_orbit.unit]
        data["v_ground"] = [round(v_ground.value, 2), v_ground.unit]
        data["R_orbit"] = [round(R_orbit.value, 2), R_orbit.unit]

        df = pd.DataFrame.from_dict(
            data=data, orient="index", columns=["Value", "Units"]
        )

        return df

    def get_orbit_radius(self):

        R_orbit = const.R_earth + self.params["altitude"]

        return R_orbit

    def get_orbit_velocity(self):
        v_orbit = np.sqrt(const.G * const.M_earth / self.get_orbit_radius())

        return v_orbit

    def get_orbit_angular_velocity(self):
        w_orbit = self.get_orbit_velocity() / self.get_orbit_radius()

        return w_orbit

    def get_orbit_ground_projected_velocity(self):
        v_ground = self.get_orbit_angular_velocity() * const.R_earth

        return v_ground

    def get_mass(self):
        mass = 0
        [mass += component.mass for component in self.components]

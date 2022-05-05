"""Base component class."""

# external
import astropy.units as unit
import pandas as pd

# project
from payload_designer import luts


class Component:
    """A base class for components.

    Captures the shared properties of all components.

    Args:
        mass: Component mass.
        dimensions: Dimensions of component bounding box. Elements are ordered as (x, y, z) in the cubesat frame.

    """

    def __init__(self, dimensions: tuple = None, mass=None):
        self.dimensions = dimensions
        self.mass = mass

    def get_property_table(self):
        """Get a table of properties."""

        properties = {}

        for key, value in self.__dict__.items():

            if type(value) == unit.Quantity:
                properties[key] = [value.value, value.unit]

            elif type(value) == luts.LUT:
                properties[key] = [f"LUT ({value.name})", [value.x.unit, value.y.unit]]

            else:
                properties[key] = [value, None]

        df = pd.DataFrame.from_dict(
            data=properties, orient="index", columns=["Value", "Unit"]
        )

        return df

    def __str__(self):
        df = self.get_property_table()

        return f"{type(self).__name__} Component\n{df.to_string()}"

    def _repr_html_(self):
        df = self.get_property_table()

        return f"{type(self).__name__} Component\n{df.to_html()}"

    def get_volume(self):
        """Get the volume of the component from its bounding box."""

        volume = self.dimensions[0] * self.dimensions[1] * self.dimensions[2]

        return volume

"""System class."""

# external
import pandas as pd
from astropy.units import Quantity
from numpy import ndarray

# project
from architect.luts import LUT


class System:
    """A system is an artifact that may be physical or non-physical.

    It is defined by its external interfaces and internal properties.

    """

    def __init__(self, **systems):
        for name, system in systems.items():
            setattr(self, name, system)

        self.systems = list(systems.values())

    def __str__(self):
        """Get a string representation of the system attributes."""
        df = self.get_attrs_table()

        return f"{type(self).__name__} \n{df.to_string()}"

    def _repr_html_(self):
        """Get an HTML representation of the system attributes."""
        df = self.get_attrs_table()

        return f"{type(self).__name__} \n{df.to_html()}"

    def get_attrs_table(self):
        """Get a table of system attributes."""

        attributes = {}

        for key, value in self.__dict__.items():

            if isinstance(value, System):
                attributes[key] = [f"{type(value).__name__}", None]

            elif isinstance(value, ndarray):
                attributes[key] = [f"Array {value.shape}", None]

            elif isinstance(value, Quantity):
                if isinstance(value, ndarray):
                    attributes[key] = [f"Array {value.shape}", value.unit]
                else:
                    attributes[key] = [value.value, value.unit]

            elif isinstance(value, LUT):
                attributes[key] = [f"LUT ({value.name})", (value.x.unit, value.y.unit)]

            elif isinstance(value, list):
                attributes[key] = [f"{type(value).__name__} [{len(value)}]", None]

            else:
                attributes[key] = [value, None]

        df = pd.DataFrame.from_dict(
            data=attributes, orient="index", columns=["Value", "Units"]
        )

        return df

    def to_latex(self):
        """Generate a LaTeX table of system attributes."""
        df_latex = self.get_attrs_table().to_latex()
        return df_latex

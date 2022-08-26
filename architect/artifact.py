"""Artifact class."""

# external
import astropy.constants as const
import pandas as pd
from astropy.units import Quantity
from numpy import ndarray

# project
from architect.luts import LUT


class Artifact:
    """A generic class for design artifacts.

    Artifacts possess properties, and can be composed and inherited from to build
    architectures.

    """

    def get_attrs_table(self):
        """Get a table of artifact attributes."""

        attributes = {}

        for key, value in self.__dict__.items():

            if isinstance(value, Artifact):
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

    def __str__(self):
        df = self.get_attrs_table()

        return f"{type(self).__name__} \n{df.to_string()}"

    def _repr_html_(self):
        df = self.get_attrs_table()

        return f"{type(self).__name__} \n{df.to_html()}"

    def to_latex(self):
        df_latex = self.get_attrs_table().to_latex()
        return df_latex

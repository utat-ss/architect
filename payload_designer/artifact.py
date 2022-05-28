"""Artifact class"""

# external
import astropy.constants as const
from astropy.units import Quantity
from numpy import ndarray
import pandas as pd

# project
from payload_designer.luts import LUT

class Artifact():
    """A generic class for design artifacts. Artifacts possess properties, and can be composed and inherited from to build architectures."""
    def get_property_table(self):
        """Get a table of artifact properties."""

        properties = {}

        for key, value in self.__dict__.items():

            if isinstance(value, Artifact):
                properties[key] = [f"{type(value).__name__}",None]

            elif isinstance(value, ndarray):
                properties[key] = [f"Array {value.shape}", None]

            elif isinstance(value, Quantity):
                if isinstance(value, ndarray):
                    properties[key] = [f"Array {value.shape}", value.unit]
                else:
                    properties[key] = [value.value, value.unit]
                
            elif isinstance(value, LUT):
                properties[key] = [f"LUT ({value.name})", (value.x.unit, value.y.unit)]
            

            elif isinstance(value, list):
                properties[key] = [f"{type(value).__name__} [{len(value)}]", None]

            else:
                properties[key] = [value, None]

        df = pd.DataFrame.from_dict(
            data=properties, orient="index", columns=["Value", "Units"]
        )

        return df

    def __str__(self):
        df = self.get_property_table()

        return f"{type(self).__name__} \n{df.to_string()}"

    def _repr_html_(self):
        df = self.get_property_table()

        return f"{type(self).__name__} \n{df.to_html()}"

    def to_latex(self):
        """Returns a latex representation of system properties table."""
        df = self.get_property_table()

        return df.to_latex() 
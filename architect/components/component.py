"""Base component class."""

# external
import astropy.units as unit
import pandas as pd

# project
from architect import Artifact


class Component(Artifact):
    """A base class for components.

    Captures the shared properties of all components.

    Args:
        mass: Component mass.
        dimensions: Dimensions of component bounding box. Elements are ordered as (x, y, z) in the cubesat frame.

    """

    def __init__(self, dimensions: tuple = None, mass=None):
        self.dimensions = dimensions
        self.mass = mass

    def get_volume(self):
        """Get the volume of the component from its bounding box."""
        assert self.dimensions is not None, "Dimensions must be specified."

        volume = self.dimensions[0] * self.dimensions[1] * self.dimensions[2]

        return volume

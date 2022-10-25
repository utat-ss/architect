"""System class."""
# project
from architect import Artifact
from architect.components import Component


class System(Artifact):
    """Base class for system artifacts, which are collections of components."""

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

"""System class tests."""
# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.components import Component
from architect.systems import System

LOG = logging.getLogger(__name__)


def test_init():
    """Test initialization."""
    system = System()
    LOG.info(system)


def test_get_mass():
    """Test get_mass."""
    system = System(
        component_a=Component(mass=1 * unit.kg),
        component_b=Component(mass=2 * unit.kg),
        component_c=Component(mass=3 * unit.kg),
    )

    result = system.get_mass()
    LOG.info(result)

    assert result == 6 * unit.kg

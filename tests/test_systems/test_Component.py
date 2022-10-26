"""Tests for the Component class."""

# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.systems import Component

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""
    component = Component()

    LOG.info(component)


def test_get_volume():
    """Test get_volume method."""

    component = Component(dimensions=(1 * unit.m, 2 * unit.m, 3 * unit.m))

    result = component.get_volume()
    LOG.info(result)

    assert result == 6 * unit.m**3


def test_get_mass():
    """Test get_mass."""
    component = Component(
        component_a=Component(mass=1 * unit.kg),
        component_b=Component(mass=2 * unit.kg),
        component_c=Component(mass=3 * unit.kg),
    )

    result = component.get_mass()
    LOG.info(result)

    assert result == 6 * unit.kg

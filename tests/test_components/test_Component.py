"""Tests for the Component class."""

# stdlib
import logging

# project
from architect.components import Component
import astropy.units as unit

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
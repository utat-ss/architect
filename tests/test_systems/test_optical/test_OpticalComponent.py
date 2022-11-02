"""Tests for OpticalComponent."""

# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.systems.optical import OpticalComponent

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    component = OpticalComponent()
    LOG.info(component)


def test_get_transmittance():
    """Test get_transmittance method."""

    component = OpticalComponent()

    result = component.get_transmittance()
    LOG.info(result)

    assert result.unit == unit.percent

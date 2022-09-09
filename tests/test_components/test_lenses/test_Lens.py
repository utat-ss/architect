"""Tests for AchromLens component."""
# stdlib
import logging

# project
from architect.components.lenses import Lens
import astropy.units as unit

LOG = logging.getLogger(__name__)


def test_get_image_height():
    """Test get_image_height."""

    lens = Lens(focal_length=10*unit.mm)

    result = lens.get_image_height(incident_angle=5*unit.deg)
    LOG.info(result)

    assert result.decompose().unit == unit.m

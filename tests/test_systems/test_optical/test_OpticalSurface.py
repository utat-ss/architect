"""Tests for OpticalSurface."""

# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.systems.optical.optical_surface import OpticalSurface

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    component = OpticalSurface()
    LOG.info(component)


def test_angle_of_refraction():
    """Test angle_of_refraction method."""

    component = OpticalSurface(medium_index=1.5)

    incident_angle = 45 * unit.deg
    incident_index = 1.0
    angle_of_refraction = component.angle_of_refraction(
        incident_angle=incident_angle, incident_index=incident_index
    )

    LOG.info(angle_of_refraction)

    assert angle_of_refraction.unit == unit.deg

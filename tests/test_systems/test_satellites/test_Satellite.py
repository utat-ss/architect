"""Satellite class tests."""
from architect.systems.satellites import Satellite
import astropy.units as unit
import logging

LOG = logging.getLogger(__name__)



def test_get_orbit_radius():
    """Test get_orbit_radius method."""

    satellite = Satellite(altitude=500 * unit.km)

    radius = satellite.get_orbit_radius()

    LOG.info(f"Orbit radius: {radius}")

def test_get_orbit_velocity():
    """Test get_orbit_velocity method."""

    satellite = Satellite(altitude=500 * unit.km)

    radius = satellite.get_orbit_velocity()

    LOG.info(f"Orbit velocity: {radius}")

def test_get_orbit_angular_velocity():
    """Test get_orbit_angular_velocity method."""

    satellite = Satellite(altitude=500 * unit.km)

    radius = satellite.get_orbit_angular_velocity()

    LOG.info(f"Orbit angular velocity: {radius}")
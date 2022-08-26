"""Tests for SRTGrating component."""
# stdlib
import logging

# project
from architect.components.diffractors import TransmissiveDiffractor
import astropy.units as unit

LOG = logging.getLogger(__name__)


def test_get_diffraction_angle():
    """Test get_emergent_angle."""
    diffractor = TransmissiveDiffractor(fringe_frequency=600 * 1/unit.m)
    angle = diffractor.get_diffraction_angle(wavelength=900*unit.nm)

    LOG.info(f"diffraction angle: {angle}")
"""Tests for VPH Grating component."""
# stdlib
import logging

# external
import astropy.units as unit
import numpy as np
import pytest

# project
from architect import components, luts
from architect.components.diffractors import VPHGrating
from architect.libs.physlib import snell

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    grating = VPHGrating()
    LOG.info(grating)


def test_get_angle_out():
    """Test get_diffraction_angle."""

    grating = VPHGrating(
        index_dcg=20, fringe_frequency=600 * (1 / unit.mm), index_seal=1.0
    )
    result = grating.get_diffraction_angle(
        incident_angle=0 * unit.rad, wavelength=1300 * unit.nm
    )
    LOG.info(result)

    assert result.unit == unit.rad

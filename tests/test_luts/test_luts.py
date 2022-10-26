"""Tests for the LUT implementation."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np

# project
from architect import luts

LOG = logging.getLogger(__name__)


def test_LUT_call():
    """Test the LUT class call method."""

    lut = luts.load("test_lut")
    LOG.debug(lut)

    x = np.linspace(start=1500, stop=1700, num=16) * unit.nm
    LOG.debug(f"Input x:\n{x}")

    y = lut(x)
    LOG.debug(f"Output y:\n{y}")

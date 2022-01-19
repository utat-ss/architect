"""Tests for the utillib library."""

# stdlib
import logging
from pathlib import Path

# external
import numpy as np

# project
from payload_designer.libs import utillib

LOG = logging.getLogger(__name__)


def test_LUT_call():
    """Test the LUT class call method."""
    lut_data = Path("data/test_LUT.csv")

    lut = utillib.LUT(lut_data)
    LOG.debug(f"LUT x:\n{lut.x}")
    LOG.debug(f"LUT y:\n{lut.y}")

    x = np.linspace(start=1400, stop=1700, num=100)
    LOG.debug(f"Input x:\n{x}")

    y = lut(x)
    LOG.debug(f"Output y:\n{y}")

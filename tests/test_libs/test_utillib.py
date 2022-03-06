"""Tests for the utillib library."""

# stdlib
import logging
from pathlib import Path

# external
import numpy as np
import pytest

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


def test_orient_tensor():
    """Test the orient_tensor function."""
    ans = (1, 4, 1)
    a = [1, 2, 3, 4]

    a_orient = utillib.orient_tensor(a=a, dim=1, dims=3)

    LOG.debug(f"a_orient shape: {a_orient.shape}, {ans} (ans)")
    assert a_orient.shape == ans


@pytest.mark.star
def test_convert_dark_current_density_to_dark_current():
    """Test dark current density to dark current conversion function."""
    ans = 0  # TODO
    i_dark = 10
    p = 15

    i_dark_converted = utillib.convert_dark_current_density_to_dark_current(i_dark, p)
    LOG.info(f"i_dark_converted: {i_dark_converted}, {ans} (ans)")

    assert i_dark_converted == ans

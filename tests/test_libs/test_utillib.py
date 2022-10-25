"""Tests for the utillib library."""

# stdlib
import logging

# project
from architect.libs import utillib

LOG = logging.getLogger(__name__)


def test_orient_tensor():
    """Test the orient_tensor function."""
    ans = (1, 4, 1)
    a = [1, 2, 3, 4]

    a_orient = utillib.orient_tensor(a=a, dim=1, dims=3)

    LOG.debug(f"a_orient shape: {a_orient.shape}, {ans} (ans)")
    assert a_orient.shape == ans

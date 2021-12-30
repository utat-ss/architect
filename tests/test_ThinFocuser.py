"""Tests for Thin Focuser component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer import components

LOG = logging.getLogger(__name__)


def test_ThinFocuser_get_image_height():
    """Test ThinFocuser.get_image_height()."""

    # parameters
    f = 4
    a_in = 30

    # component instantiation
    focuser = components.ThinFocuser(f=f, a_in=a_in)

    # evaluation
    h = focuser.get_image_height()
    LOG.info(f"Image height: {h}")

    assert h == pytest.approx(4 * math.sqrt(3) / 3)


def test_ThinFocuser_get_image_height_vectorized():
    """Test ThinFocuser.get_image_height() in vectorized mode."""

    # parameters
    f = np.array([1, 2, 3])
    a_in = np.array([15, 30, 45])

    # component instantiation
    focuser = components.ThinFocuser(f=f, a_in=a_in)

    # evaluation
    h = focuser.get_image_height()
    LOG.info(f"Image height: {h}")

    # assert h == pytest.approx(4*math.sqrt(3)/3)

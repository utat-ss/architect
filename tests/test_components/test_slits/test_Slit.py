"""Tests for Slit component."""
# stdlib
import logging

# external
import numpy as np
import pytest

# project
from payload_designer.componentss import slits

LOG = logging.getLogger(__name__)


def test_get_horizontal_field_of_view():
    """Test ThinFocuser.get_horizontal_field_of_view()."""

    # parameters
    l_s = 1
    f = 70

    # component instantiation
    slit = slits.Slit(l_s=l_s, f=f)

    # evaluation
    fov = slit.get_horizontal_field_of_view()
    LOG.info(f"Horizontal field of view: {fov}")

    assert fov == pytest.approx(360 * np.arctan(1 / 140) / np.pi)


def test_get_vertical_field_of_view():
    """Test ThinFocuser.get_vertical_field_of_view()."""

    # parameters
    w_s = 0.01
    f = 70

    # component instantiation
    slit = slits.Slit(w_s=w_s, f=f)

    # evaluation
    fov = slit.get_vertical_field_of_view()
    LOG.info(f"Vertical field of view: {fov}")

    assert fov == pytest.approx(360 * np.arctan(1 / 14000) / np.pi)


def test_get_image_width():
    """Test ThinFocuser.get_image_width()."""
    # w_i = np.power(np.multiply(np.power(self.m, 2), np.power(self.w_s, 2)) + np.power(self.w_o, 2), 0.2)
    # parameters
    m = 1
    w_s = 0.01
    w_o = 0.05

    # component instantiation
    slit = slits.Slit(m=m, w_s=w_s, w_o=w_o)

    # evaluation
    w = slit.get_image_width()
    LOG.info(f"Image width: {w}")

    assert w == pytest.approx(np.sqrt(13 / 5000))


def test_get_slit_width():
    """Test ThinFocuser.get_slit_width()."""
    # w_s = np.divide(self.w_d, self.m)
    # parameters
    w_d = 5
    m = 1

    # component instantiation
    slit = slits.Slit(w_d=w_d, m=m)

    # evaluation
    w = slit.get_slit_width()
    LOG.info(f"Slit width: {w}")

    assert w == 5

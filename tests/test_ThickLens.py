"""Tests for Thick Lens component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer import components

LOG = logging.getLogger(__name__)

# @pytest.mark.star # will only run these tests # pytest -v -m star
def test_ThickLens_get_focal_length():
    """Test ThickLens.get_focal_length()."""

    # parameters (in cm)
    n = 1.5
    R1 = 20
    R2 = -40
    d = 1

    # component instantiation
    thicklens = components.ThickLens(n=n, R1=R1, R2=R2, d=d)

    # evaluation
    h = thicklens.get_focal_length()
    LOG.info(f"Effective focal length: {h}")

    assert h == pytest.approx(4800/179)

# @pytest.mark.plot # will not run these tests # pytest -v -m "not plot"
def test_ThickLens_get_principal_planes():
    """Test ThickLens.get_principal_planes()."""

    # parameters
    n = 1.5
    R1 = 20
    R2 = -40
    d = 1
    f_thick = 4800/179

    # component instantiation
    thicklens = components.ThickLens(n=n, R1=R1, R2=R2, d=d, f_thick=f_thick)

    # evaluation
    h = thicklens.get_principal_planes()
    LOG.info(f"Principal planes: {h}")

    (h1, h2) = h

    assert h1 == pytest.approx(40/179) and h2 == pytest.approx(-80/179)

def test_ThickLens_get_focuser_image_distance():
    """Test ThickLens.get_focuser_image_distance()."""

    # parameters
    f_thick = 4800/179

    # component instantiation
    thicklens = components.ThickLens(f_thick=f_thick)

    # evaluation
    h = thicklens.get_focuser_image_distance()
    LOG.info(f"Focuser image distance: {h}")

    assert h == pytest.approx(4800/179)

def test_ThickLens_get_collimator_object_distance():
    """Test ThickLens.get_collimator_object_distance()."""

    # parameters
    f_thick = 4800/179

    # component instantiation
    thicklens = components.ThickLens(f_thick=f_thick)

    # evaluation
    h = thicklens.get_collimator_object_distance()
    LOG.info(f"Collimator object distance: {h}")

    assert h == pytest.approx(4800/179)

def test_ThickLens_get_focuser_emergent_ray_height():
    """Test ThickLens.get_focuser_emergent_ray_height()."""

    # parameters
    d = 1
    n = 1.5
    R1 = 20
    R2 = -40
    f_thick = 25
    a1 = 30

    # component instantiation
    thicklens = components.ThickLens(d=d, n=n, R1=R1, R2=R2, f_thick=f_thick, a1=a1)

    # evaluation
    h = thicklens.get_focuser_emergent_ray_height()
    LOG.info(f"Focuser emergent ray height: {h}")

    assert h == pytest.approx((2351*np.pi)/96)

def test_ThickLens_get_collimator_emergent_ray_angle():
    """Test ThickLens.get_collimator_emergent_ray_angle()."""

    # parameters
    x1 = 25
    f_thick = 4800/179

    # component instantiation
    thicklens = components.ThickLens(x1=x1, f_thick=f_thick)

    # evaluation
    h = thicklens.get_collimator_emergent_ray_angle()
    LOG.info(f"Collimator emergent ray angle: {h}")

    assert h == pytest.approx(-179/192)
"""Tests for Thick Lens component."""
# stdlib
import logging

# external
import numpy as np
import pytest

# project
from payload_designer.componentss import lenses

LOG = logging.getLogger(__name__)


def test_get_focal_length():
    """Test ThickLens.get_focal_length()."""

    # parameters (in cm)
    n = 1.5
    R1 = 20
    R2 = -40
    d = 1

    # component instantiation
    thicklens = lenses.ThickLens(n=n, R1=R1, R2=R2, d=d)

    # evaluation
    h = thicklens.get_focal_length()
    LOG.info(f"Effective focal length: {h}")

    assert h == pytest.approx(4800 / 179)


def test_get_principal_planes():
    """Test ThickLens.get_principal_planes()."""

    # parameters
    n = 1.5
    R1 = 20
    R2 = -40
    d = 1
    f_thick = 4800 / 179

    # component instantiation
    thicklens = lenses.ThickLens(n=n, R1=R1, R2=R2, d=d, f_thick=f_thick)

    # evaluation
    h = thicklens.get_principal_planes()
    LOG.info(f"Principal planes: {h}")

    (h1, h2) = h

    assert h1 == pytest.approx(40 / 179) and h2 == pytest.approx(-80 / 179)


def test_get_focuser_image_distance():
    """Test ThickLens.get_focuser_image_distance()."""

    # parameters
    f_thick = 4800 / 179

    # component instantiation
    thicklens = lenses.ThickLens(f_thick=f_thick)

    # evaluation
    h = thicklens.get_focuser_image_distance()
    LOG.info(f"Focuser image distance: {h}")

    assert h == pytest.approx(4800 / 179)


def test_get_collimator_object_distance():
    """Test ThickLens.get_collimator_object_distance()."""

    # parameters
    f_thick = 4800 / 179

    # component instantiation
    thicklens = lenses.ThickLens(f_thick=f_thick)

    # evaluation
    h = thicklens.get_collimator_object_distance()
    LOG.info(f"Collimator object distance: {h}")

    assert h == pytest.approx(4800 / 179)


def test_get_focuser_image_height():
    """Test ThickLens.get_focuser_image_height()."""

    # parameters
    f_thick = 4800 / 179
    a1 = 30

    # component instantiation
    thicklens = lenses.ThickLens(f_thick=f_thick, a1=a1)

    # evaluation
    h = thicklens.get_focuser_image_height()
    LOG.info(f"Focuser image height: {h}")

    assert h == pytest.approx(np.pi * (800 / 179))


def test_get_collimator_emergent_ray_angle():
    """Test ThickLens.get_collimator_emergent_ray_angle()."""

    # parameters
    x1 = 25
    f_thick = 4800 / 179

    # component instantiation
    thicklens = lenses.ThickLens(x1=x1, f_thick=f_thick)

    # evaluation
    h = thicklens.get_collimator_emergent_ray_angle()
    LOG.info(f"Collimator emergent ray angle: {h}")

    assert h == pytest.approx(np.degrees(-179 / 192))

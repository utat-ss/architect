"""Tests for surface relief component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer import components

LOG = logging.getLogger(__name__)



def test_SRGrating_get_angle_out():
    """Test SRGrating.get_angle_out()."""

    # parameters
    alpha = 10
    G = 300
    lmda = 1600
    m = 1

    # component instantiation
    SR = components.SRGrating(alpha=alpha, G=G, lmda=lmda, m=m)

    # evaluation
    beta = SR.get_angle_out()
    LOG.info(f"Diffracted angle: {beta}")

    assert beta == pytest.approx(np.arcsin(12/25))

def test_SRGrating_get_angular_dispersion():
    """Test SRGrating.get_angular_dispersion()."""

    # parameters
    alpha = 10
    lmda = 1600

    # component instantiation
    SR = components.SRGrating(alpha=alpha, lmda=lmda)

    # evaluation
    ang_disp = SR.get_angle_out()
    LOG.info(f"Angular dispersion: {ang_disp}")

    assert ang_disp == pytest.approx(4537)

def test_SRGrating_get_resolving_power():
    """Test SRGrating.get_resolving_power()."""

    # parameters
    alpha = 10
    beta = np.arcsin(12/25)
    lmda = 1600
    W = 300


    # component instantiation
    SR = components.SRGrating(alpha=alpha, beta=beta, lmda=lmda, W=W)

    # evaluation
    R = SR.get_angle_out()
    LOG.info(f"Resolving power: {R}")

    assert R == pytest.approx(0.12)
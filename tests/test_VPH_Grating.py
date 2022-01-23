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
    a_0 = 10
    n_0 = 1.52
    Lmda = 2.1
    lmda = 1600
    m = 1
    phi = 2

    # component instantiation
    VPHGrating = components.VPHGrating(a_0=a_0, n_0=n_0, Lmda=Lmda, lmda=lmda, m=m, phi=phi)

    # evaluation
    beta = VPHGrating.get_angle_out()
    LOG.info(f"Diffracted angle: {beta}")

    assert beta == pytest.approx(-9.95)

def test_SRGrating_get_Kogelnik_efficiency():
    """Test SRGrating.get_Kogelnik_efficiency()."""

    # parameters
    delta_n2 = 2
    n_2 = 1.5
    d = 10
    lmda = 1600
    Lmda = 2.1
    m = 1

    # component instantiation
    VPHGrating = components.get_Kogelnik_efficiency(delta_n2=delta_n2, n_2=n_2, d=d, lmda=lmda, Lmda=Lmda, m=m)

    # evaluation
    mu = VPHGrating.get_Kogelnik_efficiency()
    LOG.info(f"Diffracted angle: {mu}")

    assert mu == pytest.approx(0.29)

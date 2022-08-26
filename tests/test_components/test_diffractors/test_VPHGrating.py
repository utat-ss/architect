"""Tests for VPH Grating component."""
# stdlib
import logging

# external
import pytest

# project
from architect.components import diffractors

LOG = logging.getLogger(__name__)


def test_get_angle_out():
    """Test VPHGrating.get_angle_out()."""

    # parameters
    a_0 = 10
    n_0 = 1.52
    Lmda = 1000
    lmda = 1600
    m = 1
    phi = 2

    # component instantiation
    VPHGrating = diffractors.VPHGrating(
        a_0=a_0, n_0=n_0, Lmda=Lmda, lmda=lmda, m=m, phi=phi
    )

    # evaluation
    beta = VPHGrating.get_angle_out()
    LOG.info(f"Diffracted angle: {beta}")

    assert beta == pytest.approx(-0.17453337)


def test_get_Kogelnik_efficiency():
    """Test VPHGrating.get_Kogelnik_efficiency()."""

    # parameters
    delta_n2 = 2
    n_2 = 1.5
    d = 10
    lmda = 1600
    Lmda = 1000
    m = 1

    # component instantiation
    VPHGrating = diffractors.VPHGrating(
        delta_n2=delta_n2, n_2=n_2, d=d, lmda=lmda, Lmda=Lmda, m=m
    )

    # evaluation
    mu = VPHGrating.get_Kogelnik_efficiency()
    LOG.info(f"Diffracted angle: {mu}")

    assert mu == pytest.approx(6.55359374e-18)


def test_get_efficiency_bandwidth():
    """Test VPHGrating.get_efficiency_bandwidth()."""

    # parameters
    n_2 = 1.5
    d = 10
    lmda = 1600
    Lmda = 1000
    m = 1

    # component instantiation
    VPHGrating = diffractors.VPHGrating(n_2=n_2, d=d, lmda=lmda, Lmda=Lmda, m=m)

    # evaluation
    lmda_eff = VPHGrating.get_efficiency_bandwidth()
    LOG.info(f"Efficiency bandwidth: {lmda_eff}")

    assert lmda_eff == pytest.approx(768)

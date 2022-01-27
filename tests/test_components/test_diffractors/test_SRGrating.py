"""Tests for SRGrating component."""
# stdlib
import logging

# external
import pytest

# project
from payload_designer.components import diffractors

LOG = logging.getLogger(__name__)


def test_get_angle_out():
    """Test SRGrating.get_angle_out()."""

    # parameters
    alpha = 10
    G = 300
    lmda = 1600
    m = 1

    # component instantiation
    SR = diffractors.SRGrating(alpha=alpha, G=G, lmda=lmda, m=m)

    # evaluation
    beta = SR.get_angle_out()
    LOG.info(f"Diffracted angle: {beta}")

    assert beta == pytest.approx(0.3113582086)


def test_get_angular_dispersion():
    """Test SRGrating.get_angular_dispersion()."""

    # parameters
    alpha = 10
    lmda = 1600
    G = 300
    m = 1

    # component instantiation
    SR = diffractors.SRGrating(alpha=alpha, G=G, lmda=lmda, m=m)
    beta = SR.get_angle_out()
    SR = diffractors.SRGrating(alpha=alpha, beta=beta, lmda=lmda)

    # evaluation
    ang_disp = SR.get_angular_dispersion()
    LOG.info(f"Angular dispersion: {ang_disp}")

    assert ang_disp == pytest.approx(315153.0773)


def test_get_resolving_power():
    """Test SRGrating.get_resolving_power()."""

    # parameters
    alpha = 10
    G = 300
    lmda = 1600
    m = 1
    W = 300

    # component instantiation
    SR = diffractors.SRGrating(alpha=alpha, G=G, lmda=lmda, m=m)
    beta = SR.get_angle_out()
    SR = diffractors.SRGrating(alpha=alpha, beta=beta, lmda=lmda, W=W)

    # evaluation
    R = SR.get_resolving_power()
    LOG.info(f"Resolving power: {R}")

    assert R == pytest.approx(0.03357794565)


def test_get_anamorphic_amplification():
    """Test SRGrating.get_anamorphic_amplification()."""

    # parameters
    alpha = 10
    G = 300
    lmda = 1600
    m = 1

    # component instantiation
    SR = diffractors.SRGrating(alpha=alpha, G=G, lmda=lmda, m=m)
    beta = SR.get_angle_out()
    SR = diffractors.SRGrating(alpha=alpha, beta=beta)

    # evaluation
    ratio = SR.get_anamorphic_amplification()
    LOG.info(f"Anamorphic dispersion: {ratio}")

    assert ratio == pytest.approx(0.9666032334)

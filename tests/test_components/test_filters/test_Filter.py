# stdlib
import logging

# external
import numpy as np
import pytest

# project
from payload_designer.components import filters

LOG = logging.getLogger(__name__)


def test_phase_shift():
    """Test Filter.phase_shift()."""
    # parameters
    n_0 = 1
    n_star = 1.8
    theta = 20
    lambda_0 = 1500
    # component instantiation
    bandpass = filter.Filter(n_0=n_0, n_star=n_star, theta=theta, lambda_0=lambda_0)
    # evaluation
    h = bandpass.phase_shift()
    LOG.info(f"Phase Shift: {h}")

    assert h == pytest.approx(1500 * (1 - ((1 / 1.8) * np.sin(20)) ** 2) ** 0.5)


def test_reflected_beam():
    """Test Filter.reflected_beam()."""
    # parameters
    n_star = 1.7
    n_0 = 1

    # component instantiation
    bandpass = filter.Filter(n_0=n_0, n_star=n_star)

    # evaluation
    i = bandpass.reflected_beam()
    LOG.info(f"Reflected Beam: {i}")

    assert i == pytest.approx(((0.7) / (2.7)) ** 2)


def test_transmitted_beam_system():
    """Test Filter.transmitted_beam_system()."""
    # parameters
    R_1 = 0.37
    R_2 = 0.41
    T_1 = 0.63
    T_2 = 0.59
    n = 1.5
    d = 200000000
    lambda_0 = 1500
    theta = 20
    phi_1 = 1300
    phi_2 = 1200

    # component instantiation
    bandpass = filter.Filter(
        R_1=R_1,
        R_2=R_2,
        T_1=T_1,
        T_2=T_2,
        n=n,
        d=d,
        lambda_0=lambda_0,
        theta=theta,
        phi_1=phi_1,
        phi_2=phi_2,
    )

    # evaluation
    j = bandpass.transmitted_beam_system()
    LOG.info(f"Transmitted Beam: {j}")

    assert j == pytest.approx(
        ((0.63 * 0.59) / (1 - (0.37 * 0.41) ** 0.5) ** 2)
        * (
            1
            / (
                1
                + ((4 * (0.37 * 0.41) ** 0.5) / (1 - (0.37 * 0.41) ** 0.5) ** 2)
                * (np.sin(0.5 * 1300 * 1200 - 20)) ** 2
            )
        )
    )

"""Tests for Foreoptic component."""
# stdlib
import logging

# external
import numpy as np
import pytest

# project
from architect.components import foreoptics

LOG = logging.getLogger(__name__)


def test_get_aperture_diameter():
    """Test Foreoptic.get_aperture_diameter()."""

    # parameters
    ds_i = 10
    n = 5

    # component instantiation
    foreoptic = foreoptics.Foreoptic(ds_i=ds_i, n=n)

    # evaluation
    d = foreoptic.get_aperture_diameter()
    LOG.info(f"Aperture diameter: {d}")

    assert d == 2


def test_get_magnification():
    """Test Foreoptic.get_magnification()."""

    # parameters
    ds_i = 10
    ds_o = 20

    # component instantiation
    foreoptic = foreoptics.Foreoptic(ds_i=ds_i, ds_o=ds_o)

    # evaluation
    m = foreoptic.get_magnification()
    LOG.info(f"Magnification: {m}")

    assert m == 1 / 2


def test_get_f_number():
    """Test Foreoptic.get_f_number()."""

    # parameters
    ds_i = 10
    dm_a = 2

    # component instantiation
    foreoptic = foreoptics.Foreoptic(ds_i=ds_i, dm_a=dm_a)

    # evaluation
    n = foreoptic.get_f_number()
    LOG.info(f"F/number: {n}")

    assert n == 5


def test_get_effective_focal_length():
    """Test Foreoptic.get_effective_focal_length()."""

    # parameters
    ds_o = 40
    ds_i = 10

    # component instantiation
    foreoptic = foreoptics.Foreoptic(ds_o=ds_o, ds_i=ds_i)

    # evaluation
    efl = foreoptic.get_effective_focal_length()
    LOG.info(f"F/number: {efl}")

    assert efl == pytest.approx(1 / 8)


def test_get_numerical_aperture():
    """Test Foreoptic.get_numerical_aperture()."""

    # parameters
    a_in_max = 30

    # component instantiation
    foreoptic = foreoptics.Foreoptic(a_in_max=a_in_max)

    # evaluation
    na = foreoptic.get_numerical_aperture()
    LOG.info(f"Numerical aperture: {na}")

    assert na == pytest.approx(1 / 2)


def test_get_geometric_etendue():
    """Test Foreoptic.get_geometric_etendue()."""

    # parameters
    s = 100
    a_in_max = 30

    # component instantiation
    foreoptic = foreoptics.Foreoptic(s=s, a_in_max=a_in_max)

    # evaluation
    g = foreoptic.get_geometric_etendue()
    LOG.info(f"Geometric etendue: {g}")

    assert g == pytest.approx(np.pi * 25)


def test_get_radiant_flux():
    """Test Foreoptic.get_radian_flux()."""

    # parameters
    b = 100
    g = 75

    # component instantiation
    foreoptic = foreoptics.Foreoptic(b=b, g=g)

    # evaluation
    f = foreoptic.get_radiant_flux()
    LOG.info(f"Radiant flux: {f}")

    assert f == 7500

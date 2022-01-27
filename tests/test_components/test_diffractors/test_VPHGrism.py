"""Tests for VPH Grism component."""
# stdlib
import logging

# external
import numpy as np
import pytest

# project
from payload_designer.componentss import diffractors

LOG = logging.getLogger(__name__)


def test_get_angle_out():
    """Test VPHGrism.get_angle_out()."""

    # region parameter definiton
    l = np.linspace(start=1600, stop=1700, num=100)
    v = np.linspace(start=300, stop=6000, num=100)
    # region

    grism = diffractors.VPHGrism(
        a_in=0, n_1=1.0, n_2=1.52, n_3=1.3, m=1, a=45, v=v, l=l
    )

    angle_out = grism.get_angle_out()

    LOG.info(f"Angle out: {angle_out}°")

    # fig = px.scatter(x=v, y=angle_out)
    # fig.show()

    # fig = px.scatter(x=l, y=angle_out)
    # fig.show()


def test_get_undeviated_wavelength():
    """Test VPHGrism.get_undeviated_wavelength()."""
    # parameter definition - fill in with real values later
    m = 1
    v = 1000
    a = 90
    a_in = 0
    n_1 = 1.0
    n_2 = 1.52
    n_3 = 1.3
    grism = diffractors.VPHGrism(m=m, v=v, a=a, a_in=a_in, n_1=n_1, n_2=n_2, n_3=n_3)
    undeviated_wavelength = grism.get_undeviated_wavelength()
    LOG.info(f"Undeviated Wavelength: {undeviated_wavelength}°")
    assert undeviated_wavelength == pytest.approx(1761.118)


def test_get_resolvance():
    """Test VPHGrism.get_resolvance()."""
    # parameter definition
    l = 1600  # np.linspace(start=1600, stop=1700, num=100)  # nm
    dl = 2  # nm
    # N =
    # m = 1
    # v = 600  # lines/mm
    # w = 2  # in mm ->

    grism = diffractors.VPHGrism(l=l, dl=dl)
    # grism = diffractors.VPHGrism(m=1, v=v, w=w)
    # grism = diffractors.VPHGrism(m=m, N=N)
    resolvance = grism.get_resolvance()
    LOG.info(f"Resolvance: {resolvance}°")
    assert resolvance == pytest.approx(800)


def test_get_resolution():
    """Test VPHGrism.get_resolution()."""
    # parameter definition
    l = 1600  # np.linspace(start=1600, stop=1700, num=100)
    v = 1000  # lines/mm
    w = 2  # in mm
    # R =
    # N =
    # m = 1

    grism = diffractors.VPHGrism(m=1, v=v, w=w, l=l)
    # grism = diffractors.VPHGrism(l=l, R=R)
    # grism = diffractors.VPHGrism(m=1, N=N, l=l)

    resolution = grism.get_resolution()
    LOG.info(f"Resolution: {resolution}°")
    assert resolution == pytest.approx(0.8)


def test_get_diffraction_efficiency():
    """Test VPHGrism.get_diffraction_efficiency()."""
    # parameter definition
    a_in = 0
    a = 90
    d = 2
    l = 1600  # np.linspace(start=1600, stop=1700, num=100)
    v = 1000
    n_g = 0.1
    n_3 = 1.3
    n_2 = 1.52
    n_1 = 1.0
    eff_mat = 0.9

    grism = diffractors.VPHGrism(
        a_in=a_in,
        a=a,
        l=l,
        d=d,
        v=v,
        n_g=n_g,
        n_1=n_1,
        n_2=n_2,
        n_3=n_3,
        eff_mat=eff_mat,
    )

    diffraction_efficiency = grism.get_diffraction_efficiency()
    LOG.info(f"Diffraction Efficiency: {diffraction_efficiency}°")
    assert diffraction_efficiency == pytest.approx(0.5185951)

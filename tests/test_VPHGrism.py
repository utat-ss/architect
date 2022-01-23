"""VPH Grism component tests."""
# stdlib
import logging

# external
import numpy as np

# project
from payload_designer import components
from payload_designer.libs import plotlib

LOG = logging.getLogger(__name__)


def test_VPHGrism_get_angle_out():
    """Test VPHGrism.get_angle_out()."""

    # region parameter definiton
    l = np.linspace(start=1600, stop=1700, num=100)
    v = np.linspace(start=300, stop=6000, num=100)
    # region

    grism = components.VPHGrism(a_in=0, n_1=1.0, n_2=1.52, n_3=1.3, m=1, a=45, v=v, l=l)

    angle_out = grism.get_angle_out()

    LOG.info(f"Angle out: {angle_out}°")

    # fig = px.scatter(x=v, y=angle_out)
    # fig.show()

    # fig = px.scatter(x=l, y=angle_out)
    # fig.show()

    fig = plotlib.surface(x=l, y=v, z=angle_out)
    fig.show()


def test_get_undeviated_wavelength():
    """tests get_undeviated_wavelength"""
    # parameter definition
    m = 1
    v = 300
    a = 45
    a_in = 0
    grism = components.VPHGrism(m=m, v=v, a=a, a_in=a_in)
    undeviated_wavelength = grism.get_undeviated_wavelength()
    # LOG.info(f"Undeviated Wavelength: {undeviated_wavelength}°")


def test_VPHGrism_get_resolvance():
    """tests get_resolvance"""
    # parameter definition
    l = np.linspace(start=1600, stop=1700, num=100)  # nm -> converted to m in func
    dl = 2  # nm -> converted to m in func
    # N =
    # m = 1
    # n = 600 * 10 ** 3  # lines/m
    # w = 770  # in microns -> converted to m in func

    grism = components.VPHGrism(l=l, dl=dl)
    # grism = components.VPHGrism(m=1, n=n, w=w)
    # grism = components.VPHGrism(m=m, N=N)
    resolvance = grism.get_resolvance()
    # LOG.info(f"Resolvance: {resolvance}°")


def test_VPHGrism_get_resolution():
    """tests get_resolution"""
    # parameter definition
    l = np.linspace(start=1600, stop=1700, num=100)
    n = 600 * 10 ** 3  # lines/m
    w = 770  # in microns -> converted to m in func
    # R =
    # N =
    # m = 1

    grism = components.VPHGrism(m=1, n=n, w=w, l=l)
    # grism = components.VPHGrism(l=l, R=R)
    # grism = components.VPHGrism(m=1, N=N, l=l)

    resolution = grism.get_resolution()
    # LOG.info(f"Resolution: {resolution}°")


def test_VPHGrism_get_diffraction_efficiency():
    """tests get_diffraction efficiency"""
    # parameter definition
    a_in = 0
    a = 45
    d = 2
    l = np.linspace(start=1600, stop=1700, num=100)
    v = 300
    n_g = 0.1
    n_3 = 1.0
    n_2 = 1.0
    n_1 = 1.0
    eff_mat = 0.9

    grism = components.VPHGrism(
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
    # LOG.info(f"Diffraction Efficiency: {diffraction_efficiency}°")

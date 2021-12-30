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

    fig = plotlib.plot_surface(z=angle_out, x=l, y=v)
    fig.show()

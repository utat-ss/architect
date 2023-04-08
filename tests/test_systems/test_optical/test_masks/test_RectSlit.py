"""RectSlit tests."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np
from architect.libs import utillib

# project
from architect.systems.optical.masks import RectSlit

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    slit = RectSlit()
    LOG.info(slit)


def test_get_clear_area():
    """Test get_clear_area method."""

    slit = RectSlit(size=(2 * unit.mm, 3 * unit.mm))

    result = slit.get_clear_area()
    LOG.info(result)

    assert result == 6 * unit.mm**2


def test_get_clear_area_arrays():
    height = 1 * unit.mm
    width = np.arange(start=1, stop=4, step=1) * unit.mm

    casted_dimensions = utillib.hypercast(width, height)

    slit = RectSlit(size=casted_dimensions)

    result = slit.get_clear_area().flatten()
    LOG.info(result)

    assert (result == np.array([1, 2, 3]) * unit.mm**2).all()


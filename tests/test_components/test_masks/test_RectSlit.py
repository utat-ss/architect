"""RectSlit tests."""

# stdlib
import logging

# external

# project
from architect.components.masks import RectSlit
import astropy.units as unit

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    slit = RectSlit()
    LOG.info(slit)

def test_get_clear_area():
    """Test get_clear_area method."""

    slit = RectSlit(size=(2*unit.mm, 3*unit.mm))
    
    result = slit.get_clear_area()
    LOG.info(result)

    assert result == 6*unit.mm**2
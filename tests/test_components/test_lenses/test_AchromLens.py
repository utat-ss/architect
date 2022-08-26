"""Tests for AchromLens component."""
# stdlib
import logging

# external
import pytest

# project
from architect.components import lenses

LOG = logging.getLogger(__name__)


def test_focal_length_1():
    """Test AchromLens.focal_length_1()"""

    f_eq = 50
    V_1 = 0.016
    V_2 = 0.028

    doublet = lenses.AchromLens(f_eq=f_eq, V_1=V_1, V_2=V_2)

    fl1 = doublet.focal_length_1()
    LOG.info(f"Focal length 1: {fl1}")

    assert fl1 == pytest.approx(-37.5)


def test_focal_length_2():
    """Test AchromLens.focal_length_2()"""

    f_eq = 50
    V_1 = 0.016
    V_2 = 0.028

    doublet = lenses.AchromLens(f_eq=f_eq, V_1=V_1, V_2=V_2)

    fl2 = doublet.focal_length_2()
    LOG.info(f"Focal length 2: {fl2}")

    assert fl2 == pytest.approx(350 / 3)


def test_effective_focal_length():
    """Test AchromLens.effective_focal_length()"""

    f_1 = 50
    V_1 = 0.016
    V_2 = 0.028

    doublet = lenses.AchromLens(f_1=f_1, V_1=V_1, V_2=V_2)

    fleq = doublet.effective_focal_length()
    LOG.info(f"Effective focal length: {fleq}")

    assert fleq == pytest.approx(-200 / 3)

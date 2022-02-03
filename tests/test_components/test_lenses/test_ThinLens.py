"""Tests for Thin Lens component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer.components import lenses

LOG = logging.getLogger(__name__)


def test_get_image_distance():
    """Test get_image_distance()."""

    # region parameters
    f = 5
    ans = 5
    # endregion

    # region components
    focuser = lenses.ThinLens(f=f)
    # endregion

    # region evaluation
    d_i = focuser.get_image_distance()
    # endregion

    LOG.info(
        f"""Image distance\n
    f: {f} [mm]\n
    \n
    d_i = {d_i}, {ans} (ans) [mm]"""
    )

    assert d_i == ans


def test_get_source_distance():
    """Test get_source_distance()."""

    # region parameters
    f = 5
    ans = 5
    # endregion

    # region components
    collimator = lenses.ThinLens(f=f)
    # endregion

    # region evaluation
    d_o = collimator.get_source_distance()
    # endregion

    LOG.info(
        f"""Source distance\n
    f: {f} [mm]\n
    \n
    d_o = {d_o}, {ans} (ans) [mm]"""
    )

    assert d_o == ans


def test_get_image_height():
    """Test get_image_height()."""

    # region parameters
    f = 4
    a_in = 30

    ans = 4 * math.sqrt(3) / 3
    # endregion

    # region component instantiation
    focuser = lenses.ThinLens(f=f, a_in=a_in)
    # endregion

    # region evaluation
    h_i = focuser.get_image_height()
    # endregion

    LOG.info(
        f"""Image height\n
    f: {f} [mm]\n
    a_in: {a_in} [°]\n
    \n
    h_i = {h_i}, {ans} (ans) [mm]"""
    )

    assert h_i == pytest.approx(ans)


def test_get_image_height_vectorized():
    """Test get_image_height() in vectorized mode."""

    # parameters
    f = np.array([1, 2, 3])
    a_in = np.array([15, 30, 45])

    # component instantiation
    focuser = lenses.ThinLens(f=f, a_in=a_in)

    # evaluation
    h = focuser.get_image_height()
    LOG.info(f"Image height: {h}")

    assert h == pytest.approx(4 * math.sqrt(3) / 3)


def test_get_source_height():
    """Test get_source_height()."""

    # region parameters
    f = 4
    a_in = 30

    ans = 4 * math.sqrt(3) / 3
    # endregion

    # region component instantiation
    collimator = lenses.ThinLens(f=f, a_in=a_in)
    # endregion

    # region evaluation
    h_o = collimator.get_source_height()
    # endregion

    LOG.info(
        f"""Source height\n
    f: {f} [mm]\n
    a_in: {a_in} [°]\n
    \n
    h_o = {h_o}, {ans} (ans) [mm]"""
    )

    assert h_o == pytest.approx(ans)


@pytest.mark.parametrize(
    "d_i, d_o, h_i, a_in, h_o, a_out, ans",
    [
        (5, None, None, None, None, None, 5),
        (None, 5, None, None, None, None, 5),
        (None, None, 10, 5, None, None, 114.300523),
        (None, None, None, None, 10, 5, 114.300523),
    ],
)
def test_get_focal_length(d_i, d_o, h_i, a_in, h_o, a_out, ans):
    """Tests ThinLens.get_focal_length().

    Cases:     0: d_i is set.     1: d_o is set.     2: h_i and a_in are set.     3: h_o
    and a_out are set.

    """

    # region component instantiation
    collimator = lenses.ThinLens(
        d_i=d_i, d_o=d_o, h_i=h_i, a_in=a_in, h_o=h_o, a_out=a_out
    )
    # endregion

    # region evaluation
    f = collimator.get_focal_length()
    # endregion

    LOG.info(
        f"""Focal length\n
    d_i: {d_i} [mm]\n
    d_o: {d_o} [mm]\n
    h_i: {h_i} [mm]\n
    a_in: {a_in} [°]\n
    h_o: {h_o} [mm]\n
    a_out: {a_out} [°]\n
    \n
    f = {f}, {ans} (ans) [mm]"""
    )

    assert h_o == pytest.approx(ans)

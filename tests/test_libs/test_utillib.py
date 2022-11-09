"""Tests for the utillib library."""

# stdlib
import logging

# external
import numpy as np

# project
from architect.libs import utillib

LOG = logging.getLogger(__name__)


def test_hypercast_2D():
    """Test the hypercast function with two arrays."""

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6, 7])

    a_hyper, b_hyper = utillib.hypercast(a, b)
    LOG.info(a_hyper)
    LOG.info(b_hyper)

    assert a_hyper.shape == (3, 4)
    assert b_hyper.shape == (3, 4)


def test_hypercast_3D():
    """Test the hypercast function with three arrays."""

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6, 7])
    c = np.array([8, 9, 10, 11, 12])

    a_hyper, b_hyper, c_hyper = utillib.hypercast(a, b, c)
    LOG.info(a_hyper)
    LOG.info(b_hyper)
    LOG.info(c_hyper)

    assert a_hyper.shape == (3, 4, 5)
    assert b_hyper.shape == (3, 4, 5)
    assert c_hyper.shape == (3, 4, 5)

"""Tests for the plotlib library."""

# stdlib
import logging

# external
import pytest

# project
from payload_designer.libs import plotlib

LOG = logging.getLogger(__name__)


@pytest.mark.plot
def test_line():
    """Test the line plot function."""

    x = [1, 2, 3]
    y = [1, 2, 3]

    plotlib.line(x=x, y=y)


@pytest.mark.plot
def test_scatter():
    """Test the scatter plot function."""

    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [1, 2, 3]
    w = [1, 2, 3]

    plotlib.scatter(x=x, y=y, z=z, w=w)


@pytest.mark.plot
def test_surface():
    """Test the surface plot function."""

    x = [1, 2, 3]
    y = [1, 2, 3]
    z = [[1, 2, 1], [2, 3, 2], [1, 2, 1]]

    plotlib.surface(x=x, y=y, z=z)


@pytest.mark.plot
@pytest.mark.skip(reason="Issue with Kaleido and Poetry.")
def test_save():
    """Test the figure save function."""

    x = [1, 2, 3]
    y = [1, 2, 3]
    filename = "test_save"

    fig = plotlib.scatter(x=x, y=y)
    plotlib.save(fig=fig, filename=filename)

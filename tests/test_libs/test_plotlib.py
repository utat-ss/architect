"""Tests for the plotlib library."""

# stdlib
import logging
import math

# external
import numpy as np
import pandas as pd
import pytest

# project
from payload_designer.libs import plotlib, utillib

LOG = logging.getLogger(__name__)


@pytest.mark.plot
def test_line():
    """Test the line plot function with full dimensionality."""

    # region parameters
    x = np.linspace(start=-5, stop=5, num=16)
    a = np.arange(start=1, stop=4, step=1)
    b = np.arange(start=1, stop=4, step=1)
    # endregion

    # region broadcasting
    shape = (x.size, a.size, b.size)

    x = utillib.orient_and_broadcast(a=x, dim=0, shape=shape)
    a = utillib.orient_and_broadcast(a=a, dim=1, shape=shape)
    b = utillib.orient_and_broadcast(a=b, dim=2, shape=shape)
    # endregion

    # region evaluation
    y = a * x + b
    # endregion

    # region plot
    dfd = {"x": x.flatten(), "y": y.flatten(), "a": a.flatten(), "b": b.flatten()}
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.line(
        df=df,
        x="x",
        y="y",
        fc="a",
        fr="b",
        title="Test Line Plot",
    )
    # endregion


@pytest.mark.plot
def test_line_multiple_traces():
    """Test the line plot function with multiple traces and error bars."""

    # region parameters
    x = np.linspace(start=-math.pi, stop=math.pi, num=64)
    # endregion

    # region evaluation
    y1 = np.sin(x)
    y2 = np.cos(x)

    x_error = 0.05
    y_error = (y1 + y2) * 0.05
    # endregion

    # region plot
    dfd = {"$x$": x, "$y_1$": y1, "$y_2$": y2, "x_error": x_error, "y_error": y_error}
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.line(
        df=df,
        x="$x$",
        y=["$y_1$", "$y_2$"],
        x_error="x_error",
        y_error="y_error",
        title="Test Line Plot With Multiple Traces and Error Bars",
    )
    # endregion


@pytest.mark.plot
def test_scatter():
    """Test the scatter plot function with full dimensionality."""

    # region parameters
    x = np.linspace(start=-3, stop=3, num=16)
    a = np.arange(start=-3, stop=4, step=1)
    b = np.arange(start=1, stop=4, step=1)
    c = np.arange(start=-3, stop=4, step=1)
    d = np.arange(start=1, stop=4, step=1)
    e = np.arange(start=1, stop=4, step=1)
    # endregion

    # region broadcasting
    shape = (x.size, a.size, b.size, c.size, d.size, e.size)

    x = utillib.orient_and_broadcast(a=x, dim=0, shape=shape)
    a = utillib.orient_and_broadcast(a=a, dim=1, shape=shape)
    b = utillib.orient_and_broadcast(a=b, dim=2, shape=shape)
    c = utillib.orient_and_broadcast(a=c, dim=3, shape=shape)
    d = utillib.orient_and_broadcast(a=d, dim=4, shape=shape)
    e = utillib.orient_and_broadcast(a=e, dim=5, shape=shape)
    # endregion

    # region evaluate
    y = a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e
    # endregion

    # region plot
    dfd = {
        "x": x.flatten(),
        "y": y.flatten(),
        "a": a.flatten(),
        "b": b.flatten(),
        "c": c.flatten(),
        "d": d.flatten(),
        "e": e.flatten(),
    }
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.scatter(
        df=df,
        x="x",
        y="y",
        c="a",
        s="b",
        m="c",
        fc="d",
        fr="e",
        title="Test Scatter Plot",
    )
    # endregion


@pytest.mark.plot
def test_scatter3():
    """Test the scatter3 plot function with full dimensionality."""

    # region parameters
    x = np.linspace(start=-3, stop=3, num=16)
    y = np.linspace(start=-3, stop=3, num=16)
    a = np.arange(start=-3, stop=4, step=1)
    b = np.arange(start=1, stop=4, step=1)
    c = np.arange(start=-3, stop=4, step=1)
    # endregion

    # region broadcasting
    shape = (x.size, y.size, a.size, b.size, c.size)

    x = utillib.orient_and_broadcast(a=x, dim=0, shape=shape)
    y = utillib.orient_and_broadcast(a=y, dim=1, shape=shape)
    a = utillib.orient_and_broadcast(a=a, dim=2, shape=shape)
    b = utillib.orient_and_broadcast(a=b, dim=3, shape=shape)
    c = utillib.orient_and_broadcast(a=c, dim=4, shape=shape)
    # endregion

    # region evaluate
    z = a * (np.sin(b * x) + np.cos(c * y))
    # endregion

    # region plot
    dfd = {
        "x": x.flatten(),
        "y": y.flatten(),
        "z": z.flatten(),
        "a": a.flatten(),
        "b": b.flatten(),
        "c": c.flatten(),
    }
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.scatter3(
        df=df,
        x="x",
        y="y",
        z="a",
        c="z",
        s="b",
        m="c",
        title="Test Scatter3 Plot",
    )
    # endregion


@pytest.mark.plot
def test_surface():
    """Test the surface plot function."""
    # region parameters
    x = np.linspace(start=-5, stop=5, num=16)
    y = np.linspace(start=-5, stop=5, num=16)
    # endregion

    # region broadcasting
    shape = (x.size, y.size)

    x_broad = utillib.orient_and_broadcast(a=x, dim=0, shape=shape)
    y_broad = utillib.orient_and_broadcast(a=y, dim=1, shape=shape)
    # endregion

    # region evaluation
    z = np.cos(np.sqrt((x_broad ** 2 + y_broad ** 2))) / np.exp(
        (x_broad ** 2 + y_broad ** 2) * 0.001
    )
    LOG.debug(z)
    # endregion

    # region plot
    plotlib.surface(
        x=x,
        y=y,
        z=z,
        title="Test Surface Plot",
        title_x="x",
        title_y="y",
        title_z="z",
    )
    # endregion


@pytest.mark.plot
@pytest.mark.skip(reason="Issue with Kaleido and Poetry.")
def test_save():
    """Test the figure save function."""

    x = [1, 2, 3]
    y = [1, 2, 3]
    filename = "test_save"

    fig = plotlib.scatter(x=x, y=y)
    plotlib.save(fig=fig, filename=filename)

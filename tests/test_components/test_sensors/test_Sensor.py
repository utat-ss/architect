"""Tests for Sensor component."""
# stdlib
import logging

# external
import astropy.units as unit

# project
from architect.components.sensors import Sensor

LOG = logging.getLogger(__name__)


def test_init():
    """Test init method."""

    sensor = Sensor()
    LOG.info(sensor)


def test_get_size():
    """Test get_size method."""

    sensor = Sensor(n_px=(640, 512), pitch=10 * unit.um)

    result = sensor.get_shape()
    LOG.info(result)

    assert result[0].decompose().unit == unit.m
    assert result[1].decompose().unit == unit.m


def test_get_area():
    """Test get_area method."""

    sensor = Sensor(n_px=(640, 512), pitch=10 * unit.um)

    result = sensor.get_area()
    LOG.info(result)

    assert result.decompose().unit == unit.m**2

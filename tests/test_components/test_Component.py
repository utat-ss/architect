"""Tests for the Component class."""

# stdlib
import logging

# project
from architect.components import Component

LOG = logging.getLogger(__name__)


def test_init():
    """Test the init method."""
    component = Component()

    LOG.info(component)


def test_get_volume():
    """Test the get volume method."""
    ans = 7
    component = Component(dimensions=(1, 2, 3))

    volume = component.get_volume()

    LOG.info(component)
    LOG.info(f"Expected: {ans}\tResult: {volume}")
    assert volume == ans

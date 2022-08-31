"""Tests for the artfact class."""

# stdlib
import logging

# external
from architect import Artifact

LOG = logging.getLogger(__name__)


def test_get_attrs_table():
    """Test the get_attrs_table method."""
    artifact = Artifact()

    artifact.some_property = "some_value"

    table = artifact.get_attrs_table()

    LOG.info(f"Attribute table:\n{table}")


def test_to_latex():
    """Test the get_attrs_table method."""
    artifact = Artifact()

    artifact.some_property = "some_value"

    table = artifact.to_latex()

    LOG.info(f"Attribute LaTeX table:\n{table}")
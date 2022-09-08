"""Tests for the Artifact class."""

# stdlib
import logging

# project
from architect import Artifact

LOG = logging.getLogger(__name__)


def test_get_attrs_table():
    """Test get_attrs_table method."""
    artifact = Artifact()

    artifact.some_property = "some_value"

    table = artifact.get_attrs_table()

    LOG.info(f"Attribute table:\n{table}")


def test_to_latex():
    """Test to_latex method."""
    artifact = Artifact()

    artifact.some_property = "some_value"

    table = artifact.to_latex()

    LOG.info(f"Attribute LaTeX table:\n{table}")

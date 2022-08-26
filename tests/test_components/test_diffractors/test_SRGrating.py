"""Tests for SRTGrating component."""
# stdlib
import logging

# project
from architect.components.diffractors import SRTGrating

LOG = logging.getLogger(__name__)


def test_get_emergent_angle():
    """Test get_emergent_angle method."""
    grating = SRTGrating()
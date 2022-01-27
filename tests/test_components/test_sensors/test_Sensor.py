"""Tests for Sensor component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer.componentss import sensors

LOG = logging.getLogger(__name__)


def test_get_snr():
    """Test Sensor.get_snr()."""

    # region parameters
    i_dark = 50

    ans = 1.0
    # endregion

    # region component instantiation
    sensor = sensors.Sensor(i_dark=i_dark)
    # endregion

    # region evaluation
    snr = sensor.get_snr()
    # endregion

    LOG.info(
        f"""Image distance\n
    i_dark: {i_dark} [ke-/s]\n
    \n
    SNR = {snr}, {ans} (ans)"""
    )

    assert snr == pytest.approx(ans)

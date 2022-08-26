# stdlib
import logging

# external
import astropy.units as unit
import numpy as np
import pytest

# project
from architect import components, systems
from architect.systems.payloads import HyperspectralImager

LOG = logging.getLogger(__name__)


@pytest.mark.star
def test_get_mapped_height_sensor():
    """Test the method that maps wavelength onto sensor."""
    # region params
    wavelength = 1300

    # endregion

    # region instantiation
    foreoptic = components.foreoptics.Chromar()
    slit = components.masks.RectSlit()
    collimator = components.lenses.Lens()
    bandfilter = components.filters.DichroicBandFilter()
    grism = components.diffractors.VPHGrism(apex_angle=45, index_prism=1, index_seal=1, fringe_frequency=600)
    focuser = components.lenses.Lens(focal_length=12)

    payload = systems.payloads.FINCHEye(
        foreoptic=foreoptic,
        slit=slit,
        collimator=collimator,
        bandfilter=bandfilter,
        grism=grism,
        focuser=focuser,
        )
    # endregion

    # region pipeline
    sensor_height = payload.get_mapped_height_sensor(wavelength=wavelength)
    LOG.info(f"Sensor Height: {sensor_height}")
    # endregion

    assert sensor_height == 0
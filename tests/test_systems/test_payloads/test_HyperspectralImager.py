"""Tests for hyperspectral imager system."""
# stdlib
import logging

# external
import pytest
import astropy.units as unit
import numpy as np
from payload_designer.libs import utillib
from payload_designer import luts

# project
from payload_designer.systems.payloads import HyperspectralImager
from payload_designer.components.masks import RectSlit
from payload_designer.components.foreoptics import Foreoptic
from payload_designer.components.sensors import TauSWIR

LOG = logging.getLogger(__name__)

@pytest.mark.star
def test_ratio_cropped_light_through_slit():
    """Test that the ratio of cropped light through the slit is correct."""
    
    slit = RectSlit(size=(20,1)*unit.mm)
    foreoptic = Foreoptic(image_diameter=20*unit.mm)
    payload = HyperspectralImager(slit=slit, foreoptic=foreoptic)
    
    ratio = payload.get_ratio_cropped_light_through_slit()

    LOG.info(f"Ratio: {ratio}")



def test_get_signal_to_noise():
    """"Test the SNR function."""

    wavelength = np.arange(start=900, stop=1700, step=25) * unit.nm

    # components
    sensor = TauSWIR()
    foreoptic = Foreoptic(focal_length=100 * unit.mm, diameter=10 * unit.cm)
    slit = RectSlit(size=(1 * unit.mm, 20 * unit.mm))

    # systems
    payload = HyperspectralImager(sensor=sensor, foreoptic=foreoptic, slit=slit)

    radiance = luts.load("atmosphere/radiance_min")
    snr = payload.get_signal_to_noise(radiance=radiance, wavelength=wavelength)

    LOG.info(f"SNR: {snr}")


def test_get_f_number_units():
    foreoptic = Foreoptic(focal_length=100 * unit.mm, diameter=10 * unit.cm)

    result = foreoptic.get_f_number()
    result_simplified = result.decompose() * unit.sr

    LOG.debug(f"F number: {result_simplified}")
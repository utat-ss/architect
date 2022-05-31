
import astropy.units as unit
from colorama import Fore
import numpy as np
import pandas as pd
import logging
from IPython.display import display

# project
from payload_designer import components, systems
from payload_designer.libs import utillib


from payload_designer.components.sensors import TauSWIR
from payload_designer.components.foreoptics import Foreoptic

from payload_designer.systems.payloads import HyperspectralImager

LOG = logging.getLogger(__name__)

def test_get_optical_spectral_resolution():
    '''Test of get_optical_spectral_resolution function'''

    target_wavelength = 1650 * unit.nm
    diameter = 100 * unit.mm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1/unit.mm)


    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

    HP = HyperspectralImager(sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating)

    optical_spectral_resolution = HP.get_optical_spectral_resolution(target_wavelength=target_wavelength, beam_diameter=25*unit.mm)
    

    LOG.info(f"Optical Specral resolution: {optical_spectral_resolution}")

    assert optical_spectral_resolution == 0.11 * unit.nm


def test_get_sensor_spectral_resolution():
    '''Test of get_optical_spectral_resolution function'''

  
    diameter = 100 * unit.mm
    upper_wavelength = 1700 * unit.nm
    lower_wavelength = 900 * unit.nm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1/unit.mm)


    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

    HP = HyperspectralImager(sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating)

    sensor_spectral_resolution = HP.get_sensor_spectral_resolution(upper_wavelength=upper_wavelength, lower_wavelength=lower_wavelength, beam_diameter=25*unit.mm)
    

    LOG.info(f"Sensor Specral resolution: {sensor_spectral_resolution}")

    assert sensor_spectral_resolution == 1.5625 * unit.nm

def test_get_spectral_resolution():
    '''Test of get_optical_spectral_resolution function'''

    target_wavelength = 1650 * unit.nm
    diameter = 100 * unit.mm
    upper_wavelength = 1700 * unit.nm
    lower_wavelength = 900 * unit.nm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1/unit.mm)


    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

    HP = HyperspectralImager(sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating)

    spectral_resolution = HP.get_spectral_resolution(upper_wavelength=upper_wavelength, lower_wavelength=lower_wavelength, target_wavelength=target_wavelength, beam_diameter=[25, 25]*unit.mm)
    

    LOG.info(f"Specral resolution: {spectral_resolution}")

    assert spectral_resolution == [1.5625, 1.5625] * unit.nm
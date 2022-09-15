"""Tests for hyperspectral imager system."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np

# project
from architect import components, luts
from architect.components.foreoptics import Foreoptic
from architect.components.masks import RectSlit
from architect.components.sensors import Sensor
from architect.systems.spectrometers import HyperspectralImager

LOG = logging.getLogger(__name__)


def test_init():
    """Test the init method."""

    spectrometer = HyperspectralImager()
    LOG.info(spectrometer)


def test_get_transmittance():
    """Test get_transmittance method."""

    spectrometer = HyperspectralImager(foreoptic=Foreoptic(transmittance=0.5))

    result = spectrometer.get_transmittance()
    LOG.info(result)

    assert result.unit == unit.percent


def test_get_ratio_cropped_light_through_slit():
    """Test get_ratio_cropped_light_through_slit."""
    hyperspec = HyperspectralImager(
        foreoptic=Foreoptic(), slit=RectSlit(size=[4, 5] * unit.mm)
    )
    result = hyperspec.get_ratio_cropped_light_through_slit()
    LOG.info(result)

    assert result.decompose().unit == unit.dimensionless_unscaled


def test_get_signal_to_noise():
    """Test get_signal_to_noise method."""

    wavelength = np.arange(start=900, stop=1700, step=100) * unit.nm
    sensor = Sensor()
    foreoptic = Foreoptic(
        focal_length=100 * unit.mm, diameter=10 * unit.cm, image_diameter=20 * unit.mm
    )
    slit = RectSlit(size=(1 * unit.mm, 20 * unit.mm))
    radiance = luts.load("atmosphere/radiance_min")
    payload = HyperspectralImager(sensor=sensor, foreoptic=foreoptic, slit=slit)

    result = payload.get_signal_to_noise(radiance=radiance, wavelength=wavelength)
    LOG.info(result)

    assert result.decompose().unit == unit.dimensionless_unscaled


def test_get_optical_spatial_resolution():
    """Test the optically-limited spatial resolution method."""
    raise ValueError


def test_get_sensor_spatial_resolution():
    """Test the sensor-limited spatial resolution method."""
    raise ValueError


def test_get_spatial_resolution():
    """Test get_spatial_resolution."""
    wavelength = 400 * unit.nm
    target_distance = 1 * unit.km

    sensor = components.sensors.TauSWIR()
    foreoptic = components.foreoptics.Chromar()
    system = HyperspectralImager(sensor=sensor, foreoptic=foreoptic)

    result = system.get_spatial_resolution(
        wavelength=wavelength, target_distance=target_distance
    )
    LOG.info(result)

    assert result.decompose().unit == unit.m


def test_get_optical_spectral_resolution():
    """Test get_optical_spectral_resolution function."""
    raise ValueError


def test_get_sensor_spectral_resolution():
    """Test of get_optical_spectral_resolution."""
    raise ValueError


def test_get_spectral_resolution():
    """Test get_optical_spectral_resolution."""

    system = HyperspectralImager(sensor=Sensor())
    result = system.get_spectral_resolution(
        lower_wavelength=900 * unit.nm,
        upper_wavelength=1700 * unit.nm,
        target_wavelength=1300 * unit.nm,
        beam_diameter=25 * unit.mm,
    )
    LOG.info(result)

    assert result.decompose().unit == unit.m


def test_get_pointing_accuracy_constraint():
    """Test get_pointing_accuracy_constraint."""
    system = HyperspectralImager(
        sensor=Sensor(),
        foreoptic=Foreoptic(diameter=10 * unit.mm, focal_length=100 * unit.mm),
    )

    result = system.get_pointing_accuracy_constraint(
        wavelength=400 * unit.nm,
        target_distance=1 * unit.km,
    )
    LOG.info(result.to(unit.degree))

    assert result.unit == unit.rad

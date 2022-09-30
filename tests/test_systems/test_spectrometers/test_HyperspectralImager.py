"""Tests for hyperspectral imager system."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np

# project
from architect import components, luts
from architect.components.diffractors import TransmissiveDiffractor
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
        foreoptic=Foreoptic(image_diameter=25 * unit.mm),
        slit=RectSlit(size=[4, 5] * unit.mm),
    )
    result = hyperspec.get_ratio_cropped_light_through_slit()
    LOG.info(result)

    assert result.decompose().unit == unit.dimensionless_unscaled


def test_get_signal_to_noise():
    """Test get_signal_to_noise."""

    system = HyperspectralImager(
        sensor=Sensor(
            integration_time=10 * unit.ms,
            pitch=10 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            i_dark=10000 * (unit.electron / unit.pix / unit.s),
        ),
        foreoptic=Foreoptic(
            focal_length=100 * unit.mm,
            diameter=50 * unit.mm,
            image_diameter=25 * unit.mm,
        ),
        slit=RectSlit(size=[1, 15] * unit.mm),
    )

    result = system.get_signal_to_noise(
        radiance=luts.load("atmosphere/radiance_min"), wavelength=400 * unit.nm
    )

    assert result.decompose().unit == unit.dimensionless_unscaled


def test_get_optical_spatial_resolution():
    """Test get_optical_spatial_resolution."""

    system = HyperspectralImager(foreoptic=Foreoptic(diameter=100 * unit.mm))
    result = system.get_optical_spatial_resolution(
        wavelength=400 * unit.nm, target_distance=1 * unit.km
    )
    LOG.info(result)

    assert result.decompose().unit == unit.m


def test_get_sensor_spatial_resolution():
    """Test the sensor-limited spatial resolution method."""
    system = HyperspectralImager(
        sensor=Sensor(pitch=15 * unit.um),
        foreoptic=Foreoptic(focal_length=100 * unit.mm),
    )

    result = system.get_sensor_spatial_resolution(target_distance=1 * unit.km)
    LOG.info(result)

    assert result.decompose().unit == unit.m


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
    """Test get_optical_spectral_resolution."""

    system = HyperspectralImager(
        diffractor=TransmissiveDiffractor(fringe_frequency=600 * 1 / unit.mm)
    )
    result = system.get_optical_spectral_resolution(
        target_wavelength=1300 * unit.nm, beam_diameter=25 * unit.mm
    )
    LOG.info(result.decompose())

    assert result.decompose().unit == unit.m


def test_get_sensor_spectral_resolution():
    """Test get_sensor_spectral_resolution."""
    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            n_bin=1 * unit.dimensionless_unscaled,
            n_px=(640, 512) * unit.pix,
        )
    )
    result = system.get_sensor_spectral_resolution(
        upper_wavelength=1700 * unit.nm, lower_wavelength=900 * unit.nm
    )
    LOG.info(result)

    assert result.decompose().unit == unit.m / unit.pix


def test_get_spectral_resolution():
    """Test get_optical_spectral_resolution."""

    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            n_bin=1 * unit.dimensionless_unscaled,
            n_px=(640, 512) * unit.pix,
        ),
        diffractor=TransmissiveDiffractor(fringe_frequency=600 * (1 / unit.mm)),
    )
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
        sensor=Sensor(
            pitch=15 * unit.um,
            n_bin=1 * unit.dimensionless_unscaled,
            n_px=(640, 512) * unit.pix,
        ),
        diffractor=TransmissiveDiffractor(fringe_frequency=600 * (1 / unit.mm)),
        foreoptic=Foreoptic(diameter=10 * unit.mm, focal_length=100 * unit.mm),
    )

    result = system.get_pointing_accuracy_constraint(
        wavelength=400 * unit.nm,
        target_distance=1 * unit.km,
    )
    LOG.info(result.to(unit.degree))

    assert result.unit == unit.rad

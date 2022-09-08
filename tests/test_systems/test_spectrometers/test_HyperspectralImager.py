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
from architect.components.sensors import TauSWIR
from architect.systems.spectrometers import HyperspectralImager

LOG = logging.getLogger(__name__)


def test_init():
    """Test the init method."""

    spectrometer = HyperspectralImager()
    LOG.info(spectrometer)


def test_get_transmittance():
    """Test get_transmittance method."""

    spectrometer = HyperspectralImager(foreoptic=Foreoptic())

    result = spectrometer.get_transmittance()
    LOG.info(result)

    assert result.unit == unit.percent


def test_ratio_cropped_light_through_slit():
    """Test that the ratio of cropped light through the slit is correct."""

    slit = RectSlit(size=(20, 1) * unit.mm)
    foreoptic = Foreoptic(image_diameter=20 * unit.mm)
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
    """Test that the f-number has units of steradian."""
    foreoptic = Foreoptic(focal_length=100 * unit.mm, diameter=10 * unit.cm)

    result = foreoptic.get_f_number()
    result_simplified = result.decompose() * unit.sr

    LOG.debug(f"F number: {result_simplified}")


def test_get_optical_spatial_resolution():
    """Test the optically-limited spatial resolution method."""

    # region params
    wavelength = 400 * unit.nm
    target_distance = 1 * unit.km
    # endregion

    # region instantiation
    foreoptic = components.foreoptics.Chromar()
    system = HyperspectralImager(foreoptic=foreoptic)
    # endregion

    # region pipeline
    res = system.get_optical_spatial_resolution(
        wavelength=wavelength, target_distance=target_distance
    )
    LOG.info(f"Optically-limited spatial resolution: {res}")
    # endregion


def test_get_sensor_spatial_resolution():
    """Test the sensor-limited spatial resolution method."""

    # region params
    target_distance = 1 * unit.km
    # endregion

    # region instantiation
    sensor = components.sensors.TauSWIR()
    foreoptic = components.foreoptics.Chromar()
    system = HyperspectralImager(sensor=sensor, foreoptic=foreoptic)
    # endregion

    # region pipeline
    res = system.get_sensor_spatial_resolution(target_distance=target_distance)
    LOG.info(f"Sensor-limited spatial resolution: {res}")
    # endregion


def test_get_spatial_resolution():
    """Test the net spatial resolution method."""

    # region params
    wavelength = 400 * unit.nm
    target_distance = 1 * unit.km
    # endregion

    # region instantiation
    sensor = components.sensors.TauSWIR()
    foreoptic = components.foreoptics.Chromar()
    system = HyperspectralImager(sensor=sensor, foreoptic=foreoptic)
    # endregion

    # region pipeline
    res = system.get_spatial_resolution(
        wavelength=wavelength, target_distance=target_distance
    )
    LOG.info(f"Spatial resolution: {res}")
    # endregion


def test_get_optical_spectral_resolution():
    """Test of get_optical_spectral_resolution function."""

    target_wavelength = 1650 * unit.nm
    diameter = 100 * unit.mm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1 / unit.mm)

    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.TransmissiveDiffractor(
        fringe_frequency=fringe_frequency
    )

    HP = HyperspectralImager(
        sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating
    )

    optical_spectral_resolution = HP.get_optical_spectral_resolution(
        target_wavelength=target_wavelength, beam_diameter=25 * unit.mm
    )

    LOG.info(f"Optical Specral resolution: {optical_spectral_resolution}")

    assert optical_spectral_resolution == 0.11 * unit.nm


def test_get_sensor_spectral_resolution():
    """Test of get_optical_spectral_resolution function."""

    diameter = 100 * unit.mm
    upper_wavelength = 1700 * unit.nm
    lower_wavelength = 900 * unit.nm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1 / unit.mm)

    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.TransmissiveDiffractor(
        fringe_frequency=fringe_frequency
    )

    HP = HyperspectralImager(
        sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating
    )

    sensor_spectral_resolution = HP.get_sensor_spectral_resolution(
        upper_wavelength=upper_wavelength,
        lower_wavelength=lower_wavelength,
        beam_diameter=25 * unit.mm,
    )

    LOG.info(f"Sensor Specral resolution: {sensor_spectral_resolution}")

    assert sensor_spectral_resolution == 1.5625 * unit.nm


def test_get_spectral_resolution():
    """Test of get_optical_spectral_resolution function."""

    target_wavelength = 1650 * unit.nm
    diameter = 100 * unit.mm
    upper_wavelength = 1700 * unit.nm
    lower_wavelength = 900 * unit.nm
    slit_size = np.array([3, 1]) * unit.mm
    focal_length = 100 * unit.mm
    fringe_frequency = 600 * (1 / unit.mm)

    sensor = TauSWIR()
    foreoptic = Foreoptic(diameter=diameter, focal_length=focal_length)
    slit = components.masks.RectSlit(size=slit_size)

    sr_grating = components.diffractors.TransmissiveDiffractor(
        fringe_frequency=fringe_frequency
    )

    HP = HyperspectralImager(
        sensor=sensor, foreoptic=foreoptic, slit=slit, diffractor=sr_grating
    )

    spectral_resolution = HP.get_spectral_resolution(
        upper_wavelength=upper_wavelength,
        lower_wavelength=lower_wavelength,
        target_wavelength=target_wavelength,
        beam_diameter=[25, 25] * unit.mm,
    )

    LOG.info(f"Specral resolution: {spectral_resolution}")

    assert spectral_resolution == [1.5625, 1.5625] * unit.nm


def test_get_pointing_accuracy_constraint():
    """Test the get pointing accuracy constraint method."""

    # region params
    wavelength = 400 * unit.nm
    target_distance = 1 * unit.km
    # endregion

    # region instantiation
    sensor = components.sensors.TauSWIR()
    foreoptic = components.foreoptics.Chromar()
    system = HyperspectralImager(sensor=sensor, foreoptic=foreoptic)
    # endregion

    # region pipeline
    res = system.get_pointing_accuracy_constraint(
        wavelength=wavelength,
        target_distance=target_distance,
    )
    LOG.info(f"Pointing accuracy constraint: {res}")
    # endregion

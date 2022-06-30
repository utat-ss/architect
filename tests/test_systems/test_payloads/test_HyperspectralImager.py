# stdlib
import logging

# external
import astropy.units as unit
import numpy as np

# project
from payload_designer import components, systems
from payload_designer.systems.payloads import HyperspectralImager

LOG = logging.getLogger(__name__)


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

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

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

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

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

    sr_grating = components.diffractors.SRTGrating(fringe_frequency=fringe_frequency)

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
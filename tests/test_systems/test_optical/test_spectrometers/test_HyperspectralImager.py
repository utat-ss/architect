"""Tests for hyperspectral imager system."""

# stdlib
import logging

# external
import astropy.units as unit
import numpy as np

# project
from architect import luts
from architect.systems.optical.diffractors import TransmissiveDiffractor
from architect.systems.optical.foreoptics import Foreoptic
from architect.systems.optical.lenses import Lens
from architect.systems.optical.masks import RectSlit
from architect.systems.optical.sensors import Sensor
from architect.systems.optical.spectrometers import HyperspectralImager

LOG = logging.getLogger(__name__)


def test_init():
    """Test the init method."""

    spectrometer = HyperspectralImager()
    LOG.info(spectrometer)


def test_get_transmittance():
    """Test get_transmittance method."""

    spectrometer = HyperspectralImager(transmittance=50 * unit.pct)

    result = spectrometer.get_transmittance()
    LOG.info(result)

    assert result == 50 * unit.pct


def test_get_transmittance_from_subsystems():
    """Test get_transmittance method from subsystems."""

    spectrometer = HyperspectralImager(
        foreoptic=Foreoptic(transmittance=50 * unit.pct),
        lens=Lens(transmittance=25 * unit.pct),
    )

    result = spectrometer.get_transmittance()
    LOG.info(result)

    ans = unit.isclose(a=result, b=12.5 * unit.pct)

    assert ans


def test_get_transmittance_from_LUT():
    """Test get_transmittance method with LUTs."""

    spectrometer = HyperspectralImager(transmittance=luts.load("test_lut"))

    result = spectrometer.get_transmittance(wavelength=1300 * unit.nm)
    LOG.info(result)


def test_get_transmittance_from_subsystem_LUTs():
    """Test get_transmittance method from subsystems with multiple LUTs."""

    spectrometer = HyperspectralImager(
        foreoptic=Foreoptic(transmittance=luts.load("test_lut")),
        lens=Lens(transmittance=luts.load("test_lut")),
    )

    result = spectrometer.get_transmittance(
        wavelength=np.arange(900, 1700, 10) * unit.nm
    )
    LOG.info(result)

    assert result.unit == unit.pct


def test_get_ratio_cropped_light_through_slit():
    """Test get_ratio_cropped_light_through_slit."""
    hyperspec = HyperspectralImager(
        foreoptic=Foreoptic(image_diameter=25 * unit.mm),
        slit=RectSlit(size=[4, 5] * unit.mm),
    )
    result = hyperspec.get_ratio_cropped_light_through_slit()
    LOG.info(result)

    assert result.decompose().unit == unit.dimensionless_unscaled


def test_get_signal():
    """Test get_signal method."""
    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            integration_time=100 * unit.ms,
            waveband=800 * unit.m,
        ),
        foreoptic=Foreoptic(
            focal_length=100 * unit.mm,
            diameter=100 * unit.mm,
            image_diameter=25 * unit.mm,
        ),
        slit=RectSlit(size=[1, 15] * unit.mm),
    )

    result = system.get_signal(
        wavelength=400 * unit.nm,
        radiance=luts.load("atmosphere/radiance_min"),
    )

    assert result.decompose().unit == unit.electron


def test_get_signal_constants():
    """Test get_signal method."""
    system = HyperspectralImager()

    result = system.get_signal_constants()
    LOG.info(result)

    assert result.decompose().unit == 1 / (unit.joule * unit.m)


def test_get_signal_sensor():
    """Test get_signal_sensor method."""
    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            integration_time=100 * unit.ms,
        )
    )

    result = system.get_signal_sensor(wavelength=400 * unit.nm)
    LOG.info(result)

    assert result.decompose().unit == unit.electron * (unit.meter) ** 2 * unit.second


def test_get_signal_optic():
    """Test get_signal_optic method."""
    system = HyperspectralImager(
        foreoptic=Foreoptic(
            focal_length=100 * unit.mm,
            diameter=100 * unit.mm,
            image_diameter=25 * unit.mm,
        ),
        slit=RectSlit(size=[1, 15] * unit.mm),
    )

    result = system.get_signal_optic(wavelength=400 * unit.nm)
    LOG.info(result)

    assert result.unit == unit.pct


def test_get_signal_light():
    """Test get_signal_light method."""
    system = HyperspectralImager(sensor=Sensor(waveband=800 * unit.nm))

    result = system.get_signal_light(
        wavelength=400 * unit.nm, radiance=luts.load("atmosphere/radiance_min")
    )
    LOG.info(result)

    assert result.decompose().unit == unit.Watt / unit.meter


def test_get_noise():
    """Test get_noise method."""
    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            integration_time=100 * unit.ms,
            n_bin=1,
            i_dark=10000 * (unit.electron / unit.pix / unit.s),
            waveband=800 * unit.m,
            n_well=19 * 1e3 * unit.electron,
            n_bit=14 * unit.bit,
            noise_read=500 * unit.electron,
        ),
        foreoptic=Foreoptic(
            focal_length=100 * unit.mm,
            diameter=100 * unit.mm,
            image_diameter=25 * unit.mm,
        ),
        slit=RectSlit(size=[1, 15] * unit.mm),
    )

    result = system.get_noise(
        wavelength=400 * unit.nm,
        radiance=luts.load("atmosphere/radiance_min"),
    )

    assert result.decompose().unit == unit.electron


def test_get_shot_noise():
    """Test get_shot_noise method."""
    system = HyperspectralImager(
        sensor=Sensor(
            pitch=15 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            integration_time=100 * unit.ms,
            n_bin=1,
            i_dark=10000 * (unit.electron / unit.pix / unit.s),
            waveband=800 * unit.nm,
        ),
        foreoptic=Foreoptic(
            focal_length=100 * unit.mm,
            diameter=100 * unit.mm,
            image_diameter=25 * unit.mm,
        ),
        slit=RectSlit(size=[1, 15] * unit.mm),
    )

    result = system.get_shot_noise(
        wavelength=400 * unit.nm,
        radiance=luts.load("atmosphere/radiance_min"),
    )

    assert result.decompose().unit == unit.electron


def test_get_signal_to_noise():
    """Test get_signal_to_noise."""

    system = HyperspectralImager(
        sensor=Sensor(
            integration_time=10 * unit.ms,
            pitch=10 * unit.um,
            efficiency=luts.load("sensors/tauswir_quantum_efficiency"),
            i_dark=10000 * (unit.electron / unit.pix / unit.s),
            n_bin=1,
            n_well=19 * 1e3 * unit.electron,
            n_bit=14 * unit.bit,
            noise_read=500 * unit.electron,
            waveband=800 * unit.m,
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
    """Test get_sensor_spatial_resolution method."""
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

    sensor = Sensor(pitch=15 * unit.m)
    foreoptic = Foreoptic(focal_length=100 * unit.mm, diameter=50 * unit.mm)
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


def test_get_ground_target_error():
    """Test get_ground_target_error method."""

    spectrometer = HyperspectralImager()

    orbital_altitude = 550 * unit.km
    skew_angle = 30 * unit.deg
    pointing_accuracy = 0.001 * unit.deg

    result = spectrometer.get_ground_target_error(
        orbital_altitude, skew_angle, pointing_accuracy
    )
    LOG.info(result)

    assert result.decompose().unit == unit.m

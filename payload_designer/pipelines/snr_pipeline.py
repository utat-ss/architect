"""Compute SNR as function of wavelength."""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np

# project
from payload_designer import components
from payload_designer.libs import plotlib, utillib

# region path config
filename = Path(__file__).stem
output_path = Path(f"output/{filename}")
log_path = Path(f"logs/{filename}")
# endregion

# region logging config
log_path.mkdir(parents=True, exist_ok=True)
logging.config.fileConfig(fname="log.conf", defaults={"path": log_path})
LOG = logging.getLogger(__name__)
# endregion

# region parameter config
lmbda = np.linspace(start=1600, stop=1700, num=100)  # wavelengths [nm]
f_n = 1.5

# LUTS
foreoptic_LUT_path = Path("data/foreoptic_transmittance.csv")
collimator_LUT_path = Path("data/collimator_transmittance.csv")
bandfilter_LUT_path = Path("data/filter_transmittance.csv")
diffractor_LUT_path = Path("data/vphgrism_transmittance.csv")
focuser_LUT_path = Path("data/focuser_transmittance.csv")
sensor_LUT_path = Path("data/sensor_quantum_efficiency.csv")

radiance_LUT_path = Path("data/atmos_radiance_max.csv")
# endregion

if __name__ == "__main__":
    # region component instantiation
    foreoptic = components.Foreoptic(eta=foreoptic_LUT_path)
    collimator = components.AchromLens(eta=collimator_LUT_path)
    # bandfilter = components.Filter(eta=bandfilter_LUT_path)
    diffractor = components.VPHGrism(eta=diffractor_LUT_path)
    focuser = components.AchromLens(eta=focuser_LUT_path)
    sensor = components.Sensor(
        eta_sensor=sensor_LUT_path,
        p=15,
        i_dark=28,
        dt=0.1667,
        n_bin=1,
        n_bit=14,
        n_well=19,
        sigma_read=50,
    )
    # endregion

    # region unit unit conversions
    lmbda = lmbda * 10 ** -9  # nm to m
    # endregion

    # region pipeline
    eta_optics = (
        foreoptic.eta(lmbda)
        * collimator.eta(lmbda)
        # * bandfilter.eta(lmbda)
        * diffractor.eta(lmbda)
        * focuser.eta(lmbda)
    )
    LOG.info(f"Optical transmittance: {eta_optics}%")

    snr, signal, noise = sensor.get_snr(
        L_target=radiance_LUT_path, eta_optics=eta_optics, f_n=f_n, lmbda=lmbda
    )
    LOG.info(f"SNR: {snr}")
    # endregion

    # region plots
    L_target = utillib.LUT(radiance_LUT_path)
    fig = plotlib.line(x=lmbda, y=L_target(lmbda))
    fig = plotlib.line(x=lmbda, y=snr)
    fig = plotlib.line(x=lmbda, y=signal)
    fig = plotlib.line(x=lmbda, y=noise)
    # endregion

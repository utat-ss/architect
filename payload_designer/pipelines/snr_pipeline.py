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

filename = Path(__file__).stem
output_path = Path(f"output/{filename}")
log_path = Path(f"logs/{filename}")

# region logging config
log_path.mkdir(parents=True, exist_ok=True)
logging.config.fileConfig(fname="log.conf", defaults={"path": log_path})
LOG = logging.getLogger(__name__)
# endregion

# region parameter config
L = np.linspace(start=1600, stop=1700, num=100)  # wavelengths [nm]

# LUTS
foreoptic_LUT_path = Path("data/foreoptic_lut.csv")
collimator_LUT_path = Path("data/collimator_lut.csv")
filter_LUT_path = Path("data/filter_lut.csv")
focuser_LUT_path = Path("data/focuser_lut.csv")
sensor_LUT_path = Path("data/sensor_qe_lut.csv")
# endregion

if __name__ == "__main__":

    # region component instantiation
    foreoptic = components.Foreoptic(T=foreoptic_LUT_path)
    slit = components.Slit()
    collimator = components.AchromDoublet(T=collimator_LUT_path)
    bandfilter = components.Filter(T=filter_LUT_path)
    diffractor = components.VPHGrism()
    focuser = components.AchromDoublet(T=focuser_LUT_path)
    sensor = components.Sensor(qe=sensor_LUT_path)
    # endregion

    # region pipeline
    T_sys = (
        foreoptic.T(L) * collimator.T(L) * filter.T(L) * diffractor.T(L) * focuser.T(L)
    )

    snr = sensor.get_snr(T_sys=T_sys)
    # endregion

    fig = plotlib.line(x=L, y=snr)

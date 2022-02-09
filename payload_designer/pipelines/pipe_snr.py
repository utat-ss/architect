"""Compute SNR as function of wavelength."""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np
import pandas as pd

# project
from payload_designer.components import (
    diffractors,
    filters,
    foreoptics,
    lenses,
    sensors,
)
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
lmbda = np.linspace(start=900, stop=1700, num=100)  # [nm]
f_n = 1.5

# LUTS
foreoptic_eta = utillib.LUT(Path("data/foreoptic_transmittance.csv"))
collimator_eta = utillib.LUT(Path("data/collimator_transmittance.csv"))
bandfilter_eta = utillib.LUT(Path("data/filter_transmittance.csv"))
diffractor_eta = utillib.LUT(Path("data/vphgrism_transmittance.csv"))
focuser_eta = utillib.LUT(Path("data/focuser_transmittance.csv"))
sensor_eta = utillib.LUT(Path("data/sensor_quantum_efficiency.csv"))

L_target = utillib.LUT(
    path=Path("data/atmos_radiance_max.csv"), scale=(1e9, 1e-9)
)  # (m, W/sr/m2/m) to (nm, W/sr/m2/nm)
# endregion

if __name__ == "__main__":
    # region component instantiation
    foreoptic = foreoptics.Foreoptic(eta=foreoptic_eta)
    collimator = lenses.AchromLens(eta=collimator_eta)
    bandfilter = filters.Filter(eta=bandfilter_eta)
    diffractor = diffractors.VPHGrism(eta=diffractor_eta)
    focuser = lenses.AchromLens(eta=focuser_eta)
    sensor = sensors.TauSWIR()
    # endregion

    # region pipeline
    LOG.debug(f"L_target:\n{L_target(lmbda)}")

    eta_optics = (
        foreoptic.eta(lmbda)
        * collimator.eta(lmbda)
        * bandfilter.eta(lmbda)
        * diffractor.eta(lmbda)
        * focuser.eta(lmbda)
    )
    LOG.info(f"Optical transmittance: {eta_optics}%")

    snr, signal, noise = sensor.get_snr(
        L_target=L_target, eta_optics=eta_optics, f_n=f_n, lmbda=lmbda
    )
    LOG.info(f"SNR: {snr}")
    # endregion

    # region plots
    dfd = {"$\lambda$": lmbda.flatten(), "SNR": snr.flatten()}
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.line(df=df, x="$\lambda$", y="SNR")
    # endregion

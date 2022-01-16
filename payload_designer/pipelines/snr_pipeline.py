"""Compute SNR as function of wavelength."""

# stdlib
import logging
from datetime import datetime
from pathlib import Path

# external
import numpy as np

# project
from payload_designer import components
from payload_designer.libs import plotlib

filename = Path(__file__).stem
output_path = Path(f"output/{filename}")
log_path = Path(f"logs/{filename}")

# region logging config
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

log_path.mkdir(parents=True, exist_ok=True)
log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
log_file_path = log_path / f"{log_timestamp}.log"

# formatter
LogFormatter = logging.Formatter(
    "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"  # [%(threadName)-12.12s]
)

# file handler
LogFileHandler = logging.FileHandler(log_file_path)
LogFileHandler.setFormatter(LogFormatter)
LogFileHandler.setLevel(logging.DEBUG)
LOG.addHandler(LogFileHandler)

# cli handler
LogCLIHandler = logging.StreamHandler()
LogCLIHandler.setFormatter(LogFormatter)
LogCLIHandler.setLevel(logging.INFO)
LOG.addHandler(LogCLIHandler)
# endregion


if __name__ == "__main__":

    # region parameters
    l = np.linspace(start=900, stop=1700, num=100)  # wavelengths in nm

    # endregion

    # #region component instantiation
    # sensor = components.Sensor()
    # #endregion

    # #region pipeline
    # snr = sensor.get_snr()
    # #endregion

    # fig = plotlib.line(x=l, y=snr)

    # print(f"Net transmittance: {transmittance_net}")

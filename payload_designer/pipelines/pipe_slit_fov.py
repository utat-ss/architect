"""Calculate field of view from slit size."""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np

# project
from payload_designer.components import slits
from payload_designer.libs import plotlib

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
widths = np.linspace(start=900, stop=1700, num=1000)
# endregion

if __name__ == "__main__":
    # region component instantiation
    slit = slits.Slit()
    # endregion

    # region pipeline
    FOV_x = slit.get_horizontal_field_of_view()
    FOV_y = slit.get_vertical_field_of_view()
    # endregion

    # region plots

    # endregion

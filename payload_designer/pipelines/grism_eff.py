"""Calculate grism efficiency for VPH grism from a_in, fringe frequency, 
wavelength, DCG thickness"""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np

# project
from payload_designer.components import diffractors
from payload_designer.libs import plotlib

# region path config
filename = Path(__file__).stem
output_path = Path(f"output/{filename}")
log_path = Path(f"logs/{filename}")
# endregion

# region logging config
log_path.mkdir(parents=True, exist_ok=True)
logging.config.fileConfig(
    fname="log.conf", defaults={"path": log_path}, disable_existing_loggers=False
)
LOG = logging.getLogger(__name__)
# endregion

# region parameter config
lmbda = np.linspace(start=1500, stop=1700, num=10)  # [nm]
v = np.linspace(start=300, stop=1200, num=200)  # [L/mm]
a_in = np.linspace(start=0, stop=20, num=20)
d = np.linspace(start=0.5, stop=4, num=20)
n_g = 0.1
n_3 = 1.3
n_2 = 1.52
n_1 = 1.0
a = 90
eff_mat = 0.85
# endregion

if __name__ == "__main__":
    # region component instantiation
    diffractor = diffractors.VPHGrism(
        m=1,
        l=lmbda,
        v=v,
        a_in=a_in,
        eff_mat=eff_mat,
        a=a,
        d=d,
        n_g=n_g,
        n_3=n_3,
        n_2=n_2,
        n_1=n_1,
    )
    # endregion

    # region pipeline
    eff = diffractor.get_diffraction_efficiency()
    # endregion

    # region plots
    plotlib.line(x=lmbda, y=eff)
    plotlib.line(x=v, y=eff)
    plotlib.line(x=a_in, y=eff)
    plotlib.line(x=d, y=eff)
    # endregion

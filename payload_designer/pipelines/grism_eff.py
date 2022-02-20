"""Calculate grism efficiency for VPH grism from a_in, fringe frequency, 
wavelength, DCG thickness"""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np
import pandas as pd

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
l = np.linspace(start=1500, stop=1700, num=10)  # [nm]
v = np.linspace(start=900, stop=1200, num=200)  # [L/mm]
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
        l=l,
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
    dfd = {"a_in [°]": a_in.flatten(), "d [μm]": d.flatten(), "l [nm]": l.flatten(), "v [lines/mm]": v.flatten(), "a [°]": a.flatten(), 
    "eff_mat []": eff_mat.flatten(), "n_g []": n_g.flatten(),"n_1 []": n_1.flatten(), "n_2 []": n_2.flatten(), "n_3 []": n_3.flatten(), "eff []": eff.flatten()}
    df = pd.DataFrame(data=dfd)
    LOG.debug(df)

    plotlib.line(
        df=df,
        x="a_in [°]",
        y="eff []",
        title="Grism Efficiency vs Incident Ray Angle",
    )
    plotlib.line(
        df=df,
        x="v [lines/mm]",
        y="eff []",
        title="Grism Efficiency vs Fringe Frequency",
    )
    plotlib.line(
        df=df,
        x="f [mm]",
        y="angle [°]",
        title="Grism Efficiency vs Wavelength",
    )
    plotlib.line(
        df=df,
        x="d [μm]",
        y="eff []",
        title="Grism Efficiency vs DCG Thickness",
    )

    # endregion

"""Calculate GSD and Swath."""

# stdlib
import logging
import logging.config
from pathlib import Path

# external
import numpy as np

# project
#from payload_designer.components import sensors
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
# GSD and Swath
flight_h = np.linspace(start=160, stop=2000, num=100) # [km]
pix_pitch = 15 # [um] replace with actual value
foc_len = np.linspace(start=1, stop=100, num=100) # [mm]
skew_a = -20 # [deg] skew angle from nadir; replace with actual value
wavelength = 800 # [nm] replace with actual value
aperture_d = 10 # [mm] replace with actual value

# GSD as function of skew angle only
theta = np.linspace(start=-70, stop=70, num=100) # [deg]
R_E = 6.371*10^6 # [m] radius of Earth
r_orb = R_E + np.multiply(flight_h, 10^3) # [m] radius of orbit

# Swath only
pix_across = 2000 # replace with actual sensor pixel count in across-track direction
pix_along = 1800 # replace with actual sensor pixel count in along-track direction
sens_hor = np.multiply(pix_across, pix_pitch) # [um] horizontal sensor size
sens_ver = np.multiply(pix_along, pix_pitch) # [um] vertical sensor size
# endregion

# region unit conversions
H = np.multiply(flight_h, 10^3) # [m]
s_mu = np.multiply(pix_pitch, 10^(-6)) # [m]
f = np.multiply(foc_len, 10^(-3)) # [m]
a = np.divide(np.multiply(np.pi, skew_a), 180) # [rad]
l = np.multiply(wavelength, 10^(-9)) # [m]
d = np.multiply(aperture_d, 10^(-3)) # [m]
s_x = np.multiply(sens_hor, 10^(-6)) # [m]
s_y = np.multiply(sens_ver, 10^(-6)) # [m]
#endregion

if __name__ == "__main__":
    # region component instantiation
    #sensor = sensors.Sensor(px_x = px_x)
    # endregion

    # region pipeline
    x_sen = np.divide(np.multiply(H, s_mu), np.multiply(f, np.cos(a))) # sensor-limited GSD, flat Earth
    x_opt = np.multiply(1.22, np.divide(np.multiply(l, H), np.multiply(d, np.cos(a)))) # diffraction-limited GSD, flat Earth
    x_abs = max(x_sen, x_opt) # actual system GSD, flat Earth

    S_wid = np.multiply(np.divide(np.multiply(H, s_x), np.multiply(f, np.cos(a))), 10^(-3)) # swath width
    S_len = np.multiply(np.divide(np.multiply(H, s_y), np.multiply(f, np.cos(a))), 10^(-3)) # swath length
    
    term1a = np.multiply(np.multiply(2, r_orb), np.cot(theta))
    term1b = np.multiply(np.multiply(-2, r_orb), np.power(np.cot(theta), 2))
    sqrt1 = np.multiply(np.multiply(4, np.power(R_E, 2)), np.power(np.cot(theta), 2))
    sqrt2 = np.multiply(4, np.power(r_orb, 2))
    sqrt3 = np.multiply(4, np.power(R_E, 2))
    term2a = np.power(np.add(np.add(sqrt1, sqrt2), sqrt3), 2)
    term2b = np.multiply(np.cot(theta), np.power(np.add(np.add(sqrt1, sqrt2), sqrt3), 2))
    term3 = np.multiply(2, np.power(np.cot(theta), 2))
    exp1a = np.power(np.divide(np.add(term1a, term2a), term3), 2)
    exp2a = np.power(np.divide(np.subtract(term1b, term2b), term3), 2)
    exp1b = np.power(np.divide(np.subtract(term1a, term2a), term3), 2)
    exp2b = np.power(np.divide(np.add(term1b, term2b), term3), 2)
    D1 = np.power(np.add(exp1a, exp2a), 0.5)
    D2 = np.power(np.add(exp1b, exp2b), 0.5)
    y = np.divide(np.multiply(min(D1, D2), s_mu), f) # GSD as function of skew angle
    # endregion

    # region plots
    # GSD - flat earth
    plotlib.line(x=f, y=x_sen)
    plotlib.line(x=f, y=x_opt)
    plotlib.line(x=f, y=x_abs)

    # GSD - considering Earth curvature
    plotlib.line(x=theta, y=y)

    # Swath
    plotlib.line(x=f, y=S_wid)
    plotlib.line(x=f, y=S_len)
    # endregion
"""Component classes."""

# stdlib
import logging

# external
import numpy as np
import scipy.constants as sc

# project
from payload_designer.libs import physlib, utillib

LOG = logging.getLogger(__name__)


class VPHGrism:
    """Volume-Phase Holographic grating grism component.

    Args:
        d (float, optional): DCG thickness. Defaults to None.
        t (float, optional): transmision ratio. Defaults to None.
        a_in (float, optional): incident ray angle in degrees. Defaults to None.
        a_out (float, optional): outgoing ray angle in degrees. Defaults to None.
        R (float, optional): resolvance. Defaults to None.
        l (array_like[float], optional): wavelength in nm. Defaults to None.
        l_g (float, optional): undeviated wavelength in nm. Defaults to None.
        a (float, optional): apex angle. Defaults to None.
        m (int, optional): diffraction order. Defaults to None.
        n_1 (float, optional): external index of refraction. Defaults to None.
        n_2 (float, optional): prism index of refraction. Defaults to None.
        n_3 (float, optional): grating substrate index of refraction.
            Defaults to None.
        v (float, optional): fringe frequency. Defaults to None.
        dl (float, optional): spectral resolution. Defaults to None.
        N (float, optional): Number of illumated fringes. Defaults to None.
    """

    def __init__(
        self,
        d=None,
        t=None,
        a_in=None,
        a_out=None,
        R=None,
        l=None,
        l_g=None,
        a=None,
        m=None,
        n_1=None,
        n_2=None,
        n_3=None,
        v=None,
        dl=None,
        N=None,
    ):
        self.d = d
        self.t = t
        self.a_in = a_in
        self.a_out = a_out
        self.R = R
        self.l = l
        self.l_g = l_g
        self.a = a
        self.m = m
        self.n_1 = n_1
        self.n_2 = n_2
        self.n_3 = n_3
        self.v = v
        self.dl = dl
        self.N = N

    def get_angle_out(self):
        """Calculates the outgoing angle from the grism.

        Returns:
            float: outgoing angle in degrees.
        """
        assert self.a_in is not None, "a_in is not set."
        assert self.n_1 is not None, "n_1 is not set."
        assert self.n_2 is not None, "n_2 is not set."
        assert self.n_3 is not None, "n_3 is not set."
        assert self.m is not None, "m is not set."
        assert self.a is not None, "a is not set."
        assert self.v is not None, "v is not set."
        assert self.l is not None, "l is not set."

        # region vectorization
        a_in = np.array(self.a_in).reshape(-1, 1)
        n_1 = np.array(self.n_1).reshape(-1, 1)
        n_2 = np.array(self.n_2).reshape(-1, 1)
        n_3 = np.array(self.n_3).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        a = np.array(self.a).reshape(-1, 1)
        v = np.array(self.v).reshape(-1, 1)
        l = np.array(self.l).reshape(-1, 1)
        # endregion

        # region unit conversions
        l = l * 10 ** -9  # m to nm
        a_in = np.radians(a_in)  # deg to rad
        a = np.radians(self.a)  # deg to rad
        # endregion

        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=n_1, n_2=n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=n_2, n_2=n_3)
        angle_5 = angle_4
        angle_6 = np.arcsin(np.sin(angle_5) - m * np.matmul(v, np.transpose(l)))
        angle_7 = angle_6
        angle_8 = physlib.snell_angle_2(angle_1=angle_7, n_1=n_3, n_2=n_2)
        angle_9 = angle_8 - a
        angle_10 = physlib.snell_angle_2(angle_1=angle_9, n_1=n_2, n_2=n_1)
        angle_out = angle_10 + a

        angle_out = np.degrees(angle_out)

        return angle_out

    def get_resolvance(self):
        """Caculates the grism resolvance.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolvance.
        """
        if self.l is not None and self.dl is not None:
            R = self.l / self.dl
        elif self.m is not None and self.N is not None:
            R = self.m * self.N
        else:
            raise ValueError("l and dl or m and N must be set.")

        return R

    def get_resolution(self):
        """Caclulates the grism optically-limited spectral resolution.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolution in nm.
        """
        if self.l is not None and self.R is not None:
            dl = self.l / self.R
        elif self.l is not None and self.m is not None and self.N is not None:
            dl = self.l / (self.m * self.N)
        else:
            raise ValueError("l and R or l and m and N must be set.")

        return dl


class ThinFocuser:
    """Thin lens focuser component.

    Args:
        f (float, optional): focal length. Defaults to None.
        h (float, optional): image height above optical axis. Defaults to None.
        a_in (float, optional): incoming ray angle relative to optical axis.
            Defaults to None.
        T (path-like, optional): path to transmittance LUT data. Defaults to None.
    """

    def __init__(self, f=None, h=None, a_in=None, T=None):
        self.f = f
        self.h = h
        self.a_in = a_in
        self.T = utillib.LUT(T)

    def get_image_height(self):
        """Calculate the image height along the focal plane.

        Returns:
            float: image height in m.
        """
        assert self.f is not None, "f is not set."
        assert self.a_in is not None, "a_in is not set."

        # region vectorization
        f = np.array(self.f).reshape(-1, 1)
        a_in = np.array(self.a_in).reshape(-1, 1)
        # endregion

        # region unit conversions
        a_in = np.radians(a_in)  # deg to rad
        # endregion

        h = np.matmul(f, np.transpose(np.tan(a_in)))

        return h


class Sensor:
    """Sensor component model.

    Args:
        px_x (array_like[int], optional): Pixel count in cross-track direction.
            Defaults to None.
        px_y (array_like[int], optional): Pixel count in along-track direction.
            Defaults to None.
        p (array_like[float], optional): Pixel pitch in micrometers.
            Defaults to None.
        t_int (array_like[float], optional): Integration time in seconds.
            Defaults to None.
        d_well (array_like[int], optional): Well depth in electrons/pixel.
            Defaults to None.
        r_dyn (array_like[int], optional): Dynamic range in bits. Defaults to None.
        i_dark (array_like[int], optional): Dark current in electrons/pixel/second.
            Defaults to None.
        n_read (array_like[int], optional): Readout noise in electrons/pixel.
            Defaults to None.
        qe (path-like, optional): path to quantum efficiency LUT. Defaults to None.
    """

    def __init__(
        self,
        dt=None,
        i_dark=None,
        n_bit=None,
        n_read=None,
        n_well=None,
        p=None,
        px_x=None,
        px_y=None,
        qe=None,
    ):
        self.dt = dt
        self.i_dark = i_dark
        self.n_bit = n_bit
        self.n_read = n_read
        self.n_well = n_well
        self.p = p
        self.px_x = px_x
        self.px_y = px_y
        self.qe = utillib.LUT(qe)

    def get_sensor_detector_area(self):
        A_d = self.p * self.p
        return A_d

    def get_sensor_area(self):
        A_s = self.get_sensor_detector_area() * self.px_x * self.px_y
        return A_s

    def get_snr(self, R, T, f_n):
        """Calculates the signal to noise ratio from the sensor and system parameters.

        Args:
            L (path-like): path to atmospheric radiance LUT.
            T (array-like[float]): transmittance of the optical system by wavelength.
            f_n (float): f-number of optical system.

        Returns:
            [type]: [description]
        """

        R = utillib.LUT(R)
        A_d = self.get_sensor_detector_area()
        T

        sc.h
        sc.c

        # region signal
        signal = 1
        # endregion

        # region noise
        noise = np.sqrt()
        # endregion

        snr = signal / noise

        return snr

"""Component classes."""

# stdlib
import logging
import math

# external
import numpy as np

# project
from payload_designer.libs import physlib

LOG = logging.getLogger(__name__)


class VPHGrism:
    """Volume-Phase Holographic grating grism component.

    Args:
        d (float, optional): DCG thickness. Defaults to None.
        t (float, optional): transmision ratio. Defaults to None.
        a_in (float, optional): incident ray angle in degrees. Defaults to None.
        a_out (float, optional): outgoing ray angle in degrees. Defaults to None.
        R (float, optional): resolvance from wavelength and spectral resolution. Defaults to None.
        l (array_like[float], optional): wavelength in nm. Defaults to None.
        l_g (float, optional): undeviated wavelength in nm. Defaults to None.
        a (float, optional): apex angle. Defaults to None.
        m (int, optional): diffraction order. Defaults to None.
        n_1 (float, optional): external index of refraction. Defaults to None.
        n_2 (float, optional): prism index of refraction. Defaults to None.
        n_3 (float, optional): grating substrate index of refraction.
            Defaults to None.
        v (float, optional): fringe frequency. Defaults to None.
        dl (float, optional): spectral resolution in nm. Defaults to None.
        N (float, optional): Number of illumated fringes. Defaults to None.
        w (float, optional): slit width in m. Defaults to None.
        n (float, optional): groove density in lines/m. Defaults to None.
        n_g (float, optional): index modulation contrast. Defaults to None.
        n_p (float, optional): diffraction efficiency. Defaults to None.
        eff_mat (float, optional): efficiency of prism material. Defaults to None.
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
        w=None,
        n=None,
        n_p=None,
        eff_mat=None,
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
        self.n = n
        self.w = w
        self.n_p = n_p
        self.eff_mat = eff_mat

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

    ###def get_undeviated_wavelength():
        """Calculates the grism undeviated wavelength.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: undeviated wavelength.
        """
    def get_resolvance(self):
        """Calculates the grism resolvance.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolvance.
        """
        # vectorization

        # unit conversions
        l = l * 10 ** -9
        dl = dl * 10 ** -9
        w = w * 10 ** -9

        if self.l is not None and self.dl is not None:
            R = self.l / self.dl
        elif self.m is not None and self.N is not None:
            R = self.m * self.N
        elif self.m is not None and self.n is not None and self.w is not None:
            R = self.m * self.n * self.w
        else:
            raise ValueError("l and dl or m and N or m and n and w must be set.")
        return R

    def get_resolution(self):
        """Calculates the grism optically-limited spectral resolution.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolution in nm.
        """

        # vectorization

        # unit conversion
        l = l * 10 ** -9
        w = w * 10 ** -6

        if self.l is not None and self.R is not None:
            dl = self.l / self.R
        elif self.l is not None and self.m is not None and self.N is not None:
            dl = self.l / (self.m * self.N)
        elif (
            self.l is not None
            and self.m is not None
            and self.n is not None
            and self.w is not None
        ):
            dl = self.l / (self.m * self.n * self.w)
        else:
            raise ValueError(
                "l and R or l and m and N or l and m and n and w must be set."
            )

        return dl

    def get_diffraction_efficiency(self):
        """Calculates the grism diffraction_efficiency.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: diffraction efficiency.
        """
        assert self.a_in is not None, "a_in is not set."
        #assert self.a_out is not None, "a_out is not set."
        assert self.d is not None, "d is not set."
        assert self.l is not None, "l is not set."
        assert self.v is not None, "v is not set."
        assert self.n_g is not None, "n_g is not set"
        assert self.eff_mat is not None, "prism material efficiency is not set"


        # vectorization

        # unit conversion
        a_in = np.radians(a_in)
        l = l * 10 ** -9  # nm to m
        # d probably needs one too

        ###get angle_5 and 6 and replace angle_out and angle_in
        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=n_1, n_2=n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=n_2, n_2=n_3)
        angle_5 = angle_4
        angle_6 = np.arcsin(np.sin(angle_5) - m * np.matmul(v, np.transpose(l)))

        # check Q
        L = 1 / v
        Q = (2 * math.pi * l * d) / (n_g * L ** 2)
        if Q < 10:
            raise ValueError(
                "Q requirement not met, diffraction efficiency formula not valid"
            )

        # diffraction efficiency
        eta_s = np.sin((math.pi * n_g * d) / (l * np.cos(angle_5))) ** 2
        n_p = eta_s * np.cos(angle_5 + angle_6)
        
        ##l or l_g?
        ###add consideration for grism material
        n_p = n_p * eff_mat * eff_mat
        return n_p


class ThinFocuser:
    """Thin lens focuser component.

    Args:
        f (float, optional): focal length. Defaults to None.
        h (float, optional): image height above optical axis. Defaults to None.
        a_in (float, optional): incoming ray angle relative to optical axis.
            Defaults to None.
    """

    def __init__(self, f=None, h=None, a_in=None):

        self.f = f
        self.h = h
        self.a_in = a_in

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

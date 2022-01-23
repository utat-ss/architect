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
        d (float, optional): DCG thickness in micrometers. Defaults to None.
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
        v (float, optional): fringe frequency in lines/mm. Defaults to None.
        dl (float, optional): spectral resolution in nm. Defaults to None.
        N (float, optional): Number of illumated fringes. Defaults to None.
        w (float, optional): slit width in mm. Defaults to None.
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
        n_g=None,
        v=None,
        dl=None,
        N=None,
        w=None,
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
        self.n_g = n_g
        self.v = v
        self.dl = dl
        self.N = N
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

    def get_undeviated_wavelength(self):
        """Calculates the grism undeviated wavelength.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: undeviated wavelength.
        """
        assert self.m is not None, "m is not set."
        assert self.v is not None, "v is not set."
        assert self.a is not None, "a is not set."
        assert self.a_in is not None, "a_in is not set."
        assert self.n_1 is not None, "n_1 is not set"
        assert self.n_2 is not None, "n_2 is not set"
        assert self.n_3 is not None, "n_3 is not set"        
        # unit conversions
        a_in = np.radians(self.a_in)  # deg to rad
        a = np.radians(self.a)
        v = self.v * 10 ** -6  # lines/mm to lines/nm

        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=self.n_1, n_2=self.n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=self.n_2, n_2=self.n_3)
        angle_5 = angle_4
        l_g = 2 * (np.sin(angle_5) / (self.m * v))
        return l_g  # in nm

    def get_resolvance(self):
        """Calculates the grism resolvance.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolvance.
        """
        # vectorization

        # unit conversions

        if self.l is not None and self.dl is not None:
            R = (self.l) / (self.dl) #both in nm
        elif self.m is not None and self.N is not None:
            R = self.m * self.N
        elif self.m is not None and self.v is not None and self.w is not None:
            R = self.m * (self.v * (1 / (10 ** -3))) * (self.w*10**-3) #v -> lines/mm to lines/m. w -> mm to m
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
        
        if self.l is not None and self.R is not None:
            dl = (self.l) / self.R #no unit conversion so dl is in nm
        elif self.l is not None and self.m is not None and self.N is not None:
            dl = (self.l) / (self.m * self.N) #no unit conversion so dl is in nm
        elif (
            self.l is not None
            and self.m is not None
            and self.v is not None
            and self.w is not None
        ):
            dl = (self.l) / (self.m * (self.v *10 ** -6) * self.w * 10 ** 6) #### mm to nm
        else:
            raise ValueError(
                "l and R or l and m and N or l and m and n and w must be set."
            )

        return dl #in nm

    def get_diffraction_efficiency(self):
        """Calculates the grism diffraction_efficiency.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: diffraction efficiency.
        """

        assert self.a_in is not None, "a_in is not set."
        assert self.a is not None, "a is not set."
        assert self.d is not None, "d is not set."
        assert self.l is not None, "l is not set."
        assert self.v is not None, "v is not set."
        assert self.n_g is not None, "n_g is not set"
        assert self.n_1 is not None, "n_1 is not set"
        assert self.n_2 is not None, "n_2 is not set"
        assert self.n_3 is not None, "n_3 is not set"
        assert self.eff_mat is not None, "prism material efficiency is not set"

        # vectorization

        # unit conversion
        a_in = np.radians(self.a_in)
        a = np.radians(self.a)
        l = self.l  # nm
        v = self.v * 10 ** -6  # lines/mm to lines/nm
        d = self.d * 10 ** 3  # microns to nm

        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=self.n_1, n_2=self.n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=self.n_2, n_2=self.n_3)
        angle_5 = angle_4
        L = 1 / v  # nm/lines

        Q = (l ** 2) / (self.n_g * self.n_3 * L ** 2)
        if np.any(Q < 10):
            raise ValueError(
                "Q requirement not met, diffraction efficiency formula not valid"
            )
        # diffraction efficiency
        n_p = (np.sin((math.pi * self.n_g * d) / (l * np.cos(angle_5))) ** 2) + (
            (1 / 2)
            * (
                np.sin(
                    ((math.pi * self.n_g * d) * np.cos(2 * angle_5)) / (l * np.cos(angle_5))
                )
            )
            ** 2
        )  # angle_5 being close to bragg angle = more efficiency
        n_p = n_p * self.eff_mat * self.eff_mat
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

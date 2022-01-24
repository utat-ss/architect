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
        a_in = np.expand_dims(self.a_in, axis=1)
        n_1 = np.expand_dims(self.n_1, axis=1)
        n_2 = np.expand_dims(self.n_2, axis=1)
        n_3 = np.expand_dims(self.n_3, axis=1)
        m = np.expand_dims(self.m, axis=1)
        a = np.expand_dims(self.a, axis=1)
        v = np.expand_dims(self.v, axis=1)
        l = np.expand_dims(self.l, axis=1)
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
        angle_6 = np.arcsin(math.sin(angle_5) - m * np.matmul(v, np.transpose(l)))
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
        f = np.expand_dims(self.f, axis=1)
        a_in = np.expand_dims(self.a_in, axis=1)
        # endregion

        # region unit conversions
        a_in = np.radians(a_in)  # deg to rad
        # endregion

        h = np.matmul(f, np.transpose(np.tan(a_in)))

        return h


class VPHGrating:
    """Volume-Phase Holographic grating component.

    Args:
        a_0 (float, optional): incident ray angle in degrees. Defaults to None.
        n_0 (float, optional): external index of refraction. Defaults to None.
        n_1 (float, optional): glass substrate index of refraction. Defaults to None.
        n_2 (float, optional): DCG layer index of refraction.
        Lmda (float, optional): separation between the fringes of the DCG layer. Defaults to None.
        phi (float, optional): slant angle between the grating normal and the plane of the fringes
        lmda (float, optional): wavelength of incident light. Defaults to None.
        m (integer, optional): diffraction order. Defaults to None.
        delta_n2 (float, optional): semiamplitude of the refractive-index modulation. Defaults to None.
        d (float, optional): grating thickness. Defaults to None.

    """

    def __init__(
        self,
        a_0=None,
        n_0=None,
        n_1=None,
        n_2=None,
        Lmda=None,
        lmda=None,
        m=None,
        delta_n2=None,
        d=None,
        phi=None
    ):

        self.a_0 = a_0
        self.n_0 = n_0
        self.n_1 = n_1
        self.n_2 = n_2
        self.Lmda = Lmda
        self.lmda = lmda
        self.m = m
        self.delta_n2 = delta_n2
        self.d = d
        self.phi = phi

    def get_angle_out(self):

        """Calculates the angle of the diffracted light exiting the diffraction grating.

        Returns:
            float: diffracted angle in radians.
        """
        assert self.a_0  is not None, "a_0 is not set."
        assert self.n_0  is not None, "a_0 is not set."
        assert self.Lmda is not None, "Lmda is not set."
        assert self.lmda is not None, "lmda is not set."
        assert self.m is not None, "m is not set."
        assert self.phi is not None, "phi is not set."

        # region vectorization
        a_0 = np.array(self.a_0).reshape(-1, 1)
        n_0 = np.array(self.n_0).reshape(-1, 1)
        Lmda = np.array(self.Lmda).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        phi = np.array(self.phi).reshape(-1, 1)
        # endregion

        # region unit conversions
        a_0 = np.radians(a_0)  # deg to rad
        Lmda = Lmda * 10 ** (-3) # mm to m
        lmda = lmda * 10 ** (-9) # nm to m
        # endregion

        Lmda_g = Lmda / np.cos(phi)
        b_0 = np.arcsin( (m*lmda)/(n_0*Lmda_g) - np.sin(a_0) )

        return b_0

    def get_Kogelnik_efficiency(self):
        """Calculates the Kogelnik efficiency for unpolarized light.
        
        Returns:
            float: Kogelnik efficiency.
        """
        assert self.delta_n2 is not None, "delta_n2 is not set."
        assert self.n_2 is not None, "a_2 is not set."
        assert self.d is not None, "d is not set."
        assert self.lmda is not None, "lmda is not set."
        assert self.Lmda is not None, "lmda is not set."
        assert self.m is not None, "m is not set."

        # region vectorization
        delta_n2 = np.array(self.m).reshape(-1, 1)
        n_2 = np.array(self.n_2).reshape(-1, 1)
        d = np.array(self.d).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        Lmda = np.array(self.lmda).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        # endregion

        # region unit conversions
        d = d * 10 ** (-3) # mm to m
        lmda = lmda * 10 ** (-9) # nm to m
        Lmda = Lmda * 10 ** (-3) # mm to m
        # endregion
        
        a_2b = np.arcsin((m * lmda)/(2 * n_2 * Lmda))
        mu_s = np.sin((np.pi * delta_n2 * d)/(lmda * np.cos(a_2b)))**2 + 0.5 * np.sin((np.pi * delta_n2 * d * np.cos(2*a_2b))/(lmda * np.cos(a_2b)))**2

        return mu_s

    def get_efficiency_bandwidth(self):
        """Calculates the Kogelnik efficiency for unpolarized light.
        
        Returns:
            float: Kogelnik efficiency.
        """
        assert self.n_2 is not None, "a_2 is not set."
        assert self.d is not None, "d is not set."
        assert self.lmda is not None, "lmda is not set."
        assert self.Lmda is not None, "lmda is not set."
        assert self.m is not None, "m is not set."

        # region vectorization
        n_2 = np.array(self.n_2).reshape(-1, 1)
        d = np.array(self.d).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        Lmda = np.array(self.lmda).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        # endregion

        # region unit conversions
        d = d * 10 ** (-3) # mm to m
        lmda = lmda * 10 ** (-9) # nm to m
        Lmda = Lmda * 10 ** (-3) # mm to m
        # endregion
        
        a_2b = np.arcsin((m * lmda)/(2 * n_2 * Lmda))
        lmda_eff = (Lmda * lmda)/(d * np.tan(a_2b))
        return lmda_eff
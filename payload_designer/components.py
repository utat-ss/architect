"""Component classes."""

# stdlib
from gettext import install
import logging

# external
import numpy as np

# project
from payload_designer.libs import physlib

LOG = logging.getLogger(__name__)

class Foreoptics:
    """Foreoptics component.

    Args:
        ds_i (float, optional): image distance. Defaults to None.
        ds_o (float, optional): object distance. Defaults to None.
        n (float, optional): f-number. Defaults to None.
        dm_a (float, optional): aperture diameter. Defaults to None.
        a_in_max (float, optional): maximum angle of incidence. Defaults to None.
        na (float, optional): numerical aperture. Defaults to None.
        b (float, optional): source radiance. Defaults to None.
        g (float, optional): geometric etendue. Defaults to None.
        s (float, optional): area of emitting source. Defaults to None.

    """

    def __init__(
        self,
        ds_i=None,
        ds_o=None,
        n=None,
        dm_a=None,
        a_in_max=None,
        na=None,
        b=None,
        g=None,
        s=None
    ):
        self.ds_i = ds_i
        self.ds_o = ds_o
        self.n = n
        self.dm_a = dm_a
        self.a_in_max = a_in_max
        self.na = na
        self.b = b
        self.g = g
        self.s = s

    def get_aperture_diamter(self):
        """Calculate the aperture diamter.

        Returns:
            float: aperture diameter (length).
        """
        assert self.ds_i is not None, "ds_i is not set."

        if self.n is not None:
            dm_a = np.divide(self.ds_i, self.n)
        elif self.na is not None:
            dm_a = 2*np.multiply(self.ds_i, self.na)
        else:
            raise ValueError("n or na must be set.")

        return dm_a

    def get_magnification(self):
        """Calculate the magnification of the foreoptics.

        Returns:
            float: magnification (unitless).
        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        m = np.divide(self.ds_i,self.ds_o)

        return m
    
    def get_f_number(self):
        """Calculate the f number (f/#).

        Returns:
            float: f/# (unitless).
        """
        if self.na is not None:
            n = np.divide(1, 2*self.na)
        elif self.ds_i is not None and self.dm_a is not None:
            n = np.divide(self.ds_i, self.dm_a)
        else:
            raise ValueError("ds_i and dm_a or na must be set.")

        return n
    
    def get_effective_focal_length(self):
        """Calculate the effective focal length.

        Returns:
            float: effective focal length (length).
        """
        assert self.ds_i is not None, "ds_i is not set."
        assert self.ds_o is not None, "ds_o is not set."

        efl = np.divide(self.ds_o + self.ds_i, np.multiply(self.ds_o, self.ds_i))

        return efl
    
    def get_numerical_aperture(self):
        """Calculate the numerical aperture.

        Returns:
            float: numerical aperture (unitless).
        """
        assert self.a_in_max is not None, "a_in_max is not set."

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion

        na = np.sin(a_in_max)

        return na
    
    def get_geometric_etendue(self):
        """Calculate the geometric etendue.

        Returns:
            float: geometric etendue (length^2).
        """
        assert self.s is not None, "s is not set."
        assert self.a_in_max is not None, "a_in_max is not set."

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion

        g = np.multiply(np.pi, self.s, np.power(np.sin(a_in_max), 2))

        return g
    
    def get_radiant_flux(self):
        """Calculate the flux.

        Returns:
            float: flux (watt).
        """
        assert self.b is not None, "b is not set."
        assert self.g is not None, "g is not set."

        f = np.multiply(self.b, self.g)

        return f


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

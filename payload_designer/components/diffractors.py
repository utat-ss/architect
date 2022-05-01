"""Diffractor classes."""

# stdlib
import logging
import math

# external
import numpy as np
import pandas as pd
import scipy.constants as sc

# project
from payload_designer.components.basecomponent import BaseComponent
from payload_designer.libs import physlib, utillib

LOG = logging.getLogger(__name__)


class SRGrating(BaseComponent):
    """Surface-Relief Diffraction Grating component.

    Args:
        alpha (float, optional): incident angle of light. Defaults to None.
        beta (float, optional): diffraction angle. Defaults to None.
        G (float, optional): groove density. Defaults to None.
        lmda (float, optional): wavelength of incident light. Defaults to None.
        m (integer, optional): diffraction order. Defaults to None.
        W (float, optional): ruled width of grating. Defaults to None.
        R (float, optional): resolving power. Defaults to None.
        mass (float, optional): mass of component [g]. Defaults to None.
        V (tuple[float, float, float], optional): Volume envelope in x,y,z [mm]. Defaults to None.

    """

    def __init__(
        self,
        alpha=None,
        beta=None,
        G=None,
        lmda=None,
        m=None,
        W=None,
        R=None,
        mass=None,
        V=None,
    ):
        self.alpha = alpha
        self.beta = beta
        self.G = G
        self.lmda = lmda
        self.m = m
        self.W = W
        self.R = R
        self.mass = mass
        self.V = V

    def get_angle_out(self):
        """Calculates the angle of the diffracted light exiting the diffraction
        grating.

        Returns:
            float: diffracted angle in radians.

        """
        assert self.alpha is not None, "alpha is not set."
        assert self.G is not None, "G is not set."
        assert self.lmda is not None, "lmda is not set."
        assert self.m is not None, "m is not set."

        # region vectorization
        alpha = np.array(self.alpha).reshape(-1, 1)
        G = np.array(self.G).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        m = np.array(self.m).reshape(-1, 1)
        # endregion

        # region unit conversions
        G = G * 10 ** 3  # 1/mm to 1/m
        lmda = lmda * 10 ** (-9)  # nm to m
        alpha = np.radians(alpha)  # deg to rad
        # endregion

        beta = np.arcsin(G * m * lmda - np.sin(alpha))

        return beta

    def get_angular_dispersion(self):
        """Calculates the angular dispersion of a grating.

        Returns:
            float: angular dispersion in rad/nm.

        """
        assert self.alpha is not None, "alpha is not set."
        assert self.beta is not None, "beta is not set."
        assert self.lmda is not None, "lmda is not set."

        # region vectorization
        alpha = np.array(self.alpha).reshape(-1, 1)
        beta = np.array(self.beta).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        # endregion

        # region unit conversions
        alpha = np.radians(alpha)  # deg to rad
        lmda = lmda * 10 ** (-9)  # nm to m
        # endregion

        D = (np.sin(alpha) + np.sin(beta)) / (lmda * np.cos(beta))

        return D

    def get_resolving_power(self):
        """Calculates the resolving power of the diffraction grating.

        Returns:
            float: resolving power in radians.

        """
        assert self.alpha is not None, "alpha is not set."
        assert self.beta is not None, "beta is not set."
        assert self.lmda is not None, "lmda is not set."
        assert self.W is not None, "W is not set."

        # region vectorization
        alpha = np.array(self.alpha).reshape(-1, 1)
        beta = np.array(self.beta).reshape(-1, 1)
        lmda = np.array(self.lmda).reshape(-1, 1)
        W = np.array(self.W).reshape(-1, 1)
        # endregion

        # region unit conversions
        alpha = np.radians(alpha)  # deg to rad
        beta = np.radians(beta)  # deg to rad
        lmda = lmda * 10 ** (-9)  # nm to m
        W = W * 10 ** (-9)  # nm to m
        # endregion

        R = W * (np.sin(alpha) + np.sin(beta)) / lmda

        return R

    def get_anamorphic_amplification(self):
        """Calculates the anamorphic amplification.

        Returns:
            unitless

        """
        assert self.alpha is not None, "alpha is not set."
        assert self.beta is not None, "beta is not set."

        # region vectorization
        alpha = np.array(self.alpha).reshape(-1, 1)
        beta = np.array(self.beta).reshape(-1, 1)
        # endregion

        # region unit conversions
        alpha = np.radians(alpha)  # deg to rad
        # endregion

        b_to_a = np.cos(beta) / np.cos(alpha)

        return b_to_a


class VPHGrating(BaseComponent):
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
        mass (float, optional): mass of component [g]. Defaults to None.
        V (tuple[float, float, float], optional): Volume envelope in x,y,z [mm]. Defaults to None.

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
        phi=None,
        mass=None,
        V=None,
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
        self.mass = mass
        self.V = V

    def get_angle_out(self):

        """Calculates the angle of the diffracted light exiting the diffraction
        grating.

        Returns:
            float: diffracted angle in radians.

        """
        assert self.a_0 is not None, "a_0 is not set."
        assert self.n_0 is not None, "a_0 is not set."
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
        Lmda = Lmda * 10 ** (-3)  # mm to m
        lmda = lmda * 10 ** (-9)  # nm to m
        # endregion

        Lmda_g = Lmda / np.cos(phi)
        b_0 = np.arcsin((m * lmda) / (n_0 * Lmda_g) - np.sin(a_0))

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
        d = d * 10 ** (-3)  # mm to m
        lmda = lmda * 10 ** (-9)  # nm to m
        Lmda = Lmda * 10 ** (-3)  # mm to m
        # endregion

        a_2b = np.arcsin((m * lmda) / (2 * n_2 * Lmda))
        mu_s = (
            np.sin((np.pi * delta_n2 * d) / (lmda * np.cos(a_2b))) ** 2
            + 0.5
            * np.sin((np.pi * delta_n2 * d * np.cos(2 * a_2b)) / (lmda * np.cos(a_2b)))
            ** 2
        )

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
        d = d * 10 ** (-3)  # mm to m
        lmda = lmda * 10 ** (-9)  # nm to m
        Lmda = Lmda * 10 ** (-3)  # mm to m
        # endregion

        a_2b = np.arcsin((m * lmda) / (2 * n_2 * Lmda))
        lmda_eff = (Lmda * lmda) / (d * np.tan(a_2b))
        return lmda_eff


class VPHGrism(BaseComponent):
    """Volume-Phase Holographic grating grism component.

    Args:
        N (float, optional): Number of illumated fringes. Defaults to None.
        R (float, optional): resolvance from wavelength and spectral resolution. Defaults to None.
        a (float, optional): apex angle. Defaults to None.
        a_in (float, optional): incident ray angle in degrees. Defaults to None.
        a_out (float, optional): outgoing ray angle in degrees. Defaults to None.
        d (float, optional): DCG thickness in micrometers. Defaults to None.
        dl (float, optional): spectral resolution in nm. Defaults to None.
        eff_mat (float, optional): efficiency of prism material. Defaults to None.
        eta (LUT, optional) transmittace LUT object. Defaults to None.
        l (array_like[float], optional): wavelength in nm. Defaults to None.
        l_g (float, optional): undeviated wavelength in nm. Defaults to None.
        m (int, optional): diffraction order. Defaults to None.
        n_1 (float, optional): external index of refraction. Defaults to None.
        n_2 (float, optional): prism index of refraction. Defaults to None.
        n_3 (float, optional): grating substrate index of refraction. Defaults to None.
        n_g (float, optional): index modulation contrast. Defaults to None.
        n_p (float, optional): diffraction efficiency. Defaults to None.
        t (float, optional): transmision ratio. Defaults to None.
        v (float, optional): fringe frequency in lines/mm. Defaults to None.
        w (float, optional): slit width in mm. Defaults to None.
        mass (float, optional): mass of component [g]. Defaults to None.
        V (tuple[float, float, float], optional): Volume envelope in x,y,z [mm]. Defaults to None.

    """

    def __init__(
        self,
        N=None,
        R=None,
        a=None,
        a_in=None,
        a_out=None,
        d=None,
        dl=None,
        eff_mat=None,
        eta=None,
        l=None,
        l_g=None,
        m=None,
        n_1=None,
        n_2=None,
        n_3=None,
        n_g=None,
        n_p=None,
        t=None,
        v=None,
        w=None,
        mass=None,
        V=None,
    ):
        self.N = N
        self.R = R
        self.a = a
        self.a_in = a_in
        self.a_out = a_out
        self.d = d
        self.dl = dl
        self.eff_mat = eff_mat
        self.eta = eta
        self.l = l
        self.l_g = l_g
        self.m = m
        self.n_1 = n_1
        self.n_2 = n_2
        self.n_3 = n_3
        self.n_g = n_g
        self.n_p = n_p
        self.t = t
        self.v = v
        self.w = w
        self.mass = mass
        self.V = V

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
            R = (self.l) / (self.dl)  # both in nm
        elif self.m is not None and self.N is not None:
            R = self.m * self.N
        elif self.m is not None and self.v is not None and self.w is not None:
            R = (
                self.m * (self.v * (1 / (10 ** -3))) * (self.w * 10 ** -3)
            )  # v -> lines/mm to lines/m. w -> mm to m
        else:
            raise ValueError("l and dl or m and N or m and n and w must be set.")
        return R

    def get_resolution(self):
        """Calculates the grism optically-limited spectral resolution.

        Raises:
            ValueError: if required parameters are not set.

        Returns:
            float: resolution [nm].

        """

        # region unit conversion

        # endregion

        if self.l is not None and self.R is not None:
            dl = (self.l) / self.R  # no unit conversion so dl is in nm
        elif self.l is not None and self.m is not None and self.N is not None:
            dl = (self.l) / (self.m * self.N)  # no unit conversion so dl is in nm
        elif (
            self.l is not None
            and self.m is not None
            and self.v is not None
            and self.w is not None
        ):

            # region unit conversion
            lmbda = self.l * 1e-9  # [nm] to [m]
            v = self.v * 1e3  # [L/mm] to [L/m]
            w = self.w * 1e-3  # [mm] to [m]
            # endregion

            # region vectorization
            lmbda = np.array(lmbda).reshape(-1, 1, 1)
            v = np.array(v).reshape(1, -1, 1)
            w = np.array(w).reshape(1, 1, -1)

            shape = (lmbda.size, v.size, w.size)

            lmbda = np.broadcast_to(array=lmbda, shape=shape)
            v = np.broadcast_to(array=v, shape=shape)
            w = np.broadcast_to(array=w, shape=shape)
            # endregion

            dl = lmbda / (self.m * v * w)
            dl = np.squeeze(dl)
            print(f"dl: {dl.shape}")

            # region units reconversion
            dl = dl * 1e9  # [m] to [nm]
            # endregion
        else:
            raise ValueError(
                "l and R or l and m and N or l and m and n and w must be set."
            )

        return dl  # in nm

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

        # region unit conversion
        a = np.radians(self.a)
        a_in = np.radians(self.a_in)
        d = self.d * 1e-6  # microns to m
        eff_mat = self.eff_mat
        l = self.l * 1e-9  # nm to m
        n_1 = self.n_1
        n_2 = self.n_2
        n_3 = self.n_3
        n_g = self.n_g
        v = self.v * 1e3  # lines/mm to lines/m
        # endregion

        # region evaluation
        angle_1 = a_in + a
        angle_2 = physlib.snell_angle_2(angle_1=angle_1, n_1=n_1, n_2=n_2)
        angle_3 = a - angle_2
        angle_4 = physlib.snell_angle_2(angle_1=angle_3, n_1=n_2, n_2=n_3)
        angle_5 = angle_4
        L = 1 / v  # nm/lines

        # diffraction efficiency
        n_p = (np.sin((math.pi * n_g * d) / (l * np.cos(angle_5))) ** 2) + (
            (1 / 2)
            * (
                np.sin(
                    ((math.pi * n_g * d) * np.cos(2 * angle_5)) / (l * np.cos(angle_5))
                )
            )
            ** 2
        )  # angle_5 being close to bragg angle = more efficiency
        n_p = n_p * eff_mat * eff_mat
        # endregion

        # region unit reconversion
        l = l * 1e9  # m to nm
        v = v * 1e-3  # lines/m to lines/mm
        d = d * 1e6  # m to microns
        a_in = np.degrees(a_in)
        a = np.degrees(a)
        # endregion
        #dictionary region
        
        dfd = {"a_in [°]": a_in.flatten(), "d [um]": d.flatten(), "l [nm]": l.flatten(), "v [lines/mm]": v.flatten(), "a [°]": a.flatten(),  "n_1": n_1.flatten(), "n_2": n_2.flatten(), "n_3": n_3.flatten(), "eff_mat": eff_mat.flatten(),"eff": n_p.flatten()}
        df = pd.DataFrame(data=dfd)
        LOG.debug(f"dataframe:\n{df.to_string()}")

        return n_p

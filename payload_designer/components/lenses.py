"""Lens classes."""

# stdlib
import logging
import math

# external
import numpy as np
import scipy.constants as sc

# project
from payload_designer.libs import physlib, utillib

LOG = logging.getLogger(__name__)


class ThinLens:
    """Thin singlet lens component.

    Args:
        D (float, optional): diameter of the lens [mm]. Defaults to None.
        M (float, optional): mass of lens [g]. Defaults to None.
        eta (LUT, optional) transmittace LUT object. Defaults to None.
        a_in (array_like[float], optional): incoming ray angle relative to optical axis [°]. Defaults to None.
        a_out (array_like[float], optional): outgoing ray angle relative to optical axis [°]. Defaults to None.
        d_i (array_like[float], optional): distance to image plane [mm]. Defaults to None.
        d_o (array_like[float], optional): distance from object plane [mm]. Defaults to None.
        f (array_like[float], optional): focal length [mm]. Defaults to None.
        h_i (array_like[float], optional): image height above optical axis [mm]. Defaults to None.
        h_o (array_like[float], optional): source height above optical axis [mm]. Defaults to None.

    """

    def __init__(
        self,
        D=None,
        M=None,
        eta=None,
        a_in=None,
        a_out=None,
        d_i=None,
        d_o=None,
        f=None,
        h_i=None,
        h_o=None,
    ):
        self.D = D
        self.M = M
        self.eta = eta
        self.a_in = a_in
        self.a_out = a_out
        self.d_i = d_i
        self.d_o = d_o
        self.f = f
        self.h_i = h_i
        self.h_o = h_o

    def get_image_distance(self):
        """Calculate image distance for focuser.

        Returns:
            float: image distance [mm].

        """
        assert self.f is not None, "f is not set."

        d_i = self.f

        return d_i

    def get_source_distance(self):
        """Calculate source distance for collimator.

        Returns:
            float: source distance [mm].

        """
        assert self.f is not None, "f is not set."

        d_o = self.f

        return d_o

    def get_image_height(self):
        """Calculate the image height along the focal plane for focuser.

        Returns:
            float: image height [mm].

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

        h_i = np.matmul(f, np.transpose(np.tan(a_in)))

        return h_i

    def get_source_height(self):
        """Calculate the source height along the focal plane for collimator.

        Returns:
            float: source height [mm].

        """
        assert self.f is not None, "f is not set."
        assert self.a_out is not None, "a_out is not set."

        # region vectorization
        f = np.array(self.f).reshape(-1, 1)
        a_out = np.array(self.a_out).reshape(-1, 1)
        # endregion

        # region unit conversions
        a_out = np.radians(a_out)  # deg to rad
        # endregion

        h_o = np.matmul(f, np.transpose(np.tan(a_out)))

        return h_o

    def get_focal_length(self):
        """Calculate focal length.

        Returns:
            float: focal length [mm].

        """

        if self.d_i is not None:  # from image distance

            f = self.d_i

        elif self.d_o is not None:  # from source distance

            f = self.d_o

        elif self.h_i is not None and self.a_in is not None:  # from image height

            # region unit conversions
            a_in = np.radians(self.a_in)  # deg to rad
            # endregion

            f = self.h_i / np.tan(a_in)

        elif self.h_o is not None and self.a_out is not None:  # from source height

            # region unit conversions
            a_out = np.radians(self.a_out)  # deg to rad
            # endregion

            f = self.h_o / np.tan(a_out)

        else:
            raise ValueError("d_i or d_o or h_i and a_in or h_o and a_out must be set.")

        return f


class ThickLens:
    """Thick singlet lens component.

    asdsad asd aopsd oamf ian iawwwwwwsm soadasodas om asopd opamd oasdmoasdmoasmdo asmd osamd oasdmoasm opasdm pa ad msad
    as dsa pissoam oam osam opasm fopa oamsa odmwoa dmaopsdao d,oasm foamopam sod aos,d oas, doas
    aspd mas mopad

    Args:
        h1 (float, optional): distance from the primary vertex to the primary principal plane. Defaults to None.
        h2 (float, optional): distance from the secondary vertex to the secondary principal plane. Defaults to None.
        f_thick (float, optional): effective focal length. Defaults to None.
        n (float, optional): index of refraction of the thick lens. Defaults to None.
        d (float, optional): the thickness of the thick lens. Defaults to None.
        R1 (float, optional): the radius of curvature of the first lens surface. Defaults to None.
        R2 (float, optional): the radius of curvature of the second lens surface. Defaults to None.
        s_i (float, optional): the distance from the secondary principal plane to the image. Defaults to None.
        s_o (float, optional): the distance from the object to the primary principal plane. Defaults to None.
        a1 (float, optional): the incident ray angle relative to the optical axis in deg. Defaults to None.
        a2 (float, optional): the emergent ray angle relative to the optical axis in deg. Defaults to None.
        x1 (float, optional): object height relative to the optical axis for the collimator model. Defaults to None.
        x2 (float, optional): image height relative to the optical axis for the focuser model. Defaults to None.

    Distances and heights can be in any units (e.g., mm, cm, m, etc.) as long as the units are consistent.

    """

    def __init__(
        self,
        h1=None,
        h2=None,
        f_thick=None,
        n=None,
        d=None,
        R1=None,
        R2=None,
        s_i=None,
        s_o=None,
        a1=None,
        a2=None,
        x1=None,
        x2=None,
    ):
        self.h1 = h1
        self.h2 = h2
        self.f_thick = f_thick
        self.n = n
        self.d = d
        self.R1 = R1
        self.R2 = R2
        self.s_i = s_i
        self.s_o = s_o
        self.a1 = a1
        self.a2 = a2
        self.x1 = x1
        self.x2 = x2

    def get_focal_length(self):
        """Calculate the focal length of a thick lens in a vacuum.

        Returns:
            float: focal length.

        """

        assert self.n is not None, "n is not set."
        assert self.R1 is not None, "R1 is not set."
        assert self.R2 is not None, "R2 is not set."
        assert self.d is not None, "d is not set."

        f_thick = (self.n * self.R1 * self.R2) / (
            (self.R2 - self.R1) * (self.n - 1) * self.n + ((self.n - 1) ** 2) * self.d
        )

        return f_thick

    def get_principal_planes(self):
        """Calculate the position of the primary and secondary principal planes
        of the thick lens.

        Returns:
            float: distance from lens vertices to principal planes.

        """

        assert self.d is not None, "d is not set."
        assert self.n is not None, "n is not set."
        assert self.R1 is not None, "R1 is not set."
        assert self.R2 is not None, "R2 is not set."
        assert self.f_thick is not None, "f_thick is not set."

        h1 = -(self.f_thick * (self.n - 1) * self.d) / (self.R2 * self.n)
        h2 = -(self.f_thick * (self.n - 1) * self.d) / (self.R1 * self.n)

        return h1, h2

    def get_focuser_image_distance(self):
        """Calculate the image distance along the focal length from the
        principal plane.

        Returns:
            float: image distance.

        """

        assert self.f_thick is not None, "f_thick is not set."

        s_i = self.f_thick

        return s_i

    def get_collimator_object_distance(self):
        """Calculate the object distance along the focal length from the
        principal plane.

        Returns:
            float: object distance.

        """

        assert self.f_thick is not None, "f_thick is not set."

        s_o = self.f_thick

        return s_o

    def get_focuser_image_height(self):
        """Calculate the image height relative to the optical axis (focuser).

        Returns:
            float: image height.

        """

        assert self.f_thick is not None, "f_thick is not set."
        assert self.a1 is not None, "a1 is not set."

        x2 = np.radians(self.a1) * self.f_thick

        return x2

    def get_collimator_emergent_ray_angle(self):
        """Calculate the emergent ray angle (collimator).

        Returns:
            float: emergent ray angle in deg.

        """

        assert self.x1 is not None, "x1 is not set."
        assert self.f_thick is not None, "f_thick is not set."

        a2 = -self.x1 / self.f_thick

        return np.degrees(a2)


class AchromLens:
    """Achromatic doublet component.

    Args:
        V_1 (float, optional): Abbe number for first element. Defaults to None.
        V_2 (float, optional): Abbe number for second element. Defaults to None.
        eta (LUT, optional) transmittace LUT object. Defaults to None.
        f_1 (float, optional): Focal length of first element (mm). Defaults to None.
        f_2 (float, optional): Focal length of second element (mm). Defaults to None.
        f_eq (float, optional): Effective focal length of system (mm). Defaults to None.

    """

    def __init__(
        self,
        V_1=None,
        V_2=None,
        eta=None,
        f_1=None,
        f_2=None,
        f_eq=None,
    ):
        self.V_1 = V_1
        self.V_2 = V_2
        self.eta = eta
        self.f_1 = f_1
        self.f_2 = f_2
        self.f_eq = f_eq

    def focal_length_1(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10**-3  # mm to m
        # endregion

        f_1 = f_eq * (self.V_1 - self.V_2) / self.V_1
        return f_1

    def focal_length_2(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10**-3  # mm to m
        # endregion

        f_2 = -f_eq * (self.V_1 - self.V_2) / self.V_2
        return f_2

    def effective_focal_length(self):

        # region unit conversions
        f_1 = self.f_1 * 10**-3  # mm to m
        f_2 = self.f_2 * 10**-3  # mm to m
        # endregion

        if f_1 is not None:
            f_eq = f_1 * self.V_1 / (self.V_1 - self.V_2)
        elif f_2 is not None:
            f_eq = -f_2 * self.V_2 / (self.V_1 - self.V_2)
        else:
            raise ValueError("f_1 or f_2 must be set.")

        return f_eq

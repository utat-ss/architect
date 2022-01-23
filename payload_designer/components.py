"""Component classes."""

# stdlib
import logging

# external
import numpy as np

# project
from payload_designer.libs import physlib

LOG = logging.getLogger(__name__)

class ThickLens:
    """Thick singlet lens component.

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
        x2=None
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

        f_thick = (self.n * self.R1 * self.R2) / ((self.R2 - self.R1) * (self.n - 1) * self.n + ((self.n - 1) ** 2) * self.d)

        return f_thick
    
    def get_principal_planes(self):
        """Calculate the position of the primary and secondary principal planes of the thick lens.

        Returns:
            float: distance from lens vertices to principal planes.
        """

        assert self.d is not None, "d is not set."
        assert self.n is not None, "n is not set."
        assert self.R1 is not None, "R1 is not set."
        assert self.R2 is not None, "R2 is not set."
        assert self.f_thick is not None, "f_thick is not set."

        h1 = - (self.f_thick * (self.n - 1) * self.d) / (self.R2 * self.n)
        h2 = - (self.f_thick * (self.n - 1) * self.d) / (self.R1 * self.n)

        return h1, h2
    
    def get_focuser_image_distance(self):
        """Calculate the image distance along the focal length from the principal plane.

        Returns:
            float: image distance.
        """

        assert self.f_thick is not None, "f_thick is not set."
        
        s_i = self.f_thick

        return s_i

    def get_collimator_object_distance(self):
        """Calculate the object distance along the focal length from the principal plane.

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
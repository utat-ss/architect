"""Component classes."""

# stdlib
from gettext import install
import logging
from this import d

# external
import numpy as np

# project
from payload_designer.libs import physlib, utillib

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

class Slit:
    """Entrance slit component.

    Args:
        w_i (float, optional): image width. Defaults to None.
        m (float, optional): magnification of the optical bench. Defaults to None.
        f (float, optional): focal length of the foreoptics. Defaults to None.
        w_s (float, optional): slit width. Defaults to None.
        l_s (float, optional): slit length. Defaults to None.
        w_o (float, optional): object width. Defaults to None.
        w_d (float, optional): detector width. Defaults to None.
        fov_h (float, optional): horizontal field of view in degrees. Defaults to None.
        fov_v (float, optional): vertical field of view in degrees. Defaults to None.
    """

    def __init__(self, w_i=None, m=None, f=None, w_s=None, l_s=None, w_o=None, w_d=None, fov_h=None, fov_v=None):
        self.w_i = w_i
        self.m = m
        self.f = f
        self.w_s = w_s
        self.l_s = l_s
        self.w_o = w_o
        self.w_d = w_d
        self.fov_h = fov_h
        self.fov_v = fov_v

    def get_horizontal_field_of_view(self):
        """Caculates the horizontal field of view.

        Returns:
            float: angle (degrees).
        """
        assert self.l_s is not None, "l_s is not set."
        assert self.f is not None, "f is not set."

        fov_h = 2*np.arctan(np.divide(self.l_s, 2*self.f))
        
        return np.divide(np.multiply(fov_h, 180), np.pi)

    def get_vertical_field_of_view(self):
        """Caculates the vertical field of view.

        Returns:
            float: angle (degrees).
        """
        assert self.w_s is not None, "w_s is not set."
        assert self.f is not None, "f is not set."

        fov_v = 2*np.arctan(np.divide(self.w_s, 2*self.f))
        
        return np.divide(np.multiply(fov_v, 180), np.pi)

    def get_image_width(self):
        """Caculates the image width.

        Returns:
            float: image width.
        """
        assert self.m is not None, "m is not set."
        assert self.w_s is not None, "w_s is not set."
        assert self.w_o is not None, "w_o is not set."

        w_i = np.sqrt(np.multiply(np.power(self.m, 2), np.power(self.w_s, 2)) + np.power(self.w_o, 2))

        return w_i
    
    def get_slit_width(self):
        """Caculates the slit width.

        Returns:
            float: slit width (micrometer).
        """
        assert self.m is not None, "m is not set."
        assert self.w_d is not None, "w_d is not set."

        w_s = np.divide(self.w_d, self.m)

        return w_s

class Foreoptics:
    """Foreoptics component.

    Args:
        ds_i (float, optional): image distance. Defaults to None.
        ds_o (float, optional): object distance. Defaults to None.
        n (float, optional): f-number. Defaults to None.
        dm_a (float, optional): aperture diameter. Defaults to None.
        a_in_max (float, optional): maximum angle of incidence in degrees. Defaults to None.
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

    def get_aperture_diameter(self):
        """Calculate the aperture diamter.

        Returns:
            float: aperture diameter (mm).
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

        # region unit conversions
        a_in_max = np.radians(self.a_in_max)  # deg to rad
        # endregion        

        if a_in_max is not None:
            na = np.sin(a_in_max)
        elif self.n is not None:
            na = np.divide(1, 2*self.n)
        else:
            raise ValueError("a_in_max or n must be set.")       

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

        g = np.multiply(np.pi, np.multiply(self.s, np.power(np.sin(a_in_max), 2)))

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


class ThinLens:
    """Thin singlet lens component.

    Args:
        D (float, optional): diameter of the lens [mm]. Defaults to None.
        M (float, optional): mass of lens [g]. Defaults to None.
        T (path-like, optional): path to transmittace LUT data.
        a_in (array_like[float], optional): incoming ray angle relative to optical
            axis [°]. Defaults to None.
        a_out (array_like[float], optional): outgoing ray angle relative to optical
            axis [°]. Defaults to None.
        d_i (array_like[float], optional): distance to image plane [mm]. Defaults to
            None.
        d_o (array_like[float], optional): distance from object plane [mm]. Defaults to
            None.
        f (array_like[float], optional): focal length [mm]. Defaults to None.
        h_i (array_like[float], optional): image height above optical axis [mm].
            Defaults to None.
        h_o (array_like[float], optional): source height above optical axis [mm].
            Defaults to None.
    """

    def __init__(
        self,
        D=None,
        M=None,
        T=None,
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
        self.T = utillib.LUT(T)
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


class AchromDoublet:
    """Achromatic doublet component.

    Args:
        f_1 (float, optional): Focal length of first element (mm). Defaults to None.
        f_2 (float, optional): Focal length of second element (mm). Defaults to None.
        f_eq (float, optional): Effective focal length of system (mm). Defaults to None.
        V_1 (float, optional): Abbe number for first element. Defaults to None.
        V_2 (float, optional): Abbe number for second element. Defaults to None.
    """

    def __init__(
        self,
        f_1=None,
        f_2=None,
        f_eq=None,
        V_1=None,
        V_2=None,
    ):
        self.f_1 = f_1
        self.f_2 = f_2
        self.f_eq = f_eq
        self.V_1 = V_1
        self.V_2 = V_2

    def focal_length_1(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10 ** -3  # mm to m
        # endregion

        f_1 = f_eq * (self.V_1 - self.V_2) / self.V_1
        return f_1

    def focal_length_2(self):
        assert self.V_1 is not None, "V_1 is not set."
        assert self.V_2 is not None, "V_2 is not set."
        assert self.f_eq is not None, "f_eq is not set."

        # region unit conversions
        f_eq = self.f_eq * 10 ** -3  # mm to m
        # endregion

        f_2 = -f_eq * (self.V_1 - self.V_2) / self.V_2
        return f_2

    def effective_focal_length(self):

        # region unit conversions
        f_1 = self.f_1 * 10 ** -3  # mm to m
        f_2 = self.f_2 * 10 ** -3  # mm to m
        # endregion

        if f_1 is not None:
            f_eq = f_1 * self.V_1 / (self.V_1 - self.V_2)
        elif f_2 is not None:
            f_eq = -f_2 * self.V_2 / (self.V_1 - self.V_2)
        else:
            raise ValueError("f_1 or f_2 must be set.")
         
        return f_eq

class SRGrating:
    """Surface-Relief Diffraction Grating component.

    Args:
        alpha (float, optional): incident angle of light. Defaults to None.
        beta (float, optional): diffraction angle. Defaults to None.
        G (float, optional): groove density. Defaults to None.
        lmda (float, optional): wavelength of incident light. Defaults to None.
        m (integer, optional): diffraction order. Defaults to None.
        W (float, optional): ruled width of grating. Defaults to None.
        R (float, optional): resolving power. Defaults to None.
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
    ):
        self.alpha = alpha
        self.beta = beta
        self.G = G
        self.lmda = lmda
        self.m = m
        self.W = W
        self.R = R

    def get_angle_out(self):
        """Calculates the angle of the diffracted light exiting the diffraction grating.

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
        G = G * 10 ** 3 # 1/mm to 1/m
        lmda = lmda * 10 ** (-9) # nm to m
        alpha = np.radians(alpha)  # deg to rad
        # endregion

        beta = np.arcsin(G * m * lmda - np.sin(alpha))

        return beta

    def get_angular_dispersion(self):
        """Calculates the angular dispersion of a grating

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
        lmda = lmda * 10 ** (-9) # nm to m
        # endregion

        D = (np.sin(alpha) + np.sin(beta))/(lmda * np.cos(beta))

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
        lmda = lmda * 10 ** (-9) # nm to m
        W = W * 10 ** (-9) # nm to m
        # endregion

        R = W * (np.sin(alpha) + np.sin(beta)) / lmda

        return R

    def get_anamorphic_amplification(self):
        """Calculates the anamorphic amplification

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

        b_to_a = np.cos(beta)/np.cos(alpha)

        return b_to_a

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

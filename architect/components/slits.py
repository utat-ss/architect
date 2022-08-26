"""Slit components."""

# stdlib
import logging
import math

# external
import numpy as np

# project
from architect.libs import physlib, utillib

LOG = logging.getLogger(__name__)


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

    def __init__(
        self,
        w_i=None,
        m=None,
        f=None,
        w_s=None,
        l_s=None,
        w_o=None,
        w_d=None,
        fov_h=None,
        fov_v=None,
    ):
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

        fov_h = 2 * np.arctan(np.divide(self.l_s, 2 * self.f))

        return np.divide(np.multiply(fov_h, 180), np.pi)

    def get_vertical_field_of_view(self):
        """Caculates the vertical field of view.

        Returns:
            float: angle (degrees).

        """
        assert self.w_s is not None, "w_s is not set."
        assert self.f is not None, "f is not set."

        fov_v = 2 * np.arctan(np.divide(self.w_s, 2 * self.f))

        return np.divide(np.multiply(fov_v, 180), np.pi)

    def get_image_width(self):
        """Caculates the image width.

        Returns:
            float: image width.

        """
        assert self.m is not None, "m is not set."
        assert self.w_s is not None, "w_s is not set."
        assert self.w_o is not None, "w_o is not set."

        w_i = np.sqrt(
            np.multiply(np.power(self.m, 2), np.power(self.w_s, 2))
            + np.power(self.w_o, 2)
        )

        return w_i

    # hello
    def get_slit_width(self):
        """Caculates the slit width.

        Returns:
            float: slit width (micrometer).

        """
        assert self.m is not None, "m is not set."
        assert self.w_d is not None, "w_d is not set."

        w_s = np.divide(self.w_d, self.m)

        return w_s

"""Filter classes."""

# stdlib
import logging
import math

# external
import numpy as np
import scipy.constants as sc

# project
from payload_designer.components.basecomponent import BaseComponent
from payload_designer.libs import physlib, utillib

LOG = logging.getLogger(__name__)


class Filter(BaseComponent):
    def __init__(
        self,
        A=None,
        F=None,
        F_w=None,
        J=None,
        N=None,
        R=None,
        R_1=None,
        R_2=None,
        T_0=None,
        T_1=None,
        T_1w=None,
        T_2=None,
        T_2w=None,
        T_f=None,
        T_w=None,
        d=None,
        delta=None,
        epsilon_1=None,
        epsilon_2=None,
        eta=None,
        k=None,
        lambda_0=None,
        lambda_theta=None,
        n=None,
        n_0=None,
        n_star=None,
        phi_1=None,
        phi_2=None,
        theta=None,
        mass=None,
        V=None,
    ):
        self.A = A
        self.F = F
        self.F_w = F_w
        self.J = J
        self.N = N
        self.R = R
        self.R_1 = R_1
        self.R_2 = R_2
        self.T_0 = T_0
        self.T_1 = T_1
        self.T_1w = T_1w
        self.T_2 = T_2
        self.T_2w = T_2w
        self.T_f = T_f
        self.T_w = T_w
        self.d = d
        self.delta = delta
        self.epsilon_1 = epsilon_1
        self.epsilon_2 = epsilon_2
        self.eta = eta
        self.k = k
        self.lambda_0 = lambda_0
        self.lambda_theta = lambda_theta
        self.n = n
        self.n_0 = n_0
        self.n_star = n_star
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.theta = theta
        self.mass = mass
        self.V = V

    def effective_refractive_index(self):
        assert self.epsilon_1 is not None, "epsilon_1 is not set."
        assert self.epsilon_2 is not None, "epsilon_2 is not set."
        assert self.N is not None, "N is not set."
        assert self.k is not None, "k is not set."
        assert self.n is not None, "n is not set."
        assert self.J is not None, "J is not set."

        A = self.epsilon_1 + self.epsilon_2 + self.N * np.pi
        n_star = (
            (0.5 * A + self.k * np.pi) / ((0.5 * A / self.n**2) + 2 * self.J)
        ) ** 0.5
        return n_star

    def phase_shift(self):
        assert self.lambda_0 is not None, "lambda_0 is not set."
        assert self.n_0 is not None, "n_0 is not set."
        assert self.n_star is not None, "n_star is not set."
        assert self.theta is not None, "theta is not set."

        lambda_theta = (
            self.lambda_0
            * (1 - ((self.n_0 / self.n_star) * np.sin(self.theta)) ** 2) ** 0.5
        )

        return lambda_theta

    def reflected_beam(self):
        assert self.n_star is not None, "n_star is not set."
        assert self.n_0 is not None, "n_0 is not set."

        R = ((self.n_star - self.n_0) / (self.n_star + self.n_0)) ** 2
        return R

    def transmitted_beam_system(self):
        assert self.R_1 is not None, "R_1 is not set."
        assert self.R_2 is not None, "R_2 is not set."
        assert self.theta is not None, "theta is not set."
        assert self.T_1 is not None, "T_1 is not set."
        assert self.T_2 is not None, "T_2 is not set."
        assert self.phi_1 is not None, "phi_1 is not set."
        assert self.phi_2 is not None, "phi_2 is not set."

        T_f = ((self.T_1 * self.T_2) / (1 - (self.R_1 * self.R_2) ** 0.5) ** 2) * (
            1
            / (
                1
                + (
                    (4 * (self.R_1 * self.R_2) ** 0.5)
                    / (1 - (self.R_1 * self.R_2) ** 0.5) ** 2
                )
                * (np.sin(0.5 * self.phi_1 * self.phi_2 - self.theta)) ** 2
            )
        )
        return T_f

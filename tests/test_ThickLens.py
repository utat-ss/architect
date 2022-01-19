"""Tests for Thick Lens component."""
# stdlib
import logging
import math

# external
import numpy as np
import pytest

# project
from payload_designer import components

LOG = logging.getLogger(__name__)

# @pytest.mark.star # will only run these tests # pytest -v -m star
def test_ThickLens_get_focal_length():
    pass

# @pytest.mark.plot # will not run these tests # pytest -v -m "not plot"
def test_ThickLens_get_principal_planes():
    pass

def test_ThickLens_get_focuser_image_distance():
    pass

def test_ThickLens_get_collimator_object_distance():
    pass

def test_ThickLens_get_focuser_emergent_ray_height():
    pass

def test_ThickLens_get_collimator_emergent_ray_angle():
    pass

"""
logs >> pytest >> pytest-report.html

Reveal in file explorer >> ... >> pytest-report.html

Gives you a report of what ran and what went wrong, the log file
"""
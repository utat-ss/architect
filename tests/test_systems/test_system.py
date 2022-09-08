# project
from architect.systems import System
import logging

LOG = logging.getLogger(__name__)

def test_init():
    """Test initialization."""
    system = System()
    LOG.info(system)
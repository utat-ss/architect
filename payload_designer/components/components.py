from .diffractors import SRGrating, VPHGrating, VPHGrism
from .filters import Filter
from .foreoptics import Foreoptic
from .lenses import AchromLens, ThickLens, ThinLens
from .sensors import Sensor, TauSWIR
from .slits import Slit


class Components:
    def __init__(self):
        self.sr_grating_component = SRGrating()
        self.vph_grating_component = VPHGrating()
        self.vph_grism_component = VPHGrism()
        self.filter_component = Filter()
        self.foreoptic_component = Foreoptic()
        self.thin_lens_component = ThinLens()
        self.thick_lens_component = ThickLens()
        self.achrom_lens_component = AchromLens()
        self.sensor_component = Sensor()
        self.tau_swir_component = TauSWIR()
        self.slit_component = Slit()

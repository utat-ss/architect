"""Estimates the payload optical transmittance ratio as a function of wavelength."""

# project
from payload_designer import components

if __name__ == "__main__":

    # component instantiation
    foreoptic = components.Foreoptic(t_ratio=0.8, t_ratio_in=1)
    collimator = components.Collimator(t_ratio=0.8)
    bandfilter = components.Filter(t_ratio=0.8)
    diffractor = components.SRGrating(t_ratio=0.8)
    focuser = components.Focuser(t_ratio=0.8)

    # pipeline
    collimator.t_ratio_in = foreoptic.get_t_ratio_out()
    bandfilter.t_ratio_in = collimator.get_t_ratio_out()
    diffractor.t_ratio_in = bandfilter.get_t_ratio_out()
    focuser.t_ratio_in = diffractor.get_t_ratio_out()

    transmittance_net = focuser.get_t_ratio_out()

    print(f"Net transmittance: {transmittance_net}")

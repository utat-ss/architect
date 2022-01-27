"""Estimates the image height on the focal plane given grism and collimator
component parameters."""

# project
from payload_designer import components

if __name__ == "__main__":

    # component instantiation
    grating = components.VPHGrism(
        a_in=1, n_1=1.5, n_2=1.5, n_3=1.5, v=600, m=1, a=30, l=1600
    )
    focuser = components.ThinFocuser(f=4)

    # pipeline
    focuser.a_in = grating.get_angle_out()
    image_height = focuser.get_image_height()

    print(f"Image height: {image_height}")

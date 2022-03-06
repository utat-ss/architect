
from typing import Optional


class BaseComponent():
    """
    A base class for future components.
    Captures the shared functionalities of all components
    (i.e. shared attributes/methods)

    Args:
        min_operating_temp (float, optional): the min. temparature the
                                              component can generate
        max_operating_temp (float, optional): the max. temperature the
                                              component can generate
    """

    def __init__(
        self,
        min_operating_temp=Optional[float],
        max_operating_temp=Optional[float]
    ):
        self.min_operating_temp = min_operating_temp
        self.max_operating_temp = max_operating_temp

    def calculate_operating_temp_range(self):
        """
        Calculates the operating temperature range of
        this component.
        """

        if self.min_operating_temp and self.max_operating_temp:
            return self.max_operating_temp - self.min_operating_temp
        raise TypeError("Either min_operating_temp or \
                        max_operating_temp are of invalid types.")

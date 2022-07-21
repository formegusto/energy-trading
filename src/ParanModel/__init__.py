import pandas as pd
import numpy as np
from ..model import Household
from .simulation import simulation
from .simulation_result import simulation_result
from .simulation_public import simulation_public


class ParanModel:
    def __init__(self, file_path):
        self.datas = pd.read_csv(file_path)
        self.datas['usage (kWh)'] = np.floor(
            self.datas['usage (kWh)']).astype("int")
        self.households = np.array([Household(name, kwh).set_rate("단일", "기타")
                                    for name, kwh in self.datas.to_numpy()])


ParanModel.simulation = simulation
ParanModel.simulation_result = simulation_result
ParanModel.simulation_public = simulation_public

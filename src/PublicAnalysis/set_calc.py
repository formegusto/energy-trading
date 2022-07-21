from ..Calculator import Calculator
import numpy as np


def set_calc(self, contract="단일", kwh=None, public_percentage=None):
    if self.energy_trader is None:
        self.calc = Calculator(self.meter_month,
                               month=self.month,
                               contract=contract).set_households().set_apt(kwh=kwh, public_percentage=public_percentage).set_bill()
    else:
        if ~np.all(self.energy_trader.datas['usage (kWh)'].values == self.meter_month['usage (kWh)'].values):
            raise ValueError("트레이닝과 가격분배에 사용된 데이터는 같아야 합니다.")
        _sim_datas = self.energy_trader.simulation_datas.copy()
        _sim_datas['usage (kWh)'] = self.meter_month['usage (kWh)']
        self.calc = Calculator(_sim_datas,
                               month=self.month,
                               contract=contract).set_households().set_apt(kwh=kwh, public_percentage=public_percentage).set_bill()
